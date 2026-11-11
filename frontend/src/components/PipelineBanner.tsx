import React, { useState } from 'react';
import { ChevronRight, Layers, HelpCircle, AlertOctagon, CheckCircle2 } from 'lucide-react';
import { DownstreamReadiness } from '../types/clinical';

interface PipelineBannerProps {
  readiness?: DownstreamReadiness;
}

export const PipelineBanner: React.FC<PipelineBannerProps> = ({ readiness }) => {
  const [showExplanation, setShowExplanation] = useState(false);

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm transition-colors">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 mb-3">
        <div className="flex items-center space-x-2">
          <Layers className="h-4 w-4 text-sky-600 dark:text-sky-400" />
          <h2 className="text-sm font-bold text-slate-800 dark:text-slate-100 uppercase tracking-wider">
            Clinical Decision Pipeline Context
          </h2>
          <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-medium">
            Stage 1 Active
          </span>
        </div>

        <button
          onClick={() => setShowExplanation(!showExplanation)}
          className="text-xs text-sky-600 dark:text-sky-400 hover:text-sky-700 dark:hover:text-sky-300 flex items-center gap-1 font-medium"
        >
          <HelpCircle className="h-3.5 w-3.5" />
          {showExplanation ? 'Hide Stage Architecture' : 'Why Separate Triaging Stages?'}
        </button>
      </div>

      {/* The 4 Pipeline Stages */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
        {/* Stage 1 */}
        <div className="p-3 rounded-xl border-2 border-sky-500 bg-sky-50/60 dark:bg-sky-950/30 relative">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold text-sky-700 dark:text-sky-300">STAGE 1 &bull; THIS ENGINE</span>
            <CheckCircle2 className="h-4 w-4 text-sky-600 dark:text-sky-400" />
          </div>
          <p className="text-xs font-semibold text-slate-900 dark:text-white">Information Extraction</p>
          <p className="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5">
            Free-text &rarr; 5 structured labels + negation &amp; uncertainty
          </p>
        </div>

        {/* Stage 2 */}
        <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-800/40">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold text-slate-500 dark:text-slate-400">STAGE 2 &bull; DOWNSTREAM</span>
            <ChevronRight className="h-3.5 w-3.5 text-slate-400" />
          </div>
          <p className="text-xs font-semibold text-slate-800 dark:text-slate-200">Disease Classification</p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
            5 labels &rarr; differential disease candidates (classifier)
          </p>
        </div>

        {/* Stage 3 */}
        <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-800/40">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold text-slate-500 dark:text-slate-400">STAGE 3 &bull; DOWNSTREAM</span>
            <ChevronRight className="h-3.5 w-3.5 text-slate-400" />
          </div>
          <p className="text-xs font-semibold text-slate-800 dark:text-slate-200">Department Routing</p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
            Symptom context &rarr; recommended clinic or ER dept
          </p>
        </div>

        {/* Stage 4 */}
        <div className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-800/40">
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold text-slate-500 dark:text-slate-400">STAGE 4 &bull; SAFETY LAYER</span>
            <AlertOctagon className="h-3.5 w-3.5 text-amber-500" />
          </div>
          <p className="text-xs font-semibold text-slate-800 dark:text-slate-200">Urgency Assessment</p>
          <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
            Red flags &amp; clinical rules &rarr; urgency triage tier
          </p>
        </div>
      </div>

      {showExplanation && (
        <div className="mt-3.5 p-3.5 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 leading-relaxed space-y-2">
          <p className="font-semibold text-slate-900 dark:text-white flex items-center gap-1.5">
            <AlertOctagon className="h-4 w-4 text-amber-500 shrink-0" />
            Clinical Decoupling Rationale (Why Stage 1 is Independent):
          </p>
          <p>
            Predicting a disease does <strong>not</strong> automatically establish which department a patient should visit or how urgently they need care. For instance, headache and nausea alone cannot establish a particular diagnosis.
          </p>
          <p>
            However, a <strong>severe headache accompanied by new acute blurred vision</strong> warrants prompt immediate emergency assessment. A safety layer must never allow an ordinary disease classifier to dismiss concerning warning symptoms. Stage 1 ensures pristine, uncorrupted feature extraction without hallucinating false severities or turning negated symptoms into positives.
          </p>
        </div>
      )}
    </div>
  );
};

