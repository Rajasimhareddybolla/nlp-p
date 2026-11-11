import React from 'react';
import { SymptomEntity } from '../types/clinical';
import { Table, CheckCircle2, Ban, HelpCircle, AlertCircle } from 'lucide-react';

interface EntityMatrixProps {
  entities: SymptomEntity[];
}

export const EntityMatrix: React.FC<EntityMatrixProps> = ({ entities }) => {
  if (entities.length === 0) return null;

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm transition-colors overflow-hidden">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center space-x-2">
          <Table className="h-4 w-4 text-sky-600 dark:text-sky-400" />
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">
            Clinical Entity &amp; Attribute Binding Audit Matrix
          </h3>
        </div>
        <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
          {entities.length} total clinical entities analyzed
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-800/40 text-[11px] font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              <th className="py-2.5 px-3">Symptom</th>
              <th className="py-2.5 px-3">Matched Text</th>
              <th className="py-2.5 px-3">Body Location</th>
              <th className="py-2.5 px-3">Duration / Onset</th>
              <th className="py-2.5 px-3">Severity</th>
              <th className="py-2.5 px-3">Assertion Status</th>
              <th className="py-2.5 px-3">Certainty Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-sans">
            {entities.map((ent) => {
              const isNegated = ent.assertion === 'negated';
              const isUncertain = ent.certainty === 'uncertain';

              return (
                <tr
                  key={ent.id}
                  className={`hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors ${
                    isNegated ? 'opacity-80 bg-rose-50/20 dark:bg-rose-950/10' : ''
                  }`}
                >
                  {/* Canonical Symptom */}
                  <td className="py-2.5 px-3 font-semibold text-slate-900 dark:text-slate-100 capitalize flex items-center gap-1.5">
                    {isNegated ? (
                      <Ban className="h-3.5 w-3.5 text-rose-500 shrink-0" />
                    ) : isUncertain ? (
                      <HelpCircle className="h-3.5 w-3.5 text-amber-500 shrink-0" />
                    ) : (
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500 shrink-0" />
                    )}
                    <span className={isNegated ? 'line-through text-rose-700 dark:text-rose-400' : ''}>
                      {ent.name}
                    </span>
                  </td>

                  {/* Matched Span */}
                  <td className="py-2.5 px-3 text-slate-600 dark:text-slate-400 font-mono text-[11px]">
                    "{ent.raw_span}"
                  </td>

                  {/* Body Location */}
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 font-medium capitalize border border-indigo-100 dark:border-indigo-900">
                      {ent.body_location}
                    </span>
                  </td>

                  {/* Duration / Onset */}
                  <td className="py-2.5 px-3 font-mono">
                    <span
                      className={`px-2 py-0.5 rounded text-[11px] ${
                        ent.duration_onset === 'unknown'
                          ? 'text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800'
                          : 'text-purple-700 dark:text-purple-300 bg-purple-50 dark:bg-purple-950/60 font-semibold border border-purple-200 dark:border-purple-800'
                      }`}
                    >
                      {ent.duration_onset}
                    </span>
                  </td>

                  {/* Severity */}
                  <td className="py-2.5 px-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[11px] font-mono uppercase tracking-wider ${
                        ent.severity === 'severe'
                          ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 font-bold border border-rose-200 dark:border-rose-900'
                          : ent.severity === 'moderate'
                          ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 font-semibold'
                          : ent.severity === 'mild'
                          ? 'bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-300'
                          : 'text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800'
                      }`}
                    >
                      {ent.severity}
                    </span>
                  </td>

                  {/* Assertion Status */}
                  <td className="py-2.5 px-3">
                    {isNegated ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 font-semibold border border-rose-200 dark:border-rose-900">
                        <Ban className="h-3 w-3" /> Negated {ent.negation_cue ? `("${ent.negation_cue}")` : ''}
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-medium border border-emerald-200 dark:border-emerald-800">
                        <CheckCircle2 className="h-3 w-3" /> Affirmed
                      </span>
                    )}
                  </td>

                  {/* Certainty Status */}
                  <td className="py-2.5 px-3">
                    {isUncertain ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 font-semibold border border-dashed border-amber-300 dark:border-amber-800">
                        <HelpCircle className="h-3 w-3" /> Uncertain {ent.uncertainty_cue ? `("${ent.uncertainty_cue}")` : ''}
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-medium">
                        Confirmed
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

