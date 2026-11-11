"""Discourse Processing and Anaphora Reference Resolution Module.

Implements Unit 3 NLP Syllabus concepts:
- Discourse Processing: Cohesion, Reference Resolution, and Discourse Coherence
- Hobbs-inspired recency salience algorithm for resolving pronominal anaphora in clinical narratives
- Linking cross-sentence clinical modifiers (e.g. "I have knee pain. It started 3 days ago.")
"""

from typing import List, Dict, Any, Tuple, Optional
import re
from .schemas import ReferenceResolution

PRONOUN_TRIGGERS = {"it", "this", "that", "they", "these"}

class ClinicalReferenceResolver:
    """Resolves anaphora in patient narratives to ensure cross-sentence clinical attribution."""

    def __init__(self):
        # Clinical indicator words that signify candidate antecedents
        self.symptom_cues = {
            "pain", "ache", "headache", "fever", "cough", "rash", "nausea",
            "dizziness", "tightness", "swelling", "discomfort", "vomiting",
            "numbness", "weakness", "shortness of breath", "vision", "cramps"
        }

    def resolve(self, text: str) -> Tuple[List[ReferenceResolution], str]:
        """Identify pronouns (it, this, that) and resolve them to the most recent clinical antecedent.
        
        Returns:
            (resolutions, resolved_text)
        """
        resolutions: List[ReferenceResolution] = []
        
        # Split into sentences or clauses
        sentences = re.split(r"(?<=[.!?;\n])\s+", text)
        if len(sentences) <= 1 and not any(p in text.lower().split() for p in PRONOUN_TRIGGERS):
            return resolutions, text

        discourse_entities: List[Dict[str, Any]] = []
        resolved_sentences: List[str] = []

        for s_idx, sentence in enumerate(sentences):
            current_sent = sentence
            words = sentence.split()

            # First, check if current sentence contains a pronoun that needs resolution
            for w_idx, word in enumerate(words):
                clean_word = re.sub(r"[^\w]", "", word).lower()
                if clean_word in PRONOUN_TRIGGERS:
                    # Look backwards in discourse history for the most recent salient antecedent
                    if discourse_entities:
                        antecedent = discourse_entities[-1]  # Most recent salient entity
                        dist = (s_idx - antecedent["sent_idx"]) * 10 + (w_idx + 1)
                        
                        res = ReferenceResolution(
                            pronoun=word,
                            resolved_to=antecedent["text"],
                            antecedent_span=f"Sentence {antecedent['sent_idx']+1}: '{antecedent['text']}'",
                            distance_tokens=dist,
                            mechanism="Discourse Recency Salience (Hobbs-inspired, Unit 3)"
                        )
                        resolutions.append(res)
                        
                        # Replace pronoun in anaphora-resolved text to assist downstream assertion binding
                        pattern = r"\b" + re.escape(word) + r"\b"
                        current_sent = re.sub(pattern, f"{word} [{antecedent['text']}]", current_sent, count=1)

            # Discover clinical entities in this sentence to add to discourse history
            for cue in self.symptom_cues:
                match = re.search(r"\b([a-zA-Z\s]{0,15}" + re.escape(cue) + r")\b", sentence, re.IGNORECASE)
                if match:
                    entity_text = match.group(0).strip()
                    # Filter out pronouns themselves
                    if entity_text.lower() not in PRONOUN_TRIGGERS:
                        discourse_entities.append({
                            "text": entity_text,
                            "sent_idx": s_idx,
                            "cue": cue
                        })

            resolved_sentences.append(current_sent)

        augmented_text = " ".join(resolved_sentences)
        return resolutions, augmented_text

