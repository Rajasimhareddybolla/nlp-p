export interface AnnotatedSpan {
  start: number;
  end: number;
  text: string;
  label: string;
  color?: string;
  detail?: string;
}

export interface SymptomEntity {
  id: string;
  name: string;
  raw_span: string;
  start_char: number;
  end_char: number;
  body_location: string;
  severity: string;
  duration_onset: string;
  assertion: 'affirmed' | 'negated';
  certainty: 'confirmed' | 'uncertain';
  negation_cue?: string | null;
  uncertainty_cue?: string | null;
}

export interface TriagePrediction {
  source: string;
  disease: {
    name: string;
    confidence: number;
    probabilities?: Record<string, number>;
  };
  department: {
    name: string;
    confidence: number;
  };
  urgency: {
    level: string;
  };
}

export interface DownstreamReadiness {
  stage_1_extraction_complete: boolean;
  stage_2_disease_classification_ready: boolean;
  stage_3_department_routing_ready: boolean;
  stage_4_urgency_assessment_ready: boolean;
  red_flag_alert: boolean;
}

// NLP Syllabus Interfaces (Units 2, 3, 4)
export interface SpellingCorrection {
  original: string;
  corrected: string;
  edit_distance: number;
  algorithm: string;
  explanation: string;
}

export interface POSToken {
  token: string;
  lemma: string;
  pos: string;
  tag_desc: string;
  dep: string;
  head: string;
}

export interface SyntacticChunk {
  chunk_text: string;
  phrase_type: string;
  rule: string;
}

export interface ReferenceResolution {
  pronoun: string;
  resolved_to: string;
  antecedent_span: string;
  distance_tokens: number;
  mechanism: string;
}

export interface SBARSummary {
  situation: string;
  background: string;
  assessment: string;
  recommendation: string;
  formatted_note: string;
}

export interface ClinicalStructuredRepresentation {
  symptoms: string[];
  negated_symptoms: string[];
  uncertain_symptoms: string[];
  body_location: string[];
  duration_onset: Record<string, string>;
  severity: Record<string, string>;
  associated_symptoms: string[];
  entities: SymptomEntity[];
  spans?: AnnotatedSpan[];
  clinical_summary?: string;
  downstream_readiness?: DownstreamReadiness;
  triage_prediction?: TriagePrediction;
  normalized_text?: string;
  spelling_corrections?: SpellingCorrection[];
  pos_tags?: POSToken[];
  syntax_chunks?: SyntacticChunk[];
  reference_resolutions?: ReferenceResolution[];
  sbar_note?: SBARSummary;
}

export interface PresetCase {
  id: string;
  title: string;
  subtitle: string;
  text: string;
  category: string;
  key_highlights: string[];
}
