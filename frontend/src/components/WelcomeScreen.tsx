'use client';

import { Gift, MessageCircle } from 'lucide-react';
import { SuggestionChip } from '@/lib/api';
import { useCallback } from 'react';

interface WelcomeScreenProps {
  suggestions: SuggestionChip[];
  onSuggestionClick: (text: string) => void;
}

export default function WelcomeScreen({
  suggestions,
  onSuggestionClick,
}: WelcomeScreenProps) {
  const handleClick = useCallback((text: string) => {
    console.log('Suggestion clicked:', text);
    onSuggestionClick(text);
  }, [onSuggestionClick]);

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
      {/* Animated gift icon */}
      <div className="mb-6 p-6 bg-gradient-to-br from-pink-100 to-purple-100 rounded-full">
        <Gift className="w-16 h-16 text-purple-500 gift-icon" />
      </div>

      {/* Welcome text */}
      <h2 className="text-3xl font-bold mb-3">
        <span className="gradient-text">Find the Perfect Gift</span>
      </h2>
      <p className="text-gray-600 mb-8 max-w-md">
        Tell me about the person you&apos;re shopping for, and I&apos;ll help you find
        thoughtful gift ideas they&apos;ll love!
      </p>

      {/* Quick start suggestions */}
      <div className="space-y-4 w-full max-w-lg">
        <div className="flex items-center justify-center gap-2 text-sm text-gray-500">
          <MessageCircle className="w-4 h-4" />
          <span>Try one of these to get started:</span>
        </div>
        <div className="flex flex-wrap justify-center gap-3">
          {suggestions.map((suggestion, index) => (
            <button
              key={`${suggestion.text}-${index}`}
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                handleClick(suggestion.text);
              }}
              className="suggestion-chip px-5 py-3 rounded-full text-sm font-medium
                         bg-white border-2 border-purple-200 text-purple-700
                         hover:border-purple-400 hover:bg-purple-50 hover:shadow-md
                         transition-all duration-200 cursor-pointer"
            >
              {suggestion.text}
            </button>
          ))}
        </div>
      </div>

      {/* Tips section */}
      <div className="mt-12 p-6 bg-white/50 rounded-2xl border border-purple-100 max-w-lg">
        <h3 className="font-semibold text-gray-800 mb-3">💡 Tips for better suggestions:</h3>
        <ul className="text-sm text-gray-600 text-left space-y-2">
          <li>• Share their hobbies and interests</li>
          <li>• Mention the occasion (birthday, holiday, etc.)</li>
          <li>• Let me know your budget</li>
          <li>• Tell me about your relationship to them</li>
        </ul>
      </div>
    </div>
  );
}
