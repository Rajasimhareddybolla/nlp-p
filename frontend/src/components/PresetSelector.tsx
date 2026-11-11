import React from 'react';
import { PresetCase } from '../types/clinical';
import { Sparkles, Brain, Heart, Baby, Stethoscope, Compass } from 'lucide-react';

interface PresetSelectorProps {
  presets: PresetCase[];
  selectedId: string;
  onSelect: (preset: PresetCase) => void;
}

export const PresetSelector: React.FC<PresetSelectorProps> = ({ presets, selectedId, onSelect }) => {
  const getIcon = (id: string) => {
    if (id.includes('neuro-prompt')) return <Brain className="h-4 w-4 text-purple-500" />;
    if (id.includes('cardiac')) return <Heart className="h-4 w-4 text-rose-500" />;
    if (id.includes('peds')) return <Baby className="h-4 w-4 text-amber-500" />;
    if (id.includes('gi')) return <Stethoscope className="h-4 w-4 text-emerald-500" />;
    return <Compass className="h-4 w-4 text-sky-500" />;
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
          <Sparkles className="h-3.5 w-3.5 text-amber-500" />
          Validated Clinical Benchmark Presets
        </label>
        <span className="text-[11px] text-slate-500 dark:text-slate-400">
          Click any case to test schema extraction &amp; assertion rules
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
        {presets.map((preset) => {
          const isSelected = selectedId === preset.id;
          return (
            <button
              key={preset.id}
              onClick={() => onSelect(preset)}
              className={`p-3 rounded-xl text-left border transition-all relative flex flex-col justify-between ${
                isSelected
                  ? 'bg-sky-50 dark:bg-sky-950/40 border-sky-500 dark:border-sky-500 ring-2 ring-sky-500/20 shadow-xs'
                  : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/60'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <div className="p-1 rounded-md bg-slate-100 dark:bg-slate-800">
                    {getIcon(preset.id)}
                  </div>
                  <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                    {preset.category.split('/')[0].trim()}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-slate-900 dark:text-white line-clamp-1">
                  {preset.title.split(':')[1]?.trim() || preset.title}
                </h4>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 line-clamp-2 leading-snug">
                  {preset.subtitle}
                </p>
              </div>

              <div className="mt-2 pt-2 border-t border-slate-100 dark:border-slate-800/80 flex flex-wrap gap-1">
                {preset.key_highlights.slice(0, 2).map((tag, i) => (
                  <span
                    key={i}
                    className="text-[9px] font-medium px-1.5 py-0.5 rounded bg-slate-200/60 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};

