from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class AnnotatedSpan(BaseModel):
    start: int
    end: int
    text: str
    label: str  # SYMPTOMS, BODY_LOCATION, DURATION_ONSET, SEVERITY, NEGATION_CUE, UNCERTAINTY_CUE
    color: Optional[str] = None
    detail: Optional[str] = None

class SymptomEntity(BaseModel):
    id: str
    name: str
    raw_span: str
    start_char: int
    end_char: int
    body_location: str = "unknown"
    severity: str = "unknown"  # mild, moderate, severe, unknown
    duration_onset: str = "unknown"  # e.g. "3 days", "since this morning", "unknown"
    assertion: str = "affirmed"  # "affirmed" | "negated"
    certainty: str = "confirmed"  # "confirmed" | "uncertain"
    negation_cue: Optional[str] = None
    uncertainty_cue: Optional[str] = None

# -------------------------------------------------------------
# NLP Syllabus Integration Models (Units 2, 3, 4)
# -------------------------------------------------------------

class SpellingCorrection(BaseModel):
    original: str
    corrected: str
    edit_distance: int
    algorithm: str = "Levenshtein Matrix Dynamic Programming (Unit 2)"
    explanation: str

class POSToken(BaseModel):
    token: str
    lemma: str
    pos: str
    tag_desc: str
    dep: str
    head: str

class SyntacticChunk(BaseModel):
    chunk_text: str
    phrase_type: str
    rule: str

class ReferenceResolution(BaseModel):
    pronoun: str
    resolved_to: str
    antecedent_span: str
    distance_tokens: int
    mechanism: str = "Discourse Recency Salience (Hobbs-inspired, Unit 3)"

class SBARSummary(BaseModel):
    situation: str
    background: str
    assessment: str
    recommendation: str
    formatted_note: str

# -------------------------------------------------------------
# Complete Clinical Output Representation
# -------------------------------------------------------------

class ClinicalStructuredRepresentation(BaseModel):
    symptoms: List[str] = Field(default_factory=list, description="Affirmed clinical symptoms")
    negated_symptoms: List[str] = Field(default_factory=list, description="Explicitly negated symptoms, e.g. 'no fever'")
    uncertain_symptoms: List[str] = Field(default_factory=list, description="Uncertain or hypothetical symptoms, e.g. 'possibly dizzy'")
    body_location: List[str] = Field(default_factory=list, description="Identified anatomical body locations")
    duration_onset: Dict[str, str] = Field(default_factory=dict, description="Mapped duration and onset per symptom")
    severity: Dict[str, str] = Field(default_factory=dict, description="Mapped severity level per symptom")
    associated_symptoms: List[str] = Field(default_factory=list, description="Clinical symptom combinations and co-occurrences")
    
    # Detailed entity records and visual spans for the triage interface
    entities: List[SymptomEntity] = Field(default_factory=list)
    spans: List[AnnotatedSpan] = Field(default_factory=list)
    clinical_summary: str = ""
    downstream_readiness: Dict[str, Any] = Field(default_factory=dict)
    triage_prediction: Optional[Dict[str, Any]] = None

    # NLP Course Syllabus Additions
    normalized_text: Optional[str] = None
    spelling_corrections: List[SpellingCorrection] = Field(default_factory=list)
    pos_tags: List[POSToken] = Field(default_factory=list)
    syntax_chunks: List[SyntacticChunk] = Field(default_factory=list)
    reference_resolutions: List[ReferenceResolution] = Field(default_factory=list)
    sbar_note: Optional[SBARSummary] = None

class ExtractRequest(BaseModel):
    text: str
    confidence_threshold: float = 0.5
