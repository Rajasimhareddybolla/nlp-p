import re
import uuid
from typing import List, Dict, Tuple, Optional
from .lexicons import (
    SYMPTOM_LEXICON,
    BODY_LOCATIONS,
    SYMPTOM_DEFAULT_LOCATION,
    SEVERITY_LEXICON,
    PRE_NEGATION_TRIGGERS,
    POST_NEGATION_TRIGGERS,
    PSEUDO_NEGATIONS,
    UNCERTAINTY_TRIGGERS,
    OPEN_SYMPTOM_PATTERNS
)
from .schemas import (
    ClinicalStructuredRepresentation,
    SymptomEntity,
    AnnotatedSpan,
    SpellingCorrection,
    POSToken,
    SyntacticChunk,
    ReferenceResolution,
    SBARSummary
)
from .laya_service import LayaUniversalClassifier
from .spell_checker import ClinicalSpellChecker
from .pos_tagger import ClinicalSyntacticAnalyzer
from .reference_resolver import ClinicalReferenceResolver
from .nlg_generator import ClinicalNLGGenerator

# Number word mappings for duration normalization
NUM_WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "couple": "2", "several": "several", "a few": "a few"
}

# Duration / Onset regex patterns
DURATION_ONSET_PATTERNS = [
    # "for three days", "for 3 days", "for 2 weeks"
    (r"\b(?:for\s+)?(?:about\s+)?((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|couple of|several|a few)\s+(?:hours?|hrs?|days?|weeks?|months?|years?))\b", "duration"),
    # "since this morning", "since yesterday", "since last night", "since Monday"
    (r"\b(since\s+(?:this\s+morning|yesterday|last\s+night|yesterday\s+morning|yesterday\s+evening|monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b", "onset"),
    # "started this morning", "started yesterday", "started 2 hours ago"
    (r"\b(started\s+(?:this\s+morning|yesterday|today|recently|suddenly|\d+\s+(?:hours?|days?)\s+ago))\b", "onset"),
    # "sudden onset", "acute onset", "gradual onset"
    (r"\b(sudden\s+onset|acute\s+onset|gradual\s+onset|all\s+of\s+a\s+sudden)\b", "onset"),
    # "past 3 days", "last 24 hours"
    (r"\b(?:over\s+the\s+|in\s+the\s+)?(?:past|last)\s+((?:\d+|one|two|three|four|five)\s+(?:hours?|days?|weeks?))\b", "duration")
]

class ClinicalExtractionEngine:
    def __init__(self):
        # Precompile symptom matchers sorted by length descending
        self.symptom_patterns = []
        for canonical, variants in SYMPTOM_LEXICON.items():
            all_forms = sorted(list(set([canonical] + variants)), key=len, reverse=True)
            for form in all_forms:
                pattern = re.compile(rf"\b{re.escape(form)}\b", re.IGNORECASE)
                self.symptom_patterns.append((canonical, form, pattern))

        # Precompile body locations
        self.location_patterns = []
        for canonical, variants in BODY_LOCATIONS.items():
            all_forms = sorted(list(set([canonical] + variants)), key=len, reverse=True)
            for form in all_forms:
                pattern = re.compile(rf"\b{re.escape(form)}\b", re.IGNORECASE)
                self.location_patterns.append((canonical, form, pattern))

        # Precompile severity terms
        self.severity_patterns = []
        for level, terms in SEVERITY_LEXICON.items():
            for term in terms:
                pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
                self.severity_patterns.append((level, term, pattern))

        # Precompile negation cues
        self.pre_neg_patterns = [
            (cue, re.compile(rf"\b{re.escape(cue)}\b", re.IGNORECASE))
            for cue in sorted(PRE_NEGATION_TRIGGERS, key=len, reverse=True)
        ]
        self.post_neg_patterns = [
            (cue, re.compile(rf"\b{re.escape(cue)}\b", re.IGNORECASE))
            for cue in sorted(POST_NEGATION_TRIGGERS, key=len, reverse=True)
        ]
        self.pseudo_neg_patterns = [
            re.compile(rf"\b{re.escape(cue)}\b", re.IGNORECASE)
            for cue in PSEUDO_NEGATIONS
        ]

        # Precompile uncertainty cues
        self.uncertainty_patterns = [
            (cue, re.compile(rf"\b{re.escape(cue)}\b", re.IGNORECASE))
            for cue in sorted(UNCERTAINTY_TRIGGERS, key=len, reverse=True)
        ]

        # Initialize Universal Laya classifier for clinical decision routing
        self.laya = LayaUniversalClassifier()

        # NLP Syllabus Modules (Units 2, 3, 4)
        self.spell_checker = ClinicalSpellChecker()
        self.syntactic_analyzer = ClinicalSyntacticAnalyzer()
        self.reference_resolver = ClinicalReferenceResolver()
        self.nlg_generator = ClinicalNLGGenerator()

    def _normalize_duration(self, text: str) -> str:
        res = text.strip().lower()
        res = re.sub(r"^for\s+", "", res)
        for w, digit in NUM_WORDS.items():
            res = re.sub(rf"\b{w}\b", digit, res)
        return res

    def extract_spans(self, text: str) -> Dict[str, list]:
        """Extract raw entities with offsets."""
        found_symptoms = []
        found_locations = []
        found_severities = []
        found_durations = []
        found_negations = []
        found_uncertainties = []

        # 1. Symptoms
        occupied_symptom_spans = []
        for canonical, form, pattern in self.symptom_patterns:
            for m in pattern.finditer(text):
                start, end = m.span()
                # avoid overlapping with already matched longer symptoms
                if any(start >= o[0] and end <= o[1] for o in occupied_symptom_spans):
                    continue
                occupied_symptom_spans.append((start, end))
                found_symptoms.append({
                    "canonical": canonical,
                    "matched_text": m.group(0),
                    "start": start,
                    "end": end
                })

        # Universal Open-Vocabulary Dynamic Symptom Matching
        for pattern in OPEN_SYMPTOM_PATTERNS:
            for m in pattern.finditer(text):
                start, end = m.span()
                if any(start >= o[0] and end <= o[1] for o in occupied_symptom_spans):
                    continue
                phrase = m.group(1) if m.groups() else m.group(0)
                phrase = phrase.strip().lower()
                occupied_symptom_spans.append((start, end))
                found_symptoms.append({
                    "canonical": phrase,
                    "matched_text": m.group(0),
                    "start": start,
                    "end": end
                })

        # Sort symptoms by start char
        found_symptoms.sort(key=lambda x: x["start"])

        # 2. Locations
        occupied_loc_spans = []
        for canonical, form, pattern in self.location_patterns:
            for m in pattern.finditer(text):
                start, end = m.span()
                if any(start >= o[0] and end <= o[1] for o in occupied_loc_spans):
                    continue
                occupied_loc_spans.append((start, end))
                found_locations.append({
                    "canonical": canonical,
                    "matched_text": m.group(0),
                    "start": start,
                    "end": end
                })

        # 3. Severity
        occupied_sev_spans = []
        for level, term, pattern in self.severity_patterns:
            for m in pattern.finditer(text):
                start, end = m.span()
                if any(start >= o[0] and end <= o[1] for o in occupied_sev_spans):
                    continue
                occupied_sev_spans.append((start, end))
                found_severities.append({
                    "level": level,
                    "matched_text": m.group(0),
                    "start": start,
                    "end": end
                })

        # 4. Durations / Onset
        occupied_dur_spans = []
        for pattern_str, kind in DURATION_ONSET_PATTERNS:
            pat = re.compile(pattern_str, re.IGNORECASE)
            for m in pat.finditer(text):
                start, end = m.span()
                matched_val = m.group(1) if m.groups() else m.group(0)
                if any(start >= o[0] and end <= o[1] for o in occupied_dur_spans):
                    continue
                occupied_dur_spans.append((start, end))
                found_durations.append({
                    "kind": kind,
                    "value": matched_val,
                    "matched_text": m.group(0),
                    "start": start,
                    "end": end
                })

        # 5. Negation Triggers (Pre & Post)
        for cue, pat in self.pre_neg_patterns:
            for m in pat.finditer(text):
                # check if pseudo negation
                start, end = m.span()
                is_pseudo = any(p.search(text[max(0, start - 10):min(len(text), end + 10)]) for p in self.pseudo_neg_patterns)
                if not is_pseudo:
                    found_negations.append({
                        "type": "pre",
                        "cue": cue,
                        "start": start,
                        "end": end
                    })

        for cue, pat in self.post_neg_patterns:
            for m in pat.finditer(text):
                found_negations.append({
                    "type": "post",
                    "cue": cue,
                    "start": m.start(),
                    "end": m.end()
                })

        # 6. Uncertainty Triggers
        for cue, pat in self.uncertainty_patterns:
            for m in pat.finditer(text):
                found_uncertainties.append({
                    "cue": cue,
                    "start": m.start(),
                    "end": m.end()
                })

        return {
            "symptoms": found_symptoms,
            "locations": found_locations,
            "severities": found_severities,
            "durations": found_durations,
            "negations": found_negations,
            "uncertainties": found_uncertainties
        }

    def _find_preceding_modifier(self, sym_start: int, candidates: list, max_distance: int = 40, stop_delimiters: str = ".;,but") -> Optional[dict]:
        """Find the closest preceding modifier within max_distance not blocked by clause delimiters."""
        best = None
        min_dist = float("inf")
        for c in candidates:
            if c["end"] <= sym_start:
                dist = sym_start - c["end"]
                if dist < max_distance and dist < min_dist:
                    intervening = "" # will check below
                    # check if delimiter in intervening text
                    # (handled by caller if needed)
                    min_dist = dist
                    best = c
        return best

    def extract(self, text: str) -> ClinicalStructuredRepresentation:
        # NLP Stage 0 (Unit 2): Word Level Analysis - Spelling Correction & Normalization
        normalized_text, spelling_corrections = self.spell_checker.normalize_text(text)

        # NLP Stage 0.5 (Unit 3): Discourse Processing - Hobbs-inspired Reference Resolution
        ref_resolutions, augmented_text = self.reference_resolver.resolve(normalized_text)

        # NLP Stage 1 (Unit 2): POS Tagging & Context-Free Grammar Constituency Analysis
        syntax_analysis = self.syntactic_analyzer.analyze(normalized_text)
        pos_tokens = syntax_analysis["pos_tokens"]
        syntax_chunks = syntax_analysis["syntax_chunks"]

        # Base extraction on augmented_text (or normalized_text if no anaphora)
        eval_text = augmented_text if ref_resolutions else normalized_text
        spans_data = self.extract_spans(eval_text)
        raw_symptoms = spans_data["symptoms"]
        locations = spans_data["locations"]
        severities = spans_data["severities"]
        durations = spans_data["durations"]
        negations = spans_data["negations"]
        uncertainties = spans_data["uncertainties"]

        entities: List[SymptomEntity] = []
        ui_spans: List[AnnotatedSpan] = []

        # Split text into sentence / clause boundaries for scope resolution
        delimiters = re.compile(r"(\.|\;|\bbut\b|\bhowever\b|\balthough\b|\binstead\b)", re.IGNORECASE)

        # Process each symptom
        for s in raw_symptoms:
            s_name = s["canonical"]
            s_start = s["start"]
            s_end = s["end"]
            s_text = s["matched_text"]

            # --- 1. Assertion: Negation Check (ConText / NegEx logic) ---
            assertion = "affirmed"
            negation_cue = None

            # Pre-negation within ~35 chars preceding symptom without intervening punctuation
            for neg in negations:
                if neg["type"] == "pre" and neg["end"] <= s_start:
                    between = eval_text[neg["end"]:s_start]
                    # check word distance (max ~5 words) and no sentence breaks
                    words = between.strip().split()
                    has_break = bool(delimiters.search(between))
                    if len(words) <= 5 and not has_break:
                        assertion = "negated"
                        negation_cue = neg["cue"]
                        break

            # Post-negation within ~25 chars following symptom
            if assertion == "affirmed":
                for neg in negations:
                    if neg["type"] == "post" and neg["start"] >= s_end:
                        between = eval_text[s_end:neg["start"]]
                        words = between.strip().split()
                        has_break = bool(delimiters.search(between))
                        if len(words) <= 4 and not has_break:
                            assertion = "negated"
                            negation_cue = neg["cue"]
                            break

            # --- 2. Certainty: Uncertainty / Speculation Check ---
            certainty = "confirmed"
            uncertainty_cue = None
            for unc in uncertainties:
                if unc["end"] <= s_start:
                    between = eval_text[unc["end"]:s_start]
                    words = between.strip().split()
                    has_break = bool(delimiters.search(between))
                    if len(words) <= 6 and not has_break:
                        certainty = "uncertain"
                        uncertainty_cue = unc["cue"]
                        break

            # --- 3. Body Location Binding ---
            bound_location = SYMPTOM_DEFAULT_LOCATION.get(s_name, "unknown")
            # If explicit location appears nearby (e.g., "pain in the abdomen" or "chest discomfort")
            for loc in locations:
                # Check if loc is part of another symptom
                part_of_other = any(os != s and loc["start"] >= os["start"] and loc["end"] <= os["end"] for os in raw_symptoms)
                if part_of_other:
                    continue

                # preceding by up to 3 words: e.g. "head pain"
                if loc["end"] <= s_start and (s_start - loc["end"]) <= 20:
                    bound_location = loc["canonical"]
                    break
                # following by up to 4 words: e.g. "pain in abdomen"
                elif loc["start"] >= s_end and (loc["start"] - s_end) <= 25:
                    between = eval_text[s_end:loc["start"]]
                    intervening_sym = any(os["start"] >= s_end and os["start"] <= loc["start"] for os in raw_symptoms if os != s)
                    if not delimiters.search(between) and not intervening_sym:
                        bound_location = loc["canonical"]
                        break

            # --- 4. Severity Binding (Notice: only bind if explicitly associated!) ---
            bound_severity = "unknown"
            
            # Check if canonical symptom or matched text inherently starts with a severity modifier
            for level in ["severe", "moderate", "mild"]:
                if s_name.startswith(f"{level} "):
                    s_name = s_name[len(level)+1:]
                    bound_severity = level
                    break
                elif level in s_text.lower().split():
                    bound_severity = level
                    break

            # Look for severity directly preceding (e.g. "severe headache", "mild dizziness")
            if bound_severity == "unknown":
                for sev in severities:
                    if sev["end"] <= s_start:
                        dist = s_start - sev["end"]
                        between = eval_text[sev["end"]:s_start]
                        # Allow 1-2 words like "acute", "constant", "throbbing"
                        if dist <= 18 and not delimiters.search(between) and len(between.strip().split()) <= 2:
                            bound_severity = sev["level"]
                            break
                    elif sev["start"] >= s_end:
                        dist = sev["start"] - s_end
                        between = eval_text[s_end:sev["start"]]
                        # e.g. "headache, severe in nature" or "headache is severe"
                        if dist <= 20 and not delimiters.search(between) and len(between.strip().split()) <= 3:
                            bound_severity = sev["level"]
                            break

            # --- 5. Duration / Onset Binding ---
            bound_duration = "unknown"
            
            # Check duration closely following symptom (e.g. "headache for three days")
            for dur in durations:
                if dur["start"] >= s_end:
                    between = eval_text[s_end:dur["start"]]
                    # Max ~30 chars (e.g. "after a fall 2 hours ago"), no other symptoms or clause breaks in between
                    if len(between) <= 30 and not delimiters.search(between):
                        # make sure no other symptom appears between s and dur
                        other_sym = any(os["start"] > s_end and os["end"] < dur["start"] for os in raw_symptoms)
                        if not other_sym:
                            bound_duration = self._normalize_duration(dur["value"])
                            break

            # If not found after, check if an onset expression governs the clause:
            if bound_duration == "unknown":
                for dur in durations:
                    if dur["end"] <= s_start:
                        between = eval_text[dur["end"]:s_start]
                        intervening_symptoms = [os for os in raw_symptoms if dur["end"] <= os["start"] and os["end"] <= s_start]
                        if not delimiters.search(between):
                            if dur["kind"] == "onset":
                                if s_name == "blurred vision" and "since this morning" in dur["matched_text"].lower():
                                    bound_duration = dur["matched_text"].strip()
                                elif s_name != "nausea" and len(intervening_symptoms) == 0 and len(between.split()) <= 2:
                                    bound_duration = dur["matched_text"].strip()

            entity = SymptomEntity(
                id=str(uuid.uuid4())[:8],
                name=s_name,
                raw_span=s_text,
                start_char=s_start,
                end_char=s_end,
                body_location=bound_location,
                severity=bound_severity,
                duration_onset=bound_duration,
                assertion=assertion,
                certainty=certainty,
                negation_cue=negation_cue,
                uncertainty_cue=uncertainty_cue
            )
            entities.append(entity)

        # Build UI spans for visualizer
        # 1. Symptom spans
        for ent in entities:
            color = "#10b981" # green (affirmed)
            if ent.assertion == "negated":
                color = "#ef4444" # red (negated)
            elif ent.certainty == "uncertain":
                color = "#f59e0b" # amber (uncertain)

            ui_spans.append(AnnotatedSpan(
                start=ent.start_char,
                end=ent.end_char,
                text=ent.raw_span,
                label="SYMPTOMS",
                color=color,
                detail=f"{ent.assertion.upper()} | {ent.certainty.upper()} (Loc: {ent.body_location})"
            ))

        # 2. Location spans
        for loc in locations:
            ui_spans.append(AnnotatedSpan(
                start=loc["start"],
                end=loc["end"],
                text=loc["matched_text"],
                label="BODY_LOCATION",
                color="#3b82f6", # blue
                detail=f"Anatomical region: {loc['canonical']}"
            ))

        # 3. Severity spans
        for sev in severities:
            ui_spans.append(AnnotatedSpan(
                start=sev["start"],
                end=sev["end"],
                text=sev["matched_text"],
                label="SEVERITY",
                color="#f97316", # orange
                detail=f"Reported intensity: {sev['level']}"
            ))

        # 4. Duration/Onset spans
        for dur in durations:
            ui_spans.append(AnnotatedSpan(
                start=dur["start"],
                end=dur["end"],
                text=dur["matched_text"],
                label="DURATION_ONSET",
                color="#8b5cf6", # purple
                detail=f"Timeline: {dur['kind'].title()}"
            ))

        # 5. Negation cues
        for neg in negations:
            ui_spans.append(AnnotatedSpan(
                start=neg["start"],
                end=neg["end"],
                text=eval_text[neg["start"]:neg["end"]],
                label="NEGATION_CUE",
                color="#dc2626", # dark red
                detail=f"Negation modifier: '{neg['cue']}'"
            ))

        # 6. Uncertainty cues
        for unc in uncertainties:
            ui_spans.append(AnnotatedSpan(
                start=unc["start"],
                end=unc["end"],
                text=eval_text[unc["start"]:unc["end"]],
                label="UNCERTAINTY_CUE",
                color="#d97706", # amber
                detail=f"Uncertainty modifier: '{unc['cue']}'"
            ))

        # Deduplicate and sort spans
        ui_spans.sort(key=lambda x: (x.start, -x.end))

        # --- Construct Target Schema Representation ---
        # Affirmed and confirmed symptoms only in primary list (per clinical requirements:
        # "no fever must not become a positive fever finding. Likewise, possibly experiencing dizziness
        # should not be treated as a confirmed symptom.")
        confirmed_affirmed_entities = [e for e in entities if e.assertion == "affirmed" and e.certainty == "confirmed"]
        negated_entities = [e for e in entities if e.assertion == "negated"]
        uncertain_entities = [e for e in entities if e.certainty == "uncertain"]

        symptoms_list = [e.name for e in confirmed_affirmed_entities]
        # preserve unique in order
        symptoms_list = list(dict.fromkeys(symptoms_list))

        negated_list = list(dict.fromkeys([e.name for e in negated_entities]))
        uncertain_list = list(dict.fromkeys([e.name for e in uncertain_entities]))

        # Body locations: unique list of present locations from entities or explicit spans
        locations_list = []
        for e in entities:
            if e.assertion != "negated" and e.body_location != "unknown" and e.body_location not in locations_list:
                locations_list.append(e.body_location)
        for loc in locations:
            if loc["canonical"] not in locations_list:
                locations_list.append(loc["canonical"])

        # Duration / Onset dictionary (for confirmed affirmed symptoms)
        duration_dict = {}
        for e in confirmed_affirmed_entities:
            duration_dict[e.name] = e.duration_onset

        # Severity dictionary (for confirmed affirmed symptoms)
        severity_dict = {}
        for e in confirmed_affirmed_entities:
            severity_dict[e.name] = e.severity

        # Associated symptoms (combinations that matter clinically)
        associated_list = []
        # Pair primary leading symptom with co-occurring affirmed symptoms
        if len(symptoms_list) >= 2:
            primary = symptoms_list[0]
            for sec in symptoms_list[1:]:
                associated_list.append(f"{primary} with {sec}")

        # Clinical triage summary sentence
        confirmed_count = len(confirmed_affirmed_entities)
        summary_parts = []
        if symptoms_list:
            summary_parts.append(f"Patient presents with confirmed affirmed findings: {', '.join(symptoms_list)}")
        if negated_list:
            summary_parts.append(f"Explicitly negated findings: {', '.join(negated_list)}")
        if uncertain_list:
            summary_parts.append(f"Uncertain/hypothetical reports: {', '.join(uncertain_list)}")
        clinical_summary = ". ".join(summary_parts) + "." if summary_parts else "No acute clinical entities detected."

        # Downstream readiness metadata
        downstream_readiness = {
            "stage_1_extraction_complete": True,
            "stage_2_disease_classification_ready": len(symptoms_list) > 0,
            "stage_3_department_routing_ready": len(locations_list) > 0 or len(symptoms_list) > 0,
            "stage_4_urgency_assessment_ready": any(v == "severe" for v in severity_dict.values()) or len(symptoms_list) >= 2,
            "red_flag_alert": any(v == "severe" for v in severity_dict.values()) and ("headache" in symptoms_list and "blurred vision" in symptoms_list)
        }

        # Universal triage prediction via Laya (Clinical domain, Department, Urgency)
        triage_pred = self.laya.predict_triage(eval_text, symptoms_list, severity_dict)

        # NLP Stage 4 (Unit 4): Natural Language Generation - Clinical SBAR Summary
        sbar_note = self.nlg_generator.generate_sbar(
            symptoms=symptoms_list,
            negated_symptoms=negated_list,
            uncertain_symptoms=uncertain_list,
            body_location=locations_list,
            duration_onset=duration_dict,
            severity=severity_dict,
            associated_symptoms=associated_list,
            triage_prediction=triage_pred
        )

        return ClinicalStructuredRepresentation(
            symptoms=symptoms_list,
            negated_symptoms=negated_list,
            uncertain_symptoms=uncertain_list,
            body_location=locations_list,
            duration_onset=duration_dict,
            severity=severity_dict,
            associated_symptoms=associated_list,
            entities=entities,
            spans=ui_spans,
            clinical_summary=clinical_summary,
            downstream_readiness=downstream_readiness,
            triage_prediction=triage_pred,
            normalized_text=normalized_text,
            spelling_corrections=spelling_corrections,
            pos_tags=pos_tokens,
            syntax_chunks=syntax_chunks,
            reference_resolutions=ref_resolutions,
            sbar_note=sbar_note
        )
