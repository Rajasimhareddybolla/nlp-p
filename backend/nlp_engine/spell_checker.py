"""Clinical Spelling Correction and Text Normalization Module.

Implements Unit 2 NLP Syllabus concepts:
- Word Level Analysis: Levenshtein & Damerau-Levenshtein Edit Distance (Dynamic Programming)
- Finite-State / Edit Matrix cost computation
- Morphological parsing and normalization
"""

from typing import List, Tuple, Dict, Optional, Set
import re
import nltk
from nltk.stem import WordNetLemmatizer
from .schemas import SpellingCorrection
from .lexicons import SYMPTOM_LEXICON, BODY_LOCATIONS, SEVERITY_LEXICON

# Ensure NLTK words corpus is available
try:
    from nltk.corpus import words as nltk_words
    VALID_ENGLISH_WORDS: Set[str] = set(w.lower() for w in nltk_words.words())
except Exception:
    nltk.download('words', quiet=True)
    from nltk.corpus import words as nltk_words
    VALID_ENGLISH_WORDS = set(w.lower() for w in nltk_words.words())

def levenshtein_matrix(s1: str, s2: str) -> Tuple[int, List[List[int]]]:
    """Compute Levenshtein distance and return the dynamic programming matrix.
    
    dp[i][j] represents the minimum edit operations (insertions, deletions, substitutions)
    to transform prefix s1[0..i-1] into prefix s2[0..j-1].
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost # substitution
            )
            # Damerau transposition check
            if i > 1 and j > 1 and s1[i - 1].lower() == s2[j - 2].lower() and s1[i - 2].lower() == s2[j - 1].lower():
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)
                
    return dp[m][n], dp

def build_clinical_target_lexicon() -> Set[str]:
    """Build target medical vocabulary of canonical terms for clinical spell checking."""
    target_terms: Set[str] = set()
    
    for canon, syns in SYMPTOM_LEXICON.items():
        target_terms.add(canon.lower())
        for syn in syns:
            for w in syn.lower().split():
                if len(w) > 2:
                    target_terms.add(w)
                    
    for canon, locs in BODY_LOCATIONS.items():
        target_terms.add(canon.lower())
        for loc in locs:
            for w in loc.lower().split():
                if len(w) > 2:
                    target_terms.add(w)
                    
    for lvl, terms in SEVERITY_LEXICON.items():
        target_terms.add(lvl.lower())
        for t in terms:
            for w in t.lower().split():
                target_terms.add(w)
                
    return target_terms

CLINICAL_TARGET_TERMS = build_clinical_target_lexicon()

# Curated high-confidence medical corrections for frequent triage typings
KNOWN_CLINICAL_TYPOS = {
    "headeche": "headache",
    "hedache": "headache",
    "headach": "headache",
    "nauesa": "nausea",
    "nausia": "nausea",
    "vomitting": "vomiting",
    "dizzines": "dizziness",
    "dizynes": "dizziness",
    "sever": "severe",
    "sevear": "severe",
    "blury": "blurry",
    "feever": "fever",
    "fevr": "fever",
    "stomac": "stomach",
    "abdoman": "abdomen",
    "abdmonal": "abdominal",
    "diarhea": "diarrhea",
    "diarea": "diarrhea",
    "caugh": "cough",
    "shoartness": "shortness",
    "breth": "breath",
    "cheest": "chest",
    "palpatations": "palpitations",
    "swolen": "swollen",
    "rashs": "rash",
    "alergic": "allergic",
    "alergies": "allergies",
}

class ClinicalSpellChecker:
    """Spell Checker and Text Normalizer based on Levenshtein Distance (NLP Syllabus Unit 2)."""

    def __init__(self):
        self.english_words = VALID_ENGLISH_WORDS
        self.target_terms = CLINICAL_TARGET_TERMS
        self.known_typos = KNOWN_CLINICAL_TYPOS
        self.lemmatizer = WordNetLemmatizer()

    def correct_word(self, word: str) -> Tuple[str, Optional[SpellingCorrection]]:
        """Check and correct a single token using Levenshtein distance."""
        clean_word = word.strip().lower()
        if len(clean_word) < 3 or not clean_word.isalpha():
            return word, None

        # Check known medical typos first
        if clean_word in self.known_typos:
            replacement = self.known_typos[clean_word]
            if word.istitle():
                replacement_cased = replacement.capitalize()
            elif word.isupper():
                replacement_cased = replacement.upper()
            else:
                replacement_cased = replacement
            
            dist, _ = levenshtein_matrix(clean_word, replacement)
            corr = SpellingCorrection(
                original=word,
                corrected=replacement_cased,
                edit_distance=dist,
                algorithm="Levenshtein Matrix Dynamic Programming (Unit 2)",
                explanation=f"Transformed '{word}' to clinical term '{replacement_cased}' (edit distance = {dist})"
            )
            return replacement_cased, corr

        # Morphological parsing check (Unit 2: Lemmatization / Inflections)
        # If already a valid base or inflected English word (e.g. "three", "started", "days"), do NOT alter it!
        if (clean_word in self.english_words or
            self.lemmatizer.lemmatize(clean_word, 'v') in self.english_words or
            self.lemmatizer.lemmatize(clean_word, 'n') in self.english_words or
            self.lemmatizer.lemmatize(clean_word, 'a') in self.english_words):
            return word, None

        # Not in standard dictionary: find closest clinical match within edit distance <= 2
        best_candidate = None
        min_distance = 3

        for cand in self.target_terms:
            if abs(len(cand) - len(clean_word)) > 2:
                continue
            dist, _ = levenshtein_matrix(clean_word, cand)
            if dist < min_distance:
                min_distance = dist
                best_candidate = cand

        if best_candidate and min_distance <= 2:
            if word.istitle():
                replacement = best_candidate.capitalize()
            elif word.isupper():
                replacement = best_candidate.upper()
            else:
                replacement = best_candidate

            corr = SpellingCorrection(
                original=word,
                corrected=replacement,
                edit_distance=min_distance,
                algorithm="Levenshtein Edit Distance (Unit 2)",
                explanation=f"Corrected misspelled token '{word}' to closest clinical lexicon entry '{replacement}' (edit distance = {min_distance})"
            )
            return replacement, corr

        return word, None

    def normalize_text(self, text: str) -> Tuple[str, List[SpellingCorrection]]:
        """Normalize free-text narrative, identifying spelling errors and fixing them."""
        corrections: List[SpellingCorrection] = []
        tokens = re.findall(r"(\w+|[^\w\s]|\s+)", text)
        normalized_tokens = []

        for token in tokens:
            if re.match(r"^[A-Za-z]+$", token):
                corrected_word, corr = self.correct_word(token)
                normalized_tokens.append(corrected_word)
                if corr:
                    corrections.append(corr)
            else:
                normalized_tokens.append(token)

        normalized_text = "".join(normalized_tokens)
        return normalized_text, corrections
