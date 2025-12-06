/**
 * API service for communicating with the Gift-Finding Chatbot backend.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SuggestionChip {
  text: string;
  type: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export interface ChatResponse {
  response: string;
  suggestion_chips: SuggestionChip[];
  conversation_id: string;
}

export interface ConversationHistory {
  conversation_id: string;
  messages: ChatMessage[];
}

/**
 * Send a chat message to the backend and get a response.
 */
export async function sendMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to send message');
  }

  return response.json();
}

/**
 * Create a new conversation.
 */
export async function createConversation(): Promise<{ conversation_id: string }> {
  const response = await fetch(`${API_URL}/api/conversations/new`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Failed to create conversation');
  }

  return response.json();
}

/**
 * Get conversation history.
 */
export async function getConversationHistory(
  conversationId: string
): Promise<ConversationHistory> {
  const response = await fetch(
    `${API_URL}/api/conversations/${conversationId}/history`
  );

  if (!response.ok) {
    throw new Error('Failed to get conversation history');
  }

  return response.json();
}

/**
 * Delete a conversation.
 */
export async function deleteConversation(conversationId: string): Promise<void> {
  const response = await fetch(
    `${API_URL}/api/conversations/${conversationId}`,
    {
      method: 'DELETE',
    }
  );

  if (!response.ok) {
    throw new Error('Failed to delete conversation');
  }
}

/**
 * Get initial suggestion chips.
 */
export async function getInitialSuggestions(): Promise<{
  suggestions: SuggestionChip[];
}> {
  const response = await fetch(`${API_URL}/api/suggestions/initial`);

  if (!response.ok) {
    // Return default suggestions if the endpoint fails
    return {
      suggestions: [
        { text: 'Gift for my mom', type: 'starter' },
        { text: 'Birthday present ideas', type: 'starter' },
        { text: 'Gifts under $50', type: 'starter' },
        { text: 'Unique gift ideas', type: 'starter' },
      ],
    };
  }

  return response.json();
}

/**
 * Health check for the backend.
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
