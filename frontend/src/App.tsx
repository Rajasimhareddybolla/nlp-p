import { useState } from 'react';
import { ClinicalStructuredRepresentation } from './types/clinical';
import { 
  Activity, 
  Copy, 
  Check, 
  ArrowRight, 
  Sparkles, 
  Stethoscope, 
  Building2, 
  AlertCircle,
  MapPin,
  Clock,
  Flame,
  CheckCircle2,
  Ban,
  HelpCircle,
  Network,
  BookOpen,
  FileText,
  SpellCheck,
  GitBranch,
  Layers,
  ChevronDown,
  ChevronUp,
  Cpu,
  ShieldAlert,
  Terminal,
  ArrowDown
} from 'lucide-react';

const SAMPLES = [
  {
    id: "sample-neuro",
    label: "Benchmark (Neuro)",
    desc: "Severe headache + nausea + acute blurred vision",
    text: "I've had a severe headache for three days, and since this morning I've been experiencing nausea and blurred vision."
  },
  {
    id: "sample-cardio",
    label: "Cardiology (NegEx)",
    desc: "Substernal chest pain with explicit negative findings",
    text: "Patient presents with severe substernal chest pain for 2 hours. Denies fever, no shortness of breath, and no cough. Possibly experiencing dizziness."
  },
  {
    id: "sample-spellcheck",
    label: "Spellcheck DP (Unit 2)",
    desc: "Levenshtein edit distance correcting medical typos",
    text: "I have sever headeche and nauesa for 2 days. Feeling dizzines and blury vision since morning. Denies feever."
  },
  {
    id: "sample-anaphora",
    label: "Anaphora Discourse (Unit 3)",
    desc: "Pronoun 'It' resolved across sentence boundaries",
    text: "Patient reports severe chest pain. It started three hours ago after climbing stairs. It is accompanied by shortness of breath."
  },
  {
    id: "sample-ortho",
    label: "Orthopedics (Wrist)",
    desc: "Joint pain with localized trauma & fall onset",
    text: "Severe pain in my left wrist with swelling after a fall 2 hours ago. No numbness, denies tingling."
  }
];

export function App() {
  const [inputText, setInputText] = useState(SAMPLES[0].text);
  const [result, setResult] = useState<ClinicalStructuredRepresentation | null>(null);
  const [loading, setLoading] = useState(false);
  const [copiedJson, setCopiedJson] = useState(false);
  const [copiedNote, setCopiedNote] = useState(false);
  const [nlpSubTab, setNlpSubTab] = useState<'spell' | 'pos' | 'anaphora'>('spell');
  const [showJsonRaw, setShowJsonRaw] = useState(false);

  const handleExtract = async (textToExtract = inputText) => {
    if (!textToExtract.trim()) return;
    setLoading(true);

    try {
      const res = await fetch('/api/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textToExtract })
      });

      if (!res.ok) throw new Error('Extraction failed');
      const data: ClinicalStructuredRepresentation = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const clean5FieldsJson = result ? {
    symptoms: result.symptoms,
    body_location: result.body_location,
    duration_onset: result.duration_onset,
    severity: result.severity,
    associated_symptoms: result.associated_symptoms
  } : null;

  const handleCopyJson = () => {
    if (!clean5FieldsJson) return;
    navigator.clipboard.writeText(JSON.stringify(clean5FieldsJson, null, 2));
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 2000);
  };

  const handleCopyNote = () => {
    if (!result?.sbar_note?.formatted_note) return;
    navigator.clipboard.writeText(result.sbar_note.formatted_note);
    setCopiedNote(true);
    setTimeout(() => setCopiedNote(false), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-50/80 text-slate-900 antialiased py-6 px-4 sm:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        
        {/* Top Header */}
        <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-sky-600 flex items-center justify-center text-white shadow-xs">
              <Activity className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-extrabold text-slate-900 tracking-tight">
                  Clinical Triage NLP Pipeline
                </h1>
                <span className="text-[10px] font-bold tracking-wide uppercase px-2 py-0.5 rounded-full bg-sky-100 text-sky-800 border border-sky-200">
                  Course: 23CS7PENLP
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Sequential End-to-End Pipeline: Raw Text &rarr; NLP Grounding &rarr; 5 Target Fields &rarr; Laya Decision &rarr; SBAR Report
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-white text-slate-700 border border-slate-200 shadow-2xs flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              Laya System 1 Active
            </span>
          </div>
        </header>

        {/* Visual Pipeline Stage Indicator */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-center text-xs font-medium">
          <div className="p-2 rounded-lg bg-sky-600 text-white shadow-xs">
            <p className="text-[10px] uppercase font-bold opacity-80">Stage 1</p>
            <p className="font-semibold truncate">Patient Input</p>
          </div>
          <div className={`p-2 rounded-lg border transition-colors ${result ? 'bg-indigo-50 border-indigo-200 text-indigo-900' : 'bg-white border-slate-200 text-slate-400'}`}>
            <p className="text-[10px] uppercase font-bold opacity-80">Stage 2</p>
            <p className="font-semibold truncate">NLP Grounding</p>
          </div>
          <div className={`p-2 rounded-lg border transition-colors ${result ? 'bg-emerald-50 border-emerald-300 text-emerald-950 font-bold ring-1 ring-emerald-400/30' : 'bg-white border-slate-200 text-slate-400'}`}>
            <p className="text-[10px] uppercase font-bold opacity-80">Stage 3 (Core)</p>
            <p className="font-semibold truncate">5 Target Labels</p>
          </div>
          <div className={`p-2 rounded-lg border transition-colors ${result ? 'bg-amber-50 border-amber-200 text-amber-900' : 'bg-white border-slate-200 text-slate-400'}`}>
            <p className="text-[10px] uppercase font-bold opacity-80">Stage 4</p>
            <p className="font-semibold truncate">Laya Triage</p>
          </div>
          <div className={`col-span-2 sm:col-span-1 p-2 rounded-lg border transition-colors ${result ? 'bg-teal-50 border-teal-200 text-teal-900' : 'bg-white border-slate-200 text-slate-400'}`}>
            <p className="text-[10px] uppercase font-bold opacity-80">Stage 5</p>
            <p className="font-semibold truncate">SBAR Handover</p>
          </div>
        </div>

        {/* ========================================================================= */}
        {/* STAGE 1: PATIENT INPUT NARRATIVE                                         */}
        {/* ========================================================================= */}
        <section className="bg-white rounded-xl border border-slate-200/90 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="h-6 w-6 rounded-md bg-sky-600 text-white font-bold text-xs flex items-center justify-center">
                1
              </span>
              <div>
                <h2 className="text-sm font-bold text-slate-900">Stage 1: Patient Narrative Input</h2>
                <p className="text-[11px] text-slate-500">Unstructured free-text clinical description entered by patient or intake nurse</p>
              </div>
            </div>
            
            {/* Quick Presets */}
            <span className="hidden sm:inline-block text-[11px] font-medium text-slate-400">
              Try Preset Benchmark Cases:
            </span>
          </div>

          {/* Sample Preset Chips */}
          <div className="flex flex-wrap gap-1.5 pt-1">
            {SAMPLES.map((sample) => (
              <button
                key={sample.id}
                onClick={() => {
                  setInputText(sample.text);
                  handleExtract(sample.text);
                }}
                className={`text-xs px-2.5 py-1.5 rounded-lg border font-medium transition-colors cursor-pointer text-left ${
                  inputText === sample.text
                    ? 'bg-sky-50 border-sky-300 text-sky-800 ring-1 ring-sky-300/40'
                    : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700'
                }`}
              >
                <span className="font-bold">{sample.label}</span>
              </button>
            ))}
          </div>

          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={3}
            placeholder="Enter patient symptoms narrative..."
            className="w-full rounded-lg border border-slate-300 p-3 text-sm focus:border-sky-500 focus:outline-hidden focus:ring-2 focus:ring-sky-500/20 font-sans leading-relaxed"
          />

          <div className="flex items-center justify-between pt-1">
            <span className="text-[11px] text-slate-400 font-mono">
              {inputText.trim().split(/\s+/).filter(Boolean).length} words • {inputText.length} chars
            </span>
            <button
              onClick={() => handleExtract(inputText)}
              disabled={loading || !inputText.trim()}
              className="px-5 py-2.5 rounded-lg bg-sky-600 hover:bg-sky-700 text-white text-xs font-bold flex items-center gap-2 shadow-xs disabled:opacity-50 transition-all cursor-pointer"
            >
              {loading ? (
                <>
                  <div className="h-3.5 w-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Executing Pipeline...</span>
                </>
              ) : (
                <>
                  <Sparkles className="h-3.5 w-3.5" />
                  <span>Execute Pipeline Sequentially</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </>
              )}
            </button>
          </div>
        </section>

        {/* Downward Pipeline Connector */}
        {result && (
          <div className="flex justify-center -my-2">
            <div className="h-6 w-0.5 bg-slate-300 flex items-center justify-center">
              <ArrowDown className="h-3.5 w-3.5 text-slate-400 bg-slate-50 p-0.5 rounded-full" />
            </div>
          </div>
        )}

        {result && (
          <div className="space-y-6">

            {/* ========================================================================= */}
            {/* STAGE 2: LINGUISTIC & NLP PREPROCESSING (UNITS 2 & 3)                    */}
            {/* ========================================================================= */}
            <section className="bg-white rounded-xl border border-indigo-200/80 p-5 shadow-xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-indigo-100">
                <div className="flex items-center gap-2">
                  <span className="h-6 w-6 rounded-md bg-indigo-600 text-white font-bold text-xs flex items-center justify-center">
                    2
                  </span>
                  <div>
                    <h2 className="text-sm font-bold text-slate-900">
                      Stage 2: Linguistic NLP Grounding &amp; Normalization
                    </h2>
                    <p className="text-[11px] text-slate-500">
                      Syllabus Units 2 &amp; 3: Levenshtein DP Spellcheck, Context-Free Grammar (CFG) Parsing, &amp; Anaphora Resolution
                    </p>
                  </div>
                </div>
                <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 border border-indigo-200">
                  Pre-Extraction Stage
                </span>
              </div>

              {/* Sub-tabs for Stage 2 details */}
              <div className="flex items-center gap-2 pt-1">
                <button
                  onClick={() => setNlpSubTab('spell')}
                  className={`px-3 py-1 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                    nlpSubTab === 'spell'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  <SpellCheck className="h-3.5 w-3.5" />
                  1. Levenshtein Spellcheck ({result.spelling_corrections?.length || 0})
                </button>

                <button
                  onClick={() => setNlpSubTab('pos')}
                  className={`px-3 py-1 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                    nlpSubTab === 'pos'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  <Layers className="h-3.5 w-3.5" />
                  2. POS &amp; CFG Constituents
                </button>

                <button
                  onClick={() => setNlpSubTab('anaphora')}
                  className={`px-3 py-1 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                    nlpSubTab === 'anaphora'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  <GitBranch className="h-3.5 w-3.5" />
                  3. Discourse Anaphora ({result.reference_resolutions?.length || 0})
                </button>
              </div>

              {/* Sub-tab 1: Spellcheck */}
              {nlpSubTab === 'spell' && (
                <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-700">Dynamic Programming Matrix Error Correction:</span>
                    <span className="text-slate-500 font-mono text-[11px]">
                      {result.spelling_corrections && result.spelling_corrections.length > 0 
                        ? `${result.spelling_corrections.length} typos normalized before extraction`
                        : '0 typos (text is clean)'}
                    </span>
                  </div>

                  {result.spelling_corrections && result.spelling_corrections.length > 0 ? (
                    <div className="space-y-1.5">
                      {result.spelling_corrections.map((sc, idx) => (
                        <div key={idx} className="flex items-center justify-between p-2 rounded-md bg-white border border-rose-200 text-xs">
                          <div className="flex items-center gap-2">
                            <span className="line-through text-rose-600 font-mono font-bold">"{sc.original}"</span>
                            <ArrowRight className="h-3 w-3 text-slate-400" />
                            <span className="text-emerald-700 font-mono font-bold bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
                              "{sc.corrected}"
                            </span>
                            <span className="text-[11px] text-slate-500">({sc.explanation})</span>
                          </div>
                          <span className="font-mono text-[10px] font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded">
                            Edit Distance: {sc.edit_distance}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-500 italic">
                      No typos detected. All tokens recognized by clinical lexicon &amp; English word net.
                    </p>
                  )}
                </div>
              )}

              {/* Sub-tab 2: POS Tagging & CFG */}
              {nlpSubTab === 'pos' && (
                <div className="space-y-3">
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                    <span className="text-xs font-bold text-slate-700">Penn Treebank Part-of-Speech Tokens:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {result.pos_tags?.map((pt, idx) => {
                        const isNoun = pt.pos.startsWith('NN');
                        const isAdj = pt.pos.startsWith('JJ');
                        const isVerb = pt.pos.startsWith('VB');
                        const isPrep = pt.pos === 'IN' || pt.pos === 'CD';

                        const color = isNoun 
                          ? 'bg-emerald-100 text-emerald-900 border-emerald-300' 
                          : isAdj 
                          ? 'bg-amber-100 text-amber-900 border-amber-300' 
                          : isVerb 
                          ? 'bg-purple-100 text-purple-900 border-purple-300' 
                          : isPrep 
                          ? 'bg-sky-100 text-sky-900 border-sky-300' 
                          : 'bg-white text-slate-700 border-slate-300';

                        return (
                          <div key={idx} className={`px-2 py-0.5 rounded border text-[11px] flex items-center gap-1 ${color}`}>
                            <span className="font-medium">{pt.token}</span>
                            <span className="text-[9px] font-mono opacity-80 font-bold uppercase">{pt.pos}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {result.syntax_chunks && result.syntax_chunks.length > 0 && (
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5">
                      <span className="text-xs font-bold text-slate-700">CFG Syntactic Constituents (NP &amp; PP Rules):</span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                        {result.syntax_chunks.slice(0, 6).map((c, idx) => (
                          <div key={idx} className="p-2 rounded bg-white border border-slate-200 text-[11px] flex justify-between items-center">
                            <span className="font-mono font-semibold text-slate-800">"{c.chunk_text}"</span>
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 font-mono text-slate-600">{c.phrase_type.split(' ')[0]}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Sub-tab 3: Discourse Anaphora */}
              {nlpSubTab === 'anaphora' && (
                <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-700">Hobbs-Inspired Cross-Sentence Pronominal Anaphora:</span>
                    <span className="text-slate-500 font-mono text-[11px]">
                      {result.reference_resolutions?.length || 0} pronoun referents resolved
                    </span>
                  </div>

                  {result.reference_resolutions && result.reference_resolutions.length > 0 ? (
                    <div className="space-y-1.5">
                      {result.reference_resolutions.map((rr, idx) => (
                        <div key={idx} className="p-2.5 rounded-md bg-white border border-purple-200 text-xs flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span className="font-mono font-bold text-purple-900 bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                              Pronoun "{rr.pronoun}"
                            </span>
                            <ArrowRight className="h-3 w-3 text-purple-500" />
                            <span className="font-semibold text-slate-900">
                              Bound to antecedent: "{rr.resolved_to}"
                            </span>
                          </div>
                          <span className="text-[10px] text-purple-700 font-mono">
                            Dist: {rr.distance_tokens} tokens
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-500 italic">
                      No ambiguous third-person pronouns requiring cross-sentence discourse resolution in this narrative.
                    </p>
                  )}
                </div>
              )}
            </section>

            {/* Downward Pipeline Connector */}
            <div className="flex justify-center -my-2">
              <div className="h-6 w-0.5 bg-slate-300 flex items-center justify-center">
                <ArrowDown className="h-3.5 w-3.5 text-slate-400 bg-slate-50 p-0.5 rounded-full" />
              </div>
            </div>

            {/* ========================================================================= */}
            {/* STAGE 3: THE 5 EXTRACTED CLINICAL TARGET FIELDS (CORE OUTPUT)             */}
            {/* ========================================================================= */}
            <section className="bg-white rounded-xl border-2 border-emerald-500/80 p-5 shadow-sm space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <span className="h-6 w-6 rounded-md bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                    3
                  </span>
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="text-base font-extrabold text-slate-900 tracking-tight">
                        Stage 3: The 5 Structured Clinical Target Fields
                      </h2>
                      <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 border border-emerald-300">
                        Primary System Output
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500">
                      Strict attribute binding without modifier hallucination • Negation &amp; Uncertainty preserved
                    </p>
                  </div>
                </div>

                <button
                  onClick={handleCopyJson}
                  className="self-start sm:self-auto flex items-center gap-1.5 text-xs text-emerald-800 bg-emerald-50 hover:bg-emerald-100 px-3 py-1.5 rounded-lg border border-emerald-300 font-semibold transition-colors cursor-pointer"
                >
                  {copiedJson ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5" />}
                  <span>{copiedJson ? 'Copied 5 Fields' : 'Copy 5 Fields JSON'}</span>
                </button>
              </div>

              {/* Grid of the 5 Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                {/* 1. SYMPTOMS */}
                <div className="p-4 rounded-xl bg-slate-50/90 border border-slate-200 space-y-2.5">
                  <div className="flex items-center justify-between pb-1 border-b border-slate-200/60">
                    <span className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                      <span className="h-5 w-5 rounded-full bg-emerald-600 text-white text-[10px] flex items-center justify-center font-bold">1</span>
                      Symptoms
                    </span>
                    <span className="text-[11px] font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 font-bold">
                      {result.symptoms.length} confirmed
                    </span>
                  </div>

                  {/* Confirmed */}
                  <div className="flex flex-wrap gap-1.5">
                    {result.symptoms.length > 0 ? (
                      result.symptoms.map((s, idx) => (
                        <span key={idx} className="px-3 py-1 rounded-lg bg-emerald-50 text-emerald-900 text-xs font-bold border border-emerald-300 shadow-2xs">
                          {s}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-slate-400 italic">None confirmed</span>
                    )}
                  </div>

                  {/* Negated (Absent) */}
                  {result.negated_symptoms && result.negated_symptoms.length > 0 && (
                    <div className="pt-2 border-t border-slate-200/80 flex items-center gap-1.5 text-xs text-rose-700 bg-rose-50/60 p-2 rounded-md border border-rose-200">
                      <Ban className="h-3.5 w-3.5 text-rose-500 shrink-0" />
                      <span className="font-bold text-[10px] uppercase">Pertinent Negatives (Absent):</span>
                      <span className="line-through font-semibold">{result.negated_symptoms.join(', ')}</span>
                    </div>
                  )}

                  {/* Uncertain */}
                  {result.uncertain_symptoms && result.uncertain_symptoms.length > 0 && (
                    <div className="flex items-center gap-1.5 text-xs text-amber-800 bg-amber-50/60 p-2 rounded-md border border-amber-200">
                      <HelpCircle className="h-3.5 w-3.5 text-amber-500 shrink-0" />
                      <span className="font-bold text-[10px] uppercase">Uncertain / Hypothetical:</span>
                      <span className="font-semibold">{result.uncertain_symptoms.join(', ')}</span>
                    </div>
                  )}
                </div>

                {/* 2. BODY LOCATION */}
                <div className="p-4 rounded-xl bg-slate-50/90 border border-slate-200 space-y-2.5">
                  <div className="flex items-center justify-between pb-1 border-b border-slate-200/60">
                    <span className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                      <span className="h-5 w-5 rounded-full bg-indigo-600 text-white text-[10px] flex items-center justify-center font-bold">2</span>
                      Body Location
                    </span>
                    <MapPin className="h-4 w-4 text-indigo-500" />
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {result.body_location.length > 0 ? (
                      result.body_location.map((loc, idx) => (
                        <span key={idx} className="px-3 py-1 rounded-lg bg-indigo-50 text-indigo-900 text-xs font-bold capitalize border border-indigo-200 shadow-2xs">
                          {loc}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-slate-400 italic">None specified</span>
                    )}
                  </div>
                  <p className="text-[10px] text-slate-400 italic">Anatomical regions mapped to direct hospital routing</p>
                </div>

                {/* 3. DURATION & ONSET */}
                <div className="p-4 rounded-xl bg-slate-50/90 border border-slate-200 space-y-2.5">
                  <div className="flex items-center justify-between pb-1 border-b border-slate-200/60">
                    <span className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                      <span className="h-5 w-5 rounded-full bg-purple-600 text-white text-[10px] flex items-center justify-center font-bold">3</span>
                      Duration &amp; Onset
                    </span>
                    <Clock className="h-4 w-4 text-purple-500" />
                  </div>
                  <div className="space-y-1.5">
                    {Object.entries(result.duration_onset).map(([sym, dur], idx) => (
                      <div key={idx} className="flex justify-between items-center text-xs p-1.5 rounded bg-white border border-slate-200/60">
                        <span className="text-slate-700 font-semibold capitalize">{sym}:</span>
                        <span className="font-mono text-purple-900 font-bold bg-purple-50 px-2 py-0.5 rounded border border-purple-200">
                          {dur}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 4. SEVERITY */}
                <div className="p-4 rounded-xl bg-slate-50/90 border border-slate-200 space-y-2.5">
                  <div className="flex items-center justify-between pb-1 border-b border-slate-200/60">
                    <span className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                      <span className="h-5 w-5 rounded-full bg-orange-600 text-white text-[10px] flex items-center justify-center font-bold">4</span>
                      Severity
                    </span>
                    <Flame className="h-4 w-4 text-orange-500" />
                  </div>
                  <div className="space-y-1.5">
                    {Object.entries(result.severity).map(([sym, sev], idx) => (
                      <div key={idx} className="flex justify-between items-center text-xs p-1.5 rounded bg-white border border-slate-200/60">
                        <span className="text-slate-700 font-semibold capitalize">{sym}:</span>
                        <span className={`font-mono text-xs px-2 py-0.5 rounded font-bold uppercase ${
                          sev === 'severe'
                            ? 'bg-rose-100 text-rose-900 border border-rose-300'
                            : sev === 'moderate'
                            ? 'bg-amber-100 text-amber-900 border border-amber-300'
                            : 'bg-slate-100 text-slate-600 border border-slate-200'
                        }`}>
                          {sev}
                        </span>
                      </div>
                    ))}
                  </div>
                  <p className="text-[10px] text-slate-400 italic">Notice: Severity is not invented; unstated findings remain "unknown"</p>
                </div>

                {/* 5. ASSOCIATED SYMPTOMS */}
                <div className="p-4 rounded-xl bg-slate-50/90 border border-slate-200 space-y-2.5 md:col-span-2">
                  <div className="flex items-center justify-between pb-1 border-b border-slate-200/60">
                    <span className="text-xs font-extrabold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                      <span className="h-5 w-5 rounded-full bg-teal-600 text-white text-[10px] flex items-center justify-center font-bold">5</span>
                      Associated Symptoms (Combinations)
                    </span>
                    <Network className="h-4 w-4 text-teal-600" />
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {result.associated_symptoms.length > 0 ? (
                      result.associated_symptoms.map((assoc, idx) => (
                        <span key={idx} className="px-3 py-1.5 rounded-lg bg-teal-50 border border-teal-300 text-teal-950 text-xs font-bold shadow-2xs">
                          {assoc}
                        </span>
                      ))
                    ) : (
                      <span className="text-xs text-slate-400 italic">No co-occurring symptom pairs</span>
                    )}
                  </div>
                  <p className="text-[10px] text-slate-400 italic">Syndromic pairs that alert emergency triage rules (e.g. headache with blurred vision)</p>
                </div>

              </div>
            </section>

            {/* Downward Pipeline Connector */}
            <div className="flex justify-center -my-2">
              <div className="h-6 w-0.5 bg-slate-300 flex items-center justify-center">
                <ArrowDown className="h-3.5 w-3.5 text-slate-400 bg-slate-50 p-0.5 rounded-full" />
              </div>
            </div>

            {/* ========================================================================= */}
            {/* STAGE 4: LAYA SYSTEM 1 TRIAGE DECISION LAYER                             */}
            {/* ========================================================================= */}
            {result.triage_prediction && (
              <section className="bg-white rounded-xl border border-amber-200 p-5 shadow-xs space-y-4">
                <div className="flex items-center justify-between pb-2 border-b border-amber-100">
                  <div className="flex items-center gap-2">
                    <span className="h-6 w-6 rounded-md bg-amber-600 text-white font-bold text-xs flex items-center justify-center">
                      4
                    </span>
                    <div>
                      <h2 className="text-sm font-bold text-slate-900">
                        Stage 4: Laya System 1 Triage &amp; Routing Decisions
                      </h2>
                      <p className="text-[11px] text-slate-500">
                        Non-autoregressive forward-pass classifier (<span className="font-mono">&lt;100ms latency</span>) evaluated on extracted syndrome
                      </p>
                    </div>
                  </div>
                  <span className="text-[10px] font-mono font-bold bg-amber-50 text-amber-900 border border-amber-200 px-2 py-0.5 rounded">
                    {result.triage_prediction.source}
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {/* Disease Domain */}
                  <div className="p-3.5 rounded-xl bg-sky-50/70 border border-sky-200 space-y-1.5">
                    <span className="text-[10px] font-bold text-sky-800 uppercase tracking-wider">
                      Predicted Clinical Domain
                    </span>
                    <p className="text-sm font-extrabold text-slate-900 leading-snug">
                      {result.triage_prediction.disease.name}
                    </p>
                    <div className="flex items-center justify-between text-[11px] text-sky-700 pt-1">
                      <span>Calibrated Confidence:</span>
                      <span className="font-mono font-bold">{result.triage_prediction.disease.confidence}%</span>
                    </div>
                    {/* Confidence bar */}
                    <div className="w-full bg-sky-200/60 rounded-full h-1.5 overflow-hidden">
                      <div 
                        className="bg-sky-600 h-1.5 rounded-full" 
                        style={{ width: `${Math.min(100, result.triage_prediction.disease.confidence)}%` }} 
                      />
                    </div>
                  </div>

                  {/* Department */}
                  <div className="p-3.5 rounded-xl bg-indigo-50/70 border border-indigo-200 space-y-1.5">
                    <span className="text-[10px] font-bold text-indigo-800 uppercase tracking-wider">
                      Recommended Specialty Route
                    </span>
                    <p className="text-sm font-extrabold text-slate-900 flex items-center gap-1.5 leading-snug">
                      <Building2 className="h-4 w-4 text-indigo-600 shrink-0" />
                      {result.triage_prediction.department.name}
                    </p>
                    <div className="flex items-center justify-between text-[11px] text-indigo-700 pt-1">
                      <span>Routing Confidence:</span>
                      <span className="font-mono font-bold">{result.triage_prediction.department.confidence}%</span>
                    </div>
                    <div className="w-full bg-indigo-200/60 rounded-full h-1.5 overflow-hidden">
                      <div 
                        className="bg-indigo-600 h-1.5 rounded-full" 
                        style={{ width: `${Math.min(100, result.triage_prediction.department.confidence)}%` }} 
                      />
                    </div>
                  </div>

                  {/* Urgency */}
                  <div className="p-3.5 rounded-xl bg-rose-50/70 border border-rose-200 space-y-1.5">
                    <span className="text-[10px] font-bold text-rose-800 uppercase tracking-wider">
                      Urgency &amp; Acuity Safety
                    </span>
                    <p className="text-sm font-extrabold text-rose-950 flex items-center gap-1.5 leading-snug">
                      <AlertCircle className="h-4 w-4 text-rose-600 shrink-0" />
                      {result.triage_prediction.urgency.level}
                    </p>
                    <div className="text-[11px] text-rose-700 pt-1 flex items-center gap-1">
                      <ShieldAlert className="h-3 w-3" />
                      <span>Decoupled safety check passed</span>
                    </div>
                    <p className="text-[10px] text-rose-600/80 italic">Acute red-flag combinations trigger elevated urgency independently of disease</p>
                  </div>
                </div>
              </section>
            )}

            {/* Downward Pipeline Connector */}
            <div className="flex justify-center -my-2">
              <div className="h-6 w-0.5 bg-slate-300 flex items-center justify-center">
                <ArrowDown className="h-3.5 w-3.5 text-slate-400 bg-slate-50 p-0.5 rounded-full" />
              </div>
            </div>

            {/* ========================================================================= */}
            {/* STAGE 5: CLINICAL SBAR HANDOVER NOTE (NLG PIPELINE - UNIT 4)             */}
            {/* ========================================================================= */}
            {result.sbar_note && (
              <section className="bg-white rounded-xl border border-teal-200 p-5 shadow-xs space-y-4">
                <div className="flex items-center justify-between pb-2 border-b border-teal-100">
                  <div className="flex items-center gap-2">
                    <span className="h-6 w-6 rounded-md bg-teal-600 text-white font-bold text-xs flex items-center justify-center">
                      5
                    </span>
                    <div>
                      <h2 className="text-sm font-bold text-slate-900">
                        Stage 5: Generated SBAR Clinical Handover Note
                      </h2>
                      <p className="text-[11px] text-slate-500">
                        Syllabus Unit 4 NLG Architecture: Content Determination &rarr; Sentence Aggregation &rarr; Surface Realization
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={handleCopyNote}
                    className="flex items-center gap-1.5 text-xs text-teal-800 bg-teal-50 hover:bg-teal-100 px-3 py-1.5 rounded-lg border border-teal-300 font-semibold transition-colors cursor-pointer"
                  >
                    {copiedNote ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5" />}
                    <span>{copiedNote ? 'Copied Note' : 'Copy Doctor Note'}</span>
                  </button>
                </div>

                {/* SBAR 4 Quadrants */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div className="p-3.5 rounded-lg bg-sky-50/70 border border-sky-100 space-y-1">
                    <span className="text-[11px] font-extrabold text-sky-900 uppercase tracking-wide">
                      [S - Situation] Presenting Complaint
                    </span>
                    <p className="text-xs text-slate-800 leading-relaxed font-sans">{result.sbar_note.situation}</p>
                  </div>

                  <div className="p-3.5 rounded-lg bg-indigo-50/70 border border-indigo-100 space-y-1">
                    <span className="text-[11px] font-extrabold text-indigo-900 uppercase tracking-wide">
                      [B - Background] Onset &amp; Timeline
                    </span>
                    <p className="text-xs text-slate-800 leading-relaxed font-sans">{result.sbar_note.background}</p>
                  </div>

                  <div className="p-3.5 rounded-lg bg-amber-50/70 border border-amber-100 space-y-1">
                    <span className="text-[11px] font-extrabold text-amber-900 uppercase tracking-wide">
                      [A - Assessment] Severity &amp; Pertinent Negatives
                    </span>
                    <p className="text-xs text-slate-800 leading-relaxed font-sans">{result.sbar_note.assessment}</p>
                  </div>

                  <div className="p-3.5 rounded-lg bg-emerald-50/70 border border-emerald-100 space-y-1">
                    <span className="text-[11px] font-extrabold text-emerald-900 uppercase tracking-wide">
                      [R - Recommendation] Triage Route &amp; Safety Priority
                    </span>
                    <p className="text-xs text-slate-800 leading-relaxed font-sans">{result.sbar_note.recommendation}</p>
                  </div>
                </div>
              </section>
            )}

            {/* ========================================================================= */}
            {/* OPTIONAL: RAW TARGET SCHEMA JSON EXPORT                                   */}
            {/* ========================================================================= */}
            {clean5FieldsJson && (
              <div className="bg-slate-900 rounded-xl overflow-hidden text-slate-100 shadow-xs">
                <button
                  onClick={() => setShowJsonRaw(!showJsonRaw)}
                  className="w-full flex items-center justify-between p-4 bg-slate-900 hover:bg-slate-800/80 transition-colors text-left cursor-pointer"
                >
                  <div className="flex items-center gap-2">
                    <Terminal className="h-4 w-4 text-sky-400" />
                    <span className="text-xs font-mono font-semibold text-sky-300">
                      Target Schema JSON Payload (Machine-Readable Contract)
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-[10px] text-slate-400 font-mono">Click to toggle raw JSON</span>
                    {showJsonRaw ? <ChevronUp className="h-4 w-4 text-slate-400" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
                  </div>
                </button>

                {showJsonRaw && (
                  <div className="p-4 border-t border-slate-800 space-y-2 bg-slate-950">
                    <div className="flex justify-end">
                      <button
                        onClick={handleCopyJson}
                        className="flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-1 rounded transition-colors cursor-pointer"
                      >
                        {copiedJson ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                        <span>{copiedJson ? 'Copied' : 'Copy JSON'}</span>
                      </button>
                    </div>
                    <pre className="text-xs font-mono text-sky-300/90 overflow-x-auto p-2 leading-relaxed">
                      <code>{JSON.stringify(clean5FieldsJson, null, 2)}</code>
                    </pre>
                  </div>
                )}
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}

export default App;
