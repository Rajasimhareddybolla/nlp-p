import React from 'react';
import { 
  ClinicalStructuredRepresentation, 
  SymptomEntity 
} from '../types/clinical';
import { 
  Activity, 
  MapPin, 
  Clock, 
  Flame, 
  Network, 
  Ban, 
  HelpCircle, 
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

interface TargetSchemaDashboardProps {
  data: ClinicalStructuredRepresentation;
}

export const TargetSchemaDashboard: React.FC<TargetSchemaDashboardProps> = ({ data }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between pb-1 border-b border-slate-200 dark:border-slate-800">
        <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <Activity className="h-4 w-4 text-sky-600 dark:text-sky-400" />
          Target Extraction Schema &bull; The 5 Core Labels
        </h3>
        <span className="text-xs text-slate-500 dark:text-slate-400">
          Strict Attribute Binding &amp; Clinical Context Preservation
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* LABEL 1: SYMPTOMS (with Negation & Uncertainty Scoping) */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-col justify-between transition-colors">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
                Label 1 &bull; SYMPTOMS
              </span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 font-semibold border border-emerald-200 dark:border-emerald-800">
                {data.symptoms.length} confirmed
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
              Identifies confirmed clinical findings while decoupling negated and uncertain complaints.
            </p>

            {/* Confirmed Symptoms */}
            <div className="space-y-2 mb-3">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                Confirmed Findings:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {data.symptoms.length > 0 ? (
                  data.symptoms.map((sym, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 text-emerald-800 dark:text-emerald-200 text-xs font-semibold border border-emerald-200 dark:border-emerald-800 shadow-2xs"
                    >
                      <CheckCircle2 className="h-3 w-3 text-emerald-600 dark:text-emerald-400" />
                      {sym}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-400 italic">None confirmed</span>
                )}
              </div>
            </div>

            {/* Negated Symptoms (Crucial Safety Feature) */}
            {data.negated_symptoms.length > 0 && (
              <div className="space-y-1.5 pt-2 border-t border-slate-100 dark:border-slate-800">
                <span className="text-[10px] font-bold uppercase tracking-wider text-rose-500 flex items-center gap-1">
                  <Ban className="h-3 w-3" /> Preserved Negations (Not Present):
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {data.negated_symptoms.map((sym, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md bg-rose-50 dark:bg-rose-950/50 text-rose-700 dark:text-rose-300 text-xs line-through border border-rose-200 dark:border-rose-900"
                    >
                      {sym}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Uncertain / Speculative Symptoms */}
            {data.uncertain_symptoms.length > 0 && (
              <div className="space-y-1.5 pt-2 border-t border-slate-100 dark:border-slate-800">
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-500 flex items-center gap-1">
                  <HelpCircle className="h-3 w-3" /> Preserved Uncertainties (Unconfirmed):
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {data.uncertain_symptoms.map((sym, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md bg-amber-50 dark:bg-amber-950/50 text-amber-800 dark:text-amber-300 text-xs border border-dashed border-amber-300 dark:border-amber-800"
                    >
                      {sym}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* LABEL 2: BODY_LOCATION */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-col justify-between transition-colors">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-indigo-500"></span>
                Label 2 &bull; BODY_LOCATION
              </span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 font-semibold border border-indigo-200 dark:border-indigo-800">
                {data.body_location.length} regions
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
              Distinguishes symptoms by specific anatomical location to guide specialized triage.
            </p>

            <div className="flex flex-wrap gap-2">
              {data.body_location.length > 0 ? (
                data.body_location.map((loc, idx) => (
                  <div
                    key={idx}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-900 dark:text-indigo-200 text-xs font-semibold border border-indigo-200 dark:border-indigo-800 shadow-2xs"
                  >
                    <MapPin className="h-3.5 w-3.5 text-indigo-600 dark:text-indigo-400" />
                    <span className="capitalize">{loc}</span>
                  </div>
                ))
              ) : (
                <span className="text-xs text-slate-400 italic">No specific location specified</span>
              )}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 dark:text-slate-400 flex items-center justify-between">
            <span>Anatomical Mapping:</span>
            <span className="font-semibold text-slate-700 dark:text-slate-300">
              {data.body_location.join(', ') || 'N/A'}
            </span>
          </div>
        </div>

        {/* LABEL 3: DURATION_ONSET */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-col justify-between transition-colors">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-bold text-purple-600 dark:text-purple-400 uppercase tracking-wider flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-purple-500"></span>
                Label 3 &bull; DURATION_ONSET
              </span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-purple-50 text-purple-700 dark:bg-purple-950/60 dark:text-purple-300 font-semibold border border-purple-200 dark:border-purple-800">
                Timeline Matrix
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
              Captures how long symptoms have lasted and exact onset timestamps per symptom.
            </p>

            <div className="space-y-1.5">
              {Object.entries(data.duration_onset).map(([symptom, duration], idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60 text-xs"
                >
                  <span className="font-medium text-slate-800 dark:text-slate-200 capitalize">
                    {symptom}
                  </span>
                  <span
                    className={`font-mono text-[11px] px-2 py-0.5 rounded ${
                      duration === 'unknown'
                        ? 'text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800'
                        : 'text-purple-700 dark:text-purple-300 bg-purple-50 dark:bg-purple-950/60 font-semibold border border-purple-200 dark:border-purple-800'
                    }`}
                  >
                    {duration}
                  </span>
                </div>
              ))}
              {Object.keys(data.duration_onset).length === 0 && (
                <span className="text-xs text-slate-400 italic">No symptoms mapped</span>
              )}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 dark:text-slate-400">
            Note: Onset times are strictly bound without cross-contamination.
          </div>
        </div>

        {/* LABEL 4: SEVERITY */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-col justify-between transition-colors">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-bold text-orange-600 dark:text-orange-400 uppercase tracking-wider flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-orange-500"></span>
                Label 4 &bull; SEVERITY
              </span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-orange-50 text-orange-700 dark:bg-orange-950/60 dark:text-orange-300 font-semibold border border-orange-200 dark:border-orange-800">
                Intensity Level
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
              Captures reported intensity. Notice that severity is <strong>not invented</strong> when unspecified.
            </p>

            <div className="space-y-1.5">
              {Object.entries(data.severity).map(([symptom, sev], idx) => {
                let badgeClass = 'text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800';
                if (sev === 'severe') {
                  badgeClass = 'text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-950/60 font-bold border border-rose-200 dark:border-rose-900';
                } else if (sev === 'moderate') {
                  badgeClass = 'text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-950/60 font-semibold border border-amber-200 dark:border-amber-800';
                } else if (sev === 'mild') {
                  badgeClass = 'text-sky-700 dark:text-sky-300 bg-sky-50 dark:bg-sky-950/60 font-medium border border-sky-200 dark:border-sky-800';
                }

                return (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60 text-xs"
                  >
                    <span className="font-medium text-slate-800 dark:text-slate-200 capitalize">
                      {symptom}
                    </span>
                    <span className={`text-[11px] font-mono px-2 py-0.5 rounded uppercase tracking-wider ${badgeClass}`}>
                      {sev}
                    </span>
                  </div>
                );
              })}
              {Object.keys(data.severity).length === 0 && (
                <span className="text-xs text-slate-400 italic">No symptoms mapped</span>
              )}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 dark:text-slate-400">
            Unspecified symptoms correctly maintain: <code className="text-xs font-mono">"unknown"</code>
          </div>
        </div>

        {/* LABEL 5: ASSOCIATED_SYMPTOMS */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-col justify-between transition-colors md:col-span-2 lg:col-span-2">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-bold text-teal-600 dark:text-teal-400 uppercase tracking-wider flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-teal-500"></span>
                Label 5 &bull; ASSOCIATED_SYMPTOMS
              </span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-teal-50 text-teal-700 dark:bg-teal-950/60 dark:text-teal-300 font-semibold border border-teal-200 dark:border-teal-800">
                {data.associated_symptoms.length} syndromic pairs
              </span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-3">
              Captures clinically significant combinations and co-occurring symptom pairs that affect triage urgency.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {data.associated_symptoms.length > 0 ? (
                data.associated_symptoms.map((assoc, idx) => (
                  <div
                    key={idx}
                    className="flex items-center space-x-2 p-2.5 rounded-xl bg-teal-50/70 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-900 text-xs font-medium text-teal-900 dark:text-teal-200"
                  >
                    <Network className="h-4 w-4 text-teal-600 dark:text-teal-400 shrink-0" />
                    <span>{assoc}</span>
                  </div>
                ))
              ) : (
                <div className="p-3 text-xs text-slate-400 italic col-span-2">
                  No multi-symptom clusters detected (single isolated symptom or none reported).
                </div>
              )}
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 dark:text-slate-400">
            Syndromic clusters feed directly into Stage 2 (Disease Classifier) &amp; Stage 4 (Urgency Assessment).
          </div>
        </div>
      </div>
    </div>
  );
};

