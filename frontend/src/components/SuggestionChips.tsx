'use client';

import { SuggestionChip as SuggestionChipType } from '@/lib/api';
import { Sparkles } from 'lucide-react';
import { useCallback } from 'react';

interface SuggestionChipsProps {
  chips: SuggestionChipType[];
  onChipClick: (text: string) => void;
  disabled?: boolean;
}

export default function SuggestionChips({
  chips,
  onChipClick,
  disabled = false,
}: SuggestionChipsProps) {
  const handleClick = useCallback((text: string) => {
    console.log('Chip clicked:', text);
    if (!disabled) {
      onChipClick(text);
    }
  }, [onChipClick, disabled]);

  if (chips.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 px-4 py-3">
      <div className="w-full flex items-center gap-2 text-xs text-gray-500 mb-1">
        <Sparkles className="w-3 h-3" />
        <span>Quick suggestions</span>
      </div>
      {chips.map((chip, index) => (
        <button
          key={`${chip.text}-${index}`}
          type="button"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            handleClick(chip.text);
          }}
          disabled={disabled}
          className={`suggestion-chip px-4 py-2 rounded-full text-sm font-medium
                     border-2 border-purple-200 bg-white text-purple-700
                     hover:border-purple-400 hover:bg-purple-50
                     disabled:opacity-50 disabled:cursor-not-allowed
                     transition-all duration-200 cursor-pointer`}
        >
          {chip.text}
        </button>
      ))}
    </div>
  );
}
