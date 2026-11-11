"""Natural Language Generation (NLG) Module for Clinical Triage Summarization.

Implements Unit 4 NLP Syllabus concepts:
- Architecture of NLG Systems:
  1. Content Planning (Clinical determination: salience, pertinent negatives, urgency)
  2. Sentence Planning (Discourse aggregation, referring expressions, lexical choice)
  3. Surface Realization (Generating cohesive, grammatically sound clinical handoff notes in standard SBAR format)
"""

from typing import Dict, Any, List, Optional
from .schemas import SBARSummary

class ClinicalNLGGenerator:
    """Natural Language Generation engine synthesizing structured clinical findings into SBAR format."""

    def __init__(self):
        pass

    def generate_sbar(
        self,
        symptoms: List[str],
        negated_symptoms: List[str],
        uncertain_symptoms: List[str],
        body_location: List[str],
        duration_onset: Dict[str, str],
        severity: Dict[str, str],
        associated_symptoms: List[str],
        triage_prediction: Optional[Dict[str, Any]] = None
    ) -> SBARSummary:
        """Execute the 3-stage NLG pipeline to generate an SBAR handover note."""
        
        # ----------------------------------------------------
        # Stage 1: Content Planning
        # ----------------------------------------------------
        primary_symptoms = symptoms[:3] if symptoms else ["Undetermined clinical discomfort"]
        known_durations = [f"{s} ({d})" for s, d in duration_onset.items() if d and d != "unknown"]
        high_severity_items = [s for s, sev in severity.items() if sev in ("severe", "moderate")]
        
        dept = "General Medicine"
        urgency = "Standard"
        if triage_prediction:
            dept = triage_prediction.get("recommended_department", dept)
            urgency = triage_prediction.get("urgency_category", urgency)

        # ----------------------------------------------------
        # Stage 2: Sentence Planning & Lexical Selection
        # ----------------------------------------------------
        # Situation: Acute presenting complaint
        if symptoms:
            sym_clause = ", ".join(primary_symptoms)
            loc_clause = f" localized to the {', '.join(body_location)}" if body_location else ""
            situation_text = f"Patient presents for clinical triage with primary complaint of {sym_clause}{loc_clause}."
        else:
            situation_text = "Patient presents requesting clinical evaluation with non-specific symptom presentation."

        # Background: Chronological onset and anatomical history
        bg_elements = []
        if known_durations:
            bg_elements.append(f"Timeline indicates symptom manifestation: {'; '.join(known_durations)}.")
        else:
            bg_elements.append("Exact onset duration remains unspecified by narrative.")

        if associated_symptoms:
            bg_elements.append(f"Syndromic presentation exhibits co-occurrence: {'; '.join(associated_symptoms)}.")
        background_text = " ".join(bg_elements)

        # Assessment: Severity profile, uncertainty, and pertinent negatives
        assess_elements = []
        if high_severity_items:
            assess_elements.append(f"Elevated symptom intensity reported for: {', '.join(high_severity_items)}.")
        
        if negated_symptoms:
            assess_elements.append(f"Pertinent negatives confirmed: Patient explicitly denies {', '.join(negated_symptoms)}.")
            
        if uncertain_symptoms:
            assess_elements.append(f"Subjective uncertainty noted regarding {', '.join(uncertain_symptoms)} (requires clinical verification).")

        if not assess_elements:
            assess_elements.append("No critical red flags or confirmed high-severity markers identified.")
        assessment_text = " ".join(assess_elements)

        # Recommendation: Triage routing & safety directives
        rec_elements = [
            f"Recommended Specialty Route: {dept} (Triage Priority: {urgency.upper()})."
        ]
        if urgency.lower() in ("high", "emergency", "urgent"):
            rec_elements.append("Direct physician evaluation advised without delay due to acute symptom combination.")
        else:
            rec_elements.append("Proceed with standardized intake and targeted diagnostic assessment.")
        recommendation_text = " ".join(rec_elements)

        # ----------------------------------------------------
        # Stage 3: Surface Realization (Formatting SBAR Note)
        # ----------------------------------------------------
        formatted_note = (
            f"CLINICAL TRIAGE SBAR HANDOVER NOTE\n"
            f"=====================================\n"
            f"[S - SITUATION]:\n{situation_text}\n\n"
            f"[B - BACKGROUND]:\n{background_text}\n\n"
            f"[A - ASSESSMENT]:\n{assessment_text}\n\n"
            f"[R - RECOMMENDATION]:\n{recommendation_text}"
        )

        return SBARSummary(
            situation=situation_text,
            background=background_text,
            assessment=assessment_text,
            recommendation=recommendation_text,
            formatted_note=formatted_note
        )

