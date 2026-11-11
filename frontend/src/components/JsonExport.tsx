import React, { useState } from 'react';
import { ClinicalStructuredRepresentation } from '../types/clinical';
import { Code2, Copy, Check, Download, FileJson } from 'lucide-react';

interface JsonExportProps {
  data: ClinicalStructuredRepresentation;
}

export const JsonExport: React.FC<JsonExportProps> = ({ data }) => {
  const [copied, setCopied] = useState(false);
  const [format, setFormat] = useState<'minimal' | 'full'>('minimal');

  // Exact target schema representation requested in the user prompt & design.md
  const minimalSchema = {
    symptoms: data.symptoms,
    body_location: data.body_location,
    duration_onset: data.duration_onset,
    severity: data.severity,
    associated_symptoms: data.associated_symptoms
  };

  const fullSchema = {
    ...minimalSchema,
    preserved_attributes: {
      negated_symptoms: data.negated_symptoms,
      uncertain_symptoms: data.uncertain_symptoms
    },
    clinical_summary: data.clinical_summary,
    downstream_readiness: data.downstream_readiness,
    entities_audit_trail: data.entities
  };

  const jsonString = JSON.stringify(format === 'minimal' ? minimalSchema : fullSchema, null, 2);

  const handleCopy = () => {
    navigator.clipboard.writeText(jsonString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `clinical_extraction_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-800 p-5 shadow-lg text-slate-100 overflow-hidden">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 mb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Code2 className="h-4 w-4 text-sky-400" />
          <h3 className="text-sm font-bold text-white">
            Structured Representation JSON Output
          </h3>
          <span className="text-[10px] px-2 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800 font-mono">
            {format === 'minimal' ? 'Design Target Schema' : 'Extended Clinical Audit'}
          </span>
        </div>

        <div className="flex items-center space-x-2">
          <div className="bg-slate-800 p-0.5 rounded-lg border border-slate-700 flex text-xs">
            <button
              onClick={() => setFormat('minimal')}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                format === 'minimal'
                  ? 'bg-sky-600 text-white shadow-xs'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              5 Labels Target Schema
            </button>
            <button
              onClick={() => setFormat('full')}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors ${
                format === 'full'
                  ? 'bg-sky-600 text-white shadow-xs'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Full Clinical Audit
            </button>
          </div>

          <button
            onClick={handleCopy}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 hover:text-white transition-colors"
            title="Copy to clipboard"
          >
            {copied ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
          </button>

          <button
            onClick={handleDownload}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 hover:text-white transition-colors"
            title="Download JSON"
          >
            <Download className="h-4 w-4" />
          </button>
        </div>
      </div>

      <pre className="font-mono text-xs text-sky-300/90 bg-slate-950/80 p-4 rounded-xl border border-slate-800/80 overflow-x-auto max-h-96 leading-relaxed selection:bg-sky-900 selection:text-white">
        <code>{jsonString}</code>
      </pre>

      <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400">
        <span>Ready for downstream consumption by Stage 2, Stage 3, and Stage 4 models</span>
        <span className="font-mono">{jsonString.length} bytes</span>
      </div>
    </div>
  );
};

