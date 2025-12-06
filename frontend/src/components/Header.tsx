'use client';

import { Gift, Sparkles, RotateCcw } from 'lucide-react';
import { useCallback } from 'react';

interface HeaderProps {
  onNewChat: () => void;
}

export default function Header({ onNewChat }: HeaderProps) {
  const handleNewChat = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('New chat clicked');
    onNewChat();
  }, [onNewChat]);

  return (
    <header className="bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 text-white shadow-lg">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-white/20 rounded-xl backdrop-blur-sm">
            <Gift className="w-8 h-8 gift-icon" />
          </div>
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-2">
              Gift Finder
              <Sparkles className="w-5 h-5" />
            </h1>
            <p className="text-sm text-white/80">
              AI-powered gift suggestions
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={handleNewChat}
          className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg 
                     backdrop-blur-sm transition-all duration-200 
                     flex items-center gap-2 text-sm font-medium cursor-pointer"
        >
          <RotateCcw className="w-4 h-4" />
          <span>New Chat</span>
        </button>
      </div>
    </header>
  );
}
