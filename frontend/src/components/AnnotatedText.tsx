import React, { useState } from 'react';
import { AnnotatedSpan, SymptomEntity } from '../types/clinical';
import { Sparkles, Info, Eye, Ban, AlertCircle } from 'lucide-react';

interface AnnotatedTextProps {
  text: string;
  spans: AnnotatedSpan[];
  entities: SymptomEntity[];
}

export const AnnotatedText: React.FC<AnnotatedTextProps> = ({ text, spans, entities }) => {
  const [activeSpanIndex, setActiveSpanIndex] = useState<number | null>(null);

  // Filter non-overlapping spans or build segmented fragments
  const renderAnnotatedContent = () => {
    if (!text || spans.length === 0) {
      return <p className="text-slate-600 dark:text-slate-400 italic">No clinical annotations extracted yet.</p>;
    }

    // Sort spans by start offset
    const sortedSpans = [...spans].sort((a, b) => a.start - b.start || (b.end - b.start) - (a.end - a.start));

    // Simple robust linear span segmenter
    const segments: React.ReactNode[] = [];
    let currentIdx = 0;

    // Filter out spans that are completely enclosed inside an earlier span to keep markup clean
    const nonOverlapping: AnnotatedSpan[] = [];
    for (const span of sortedSpans) {
      if (span.start >= currentIdx) {
        nonOverlapping.push(span);
        currentIdx = span.end;
      }
    }

    currentIdx = 0;
    nonOverlapping.forEach((span, idx) => {
      // Plain text before span
      if (span.start > currentIdx) {
        segments.push(
          <span key={`plain-${currentIdx}`} className="text-slate-800 dark:text-slate-200">
            {text.slice(currentIdx, span.start)}
          </span>
        );
      }

      // Find if this span corresponds to a negated or uncertain symptom entity
      const matchedEntity = entities.find(e => 
        (e.start_char === span.start && e.end_char === span.end) ||
        (span.label === 'SYMPTOMS' && e.name.toLowerCase() === span.text.toLowerCase())
      );

      const isNegated = matchedEntity?.assertion === 'negated';
      const isUncertain = matchedEntity?.certainty === 'uncertain';

      // Style determination
      let spanBg = 'bg-sky-100 text-sky-900 border-sky-300 dark:bg-sky-950/70 dark:text-sky-200 dark:border-sky-800';
      let badgeLabel: string = span.label;

      if (span.label === 'SYMPTOMS') {
        if (isNegated) {
          spanBg = 'bg-rose-100 text-rose-900 line-through decoration-rose-500 decoration-2 border-rose-300 dark:bg-rose-950/70 dark:text-rose-200 dark:border-rose-800';
          badgeLabel = 'NEGATED SYMPTOM';
        } else if (isUncertain) {
          spanBg = 'bg-amber-100 text-amber-900 border-dashed border-amber-400 dark:bg-amber-950/70 dark:text-amber-200 dark:border-amber-700';
          badgeLabel = 'UNCERTAIN SYMPTOM';
        } else {
          spanBg = 'bg-emerald-100 text-emerald-950 font-semibold border-emerald-300 dark:bg-emerald-950/70 dark:text-emerald-200 dark:border-emerald-800';
          badgeLabel = 'SYMPTOM (AFFIRMED)';
        }
      } else if (span.label === 'BODY_LOCATION') {
        spanBg = 'bg-indigo-100 text-indigo-900 border-indigo-300 dark:bg-indigo-950/70 dark:text-indigo-200 dark:border-indigo-800';
      } else if (span.label === 'DURATION_ONSET') {
        spanBg = 'bg-purple-100 text-purple-900 border-purple-300 dark:bg-purple-950/70 dark:text-purple-200 dark:border-purple-800';
      } else if (span.label === 'SEVERITY') {
        spanBg = 'bg-orange-100 text-orange-900 font-semibold border-orange-300 dark:bg-orange-950/70 dark:text-orange-200 dark:border-orange-800';
      } else if (span.label === 'NEGATION_CUE') {
        spanBg = 'bg-red-50 text-red-700 border-red-300 dark:bg-red-950/50 dark:text-red-300 dark:border-red-900';
        badgeLabel = 'NEGATION TRIGGER';
      } else if (span.label === 'UNCERTAINTY_CUE') {
        spanBg = 'bg-yellow-50 text-yellow-800 border-yellow-300 dark:bg-yellow-950/50 dark:text-yellow-300 dark:border-yellow-900';
        badgeLabel = 'UNCERTAINTY TRIGGER';
      }

      segments.push(
        <span
          key={`span-${idx}`}
          onMouseEnter={() => setActiveSpanIndex(idx)}
          onMouseLeave={() => setActiveSpanIndex(null)}
          className={`relative inline-flex items-center px-2 py-0.5 mx-0.5 rounded-md border text-xs transition-all cursor-pointer ${spanBg} ${
            activeSpanIndex === idx ? 'ring-2 ring-sky-500 scale-[1.02] shadow-sm' : ''
          }`}
        >
          <span>{text.slice(span.start, span.end)}</span>
          <span className="ml-1 text-[9px] font-bold opacity-75 uppercase tracking-tight">
            [{badgeLabel}]
          </span>
        </span>
      );

      currentIdx = span.end;
    });

    // Plain text after last span
    if (currentIdx < text.length) {
      segments.push(
        <span key={`plain-${currentIdx}`} className="text-slate-800 dark:text-slate-200">
          {text.slice(currentIdx)}
        </span>
      );
    }

    return segments;
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm transition-colors">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-3 mb-3 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center space-x-2">
          <Eye className="h-4 w-4 text-sky-600 dark:text-sky-400" />
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">
            Interactive Token &amp; Span Visualizer
          </h3>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-1.5 text-[10px]">
          <span className="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 font-semibold border border-emerald-200 dark:border-emerald-800">
            Symptom (Affirmed)
          </span>
          <span className="px-2 py-0.5 rounded bg-rose-100 dark:bg-rose-950/80 text-rose-800 dark:text-rose-300 line-through border border-rose-200 dark:border-rose-800">
            Negated Finding
          </span>
          <span className="px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300 border border-dashed border-amber-300 dark:border-amber-800">
            Uncertain/Possible
          </span>
          <span className="px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-950/80 text-indigo-800 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
            Body Location
          </span>
          <span className="px-2 py-0.5 rounded bg-purple-100 dark:bg-purple-950/80 text-purple-800 dark:text-purple-300 border border-purple-200 dark:border-purple-800">
            Duration/Onset
          </span>
          <span className="px-2 py-0.5 rounded bg-orange-100 dark:bg-orange-950/80 text-orange-800 dark:text-orange-300 border border-orange-200 dark:border-orange-800">
            Severity
          </span>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-950/60 border border-slate-200/80 dark:border-slate-800/80 leading-relaxed text-sm md:text-base font-sans select-text">
        {renderAnnotatedContent()}
      </div>

      <div className="mt-2.5 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
        <span className="flex items-center gap-1">
          <Info className="h-3.5 w-3.5" /> Hover over any highlighted span to inspect the exact label and clinical attributes.
        </span>
        <span className="text-[11px] font-mono">
          {spans.length} spans extracted
        </span>
      </div>
    </div>
  );
};
