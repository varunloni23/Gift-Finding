'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import Header from '@/components/Header';
import ChatMessage, { TypingIndicator, Message } from '@/components/ChatMessage';
import ChatInput from '@/components/ChatInput';
import SuggestionChips from '@/components/SuggestionChips';
import WelcomeScreen from '@/components/WelcomeScreen';
import {
  sendMessage,
  getInitialSuggestions,
  SuggestionChip,
} from '@/lib/api';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [suggestionChips, setSuggestionChips] = useState<SuggestionChip[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [initialSuggestions, setInitialSuggestions] = useState<SuggestionChip[]>([
    { text: 'Gift for my mom', type: 'starter' },
    { text: 'Birthday present ideas', type: 'starter' },
    { text: 'Gifts under $50', type: 'starter' },
    { text: 'Unique gift ideas', type: 'starter' },
  ]);

  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Fetch initial suggestions on mount
  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const data = await getInitialSuggestions();
        if (data.suggestions) {
          setInitialSuggestions(data.suggestions);
        }
      } catch (err) {
        console.log('Using default suggestions');
      }
    };
    fetchSuggestions();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  // Handle sending a message
  const handleSendMessage = useCallback(async (text: string) => {
    if (!text.trim() || isLoading) return;
    
    console.log('Sending message:', text);
    setError(null);
    
    // Add user message to chat
    const userMessage: Message = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setSuggestionChips([]); // Clear chips while loading

    try {
      const response = await sendMessage(text, conversationId || undefined);
      console.log('Response received:', response);
      
      // Update conversation ID if new
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response to chat
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Update suggestion chips
      if (response.suggestion_chips && response.suggestion_chips.length > 0) {
        setSuggestionChips(response.suggestion_chips);
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to get a response. Please try again.');
      
      // Remove the user message if there was an error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  }, [conversationId, isLoading]);

  // Handle clicking a suggestion chip
  const handleChipClick = useCallback((text: string) => {
    console.log('Chip click handler:', text);
    handleSendMessage(text);
  }, [handleSendMessage]);

  // Handle starting a new chat
  const handleNewChat = useCallback(() => {
    console.log('Starting new chat');
    setMessages([]);
    setSuggestionChips([]);
    setConversationId(null);
    setError(null);
  }, []);

  const hasMessages = messages.length > 0;

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-purple-50 to-white">
      <Header onNewChat={handleNewChat} />

      <main className="flex-1 flex flex-col overflow-hidden max-w-4xl mx-auto w-full">
        {!hasMessages ? (
          <WelcomeScreen
            suggestions={initialSuggestions}
            onSuggestionClick={handleChipClick}
          />
        ) : (
          <>
            {/* Chat messages container */}
            <div
              ref={chatContainerRef}
              className="chat-container flex-1 overflow-y-auto p-4 space-y-4"
            >
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))}
              
              {isLoading && <TypingIndicator />}

              {error && (
                <div className="text-center py-2">
                  <span className="inline-block px-4 py-2 bg-red-100 text-red-700 rounded-lg text-sm">
                    {error}
                  </span>
                </div>
              )}
            </div>

            {/* Suggestion chips */}
            {!isLoading && suggestionChips.length > 0 && (
              <SuggestionChips
                chips={suggestionChips}
                onChipClick={handleChipClick}
                disabled={isLoading}
              />
            )}
          </>
        )}

        {/* Chat input */}
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </main>
    </div>
  );
}
