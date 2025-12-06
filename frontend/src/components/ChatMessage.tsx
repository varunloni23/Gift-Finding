'use client';

import { User, Bot, Gift } from 'lucide-react';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`message-bubble flex gap-3 ${
        isUser ? 'flex-row-reverse' : 'flex-row'
      }`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser
            ? 'bg-gradient-to-br from-blue-500 to-purple-500'
            : 'bg-gradient-to-br from-pink-500 to-purple-500'
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Gift className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message bubble */}
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-gradient-to-br from-blue-500 to-purple-500 text-white rounded-tr-sm'
            : 'bg-white shadow-md border border-gray-100 text-gray-800 rounded-tl-sm'
        }`}
      >
        <div className="whitespace-pre-wrap text-sm leading-relaxed">
          {message.content}
        </div>
      </div>
    </div>
  );
}

// Typing indicator component
export function TypingIndicator() {
  return (
    <div className="message-bubble flex gap-3">
      <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center bg-gradient-to-br from-pink-500 to-purple-500">
        <Gift className="w-5 h-5 text-white" />
      </div>
      <div className="bg-white shadow-md border border-gray-100 rounded-2xl rounded-tl-sm px-4 py-3">
        <div className="flex items-center gap-1">
          <div className="typing-dot w-2 h-2 bg-purple-400 rounded-full" />
          <div className="typing-dot w-2 h-2 bg-purple-400 rounded-full" />
          <div className="typing-dot w-2 h-2 bg-purple-400 rounded-full" />
        </div>
      </div>
    </div>
  );
}
