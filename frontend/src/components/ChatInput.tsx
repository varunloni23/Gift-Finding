'use client';

import { useState, FormEvent } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export default function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Describe who you need a gift for...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-end gap-2 p-4 bg-white border-t border-gray-100">
        <div className="flex-1 relative">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className="w-full px-4 py-3 pr-12 rounded-2xl border-2 border-gray-200 
                       focus:border-purple-400 focus:ring-2 focus:ring-purple-100
                       resize-none transition-all duration-200
                       placeholder:text-gray-400 text-gray-800
                       disabled:bg-gray-50 disabled:cursor-not-allowed"
            style={{
              minHeight: '48px',
              maxHeight: '120px',
            }}
          />
        </div>
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="flex-shrink-0 p-3 rounded-xl 
                     bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500
                     text-white shadow-lg hover:shadow-xl
                     disabled:opacity-50 disabled:cursor-not-allowed
                     transition-all duration-200 hover:scale-105"
        >
          {disabled ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </button>
      </div>
    </form>
  );
}
