"""POS Tagging and Syntactic Analysis Module.

Implements Unit 2 NLP Syllabus concepts:
- Part-of-Speech (POS) Tagging (Penn Treebank Tagset)
- Syntactic Analysis: Context-Free Grammar (CFG) rules for clinical symptom phrases
- Constituency Parsing & Shallow Chunking via RegexpParser
"""

from typing import List, Dict, Any, Optional
import nltk
from nltk import word_tokenize, pos_tag, RegexpParser
from .schemas import POSToken, SyntacticChunk

PENN_TAG_DESCRIPTIONS = {
    "JJ": "Adjective (Severity / Modifier)",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "NN": "Noun, singular (Symptom / Anatomy)",
    "NNS": "Noun, plural (Symptoms / Locations)",
    "NNP": "Proper noun, singular",
    "NNPS": "Proper noun, plural",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense (Temporal marker)",
    "VBG": "Verb, gerund/present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "CD": "Cardinal number (Duration / Quantification)",
    "IN": "Preposition / Subordinating conjunction (Temporal/Spatial)",
    "DT": "Determiner",
    "RB": "Adverb (Negation / Degree)",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "CC": "Coordinating conjunction (Syndrome linkage)",
    "PRP": "Personal pronoun (Anaphoric referent)",
    "PRP$": "Possessive pronoun",
    "MD": "Modal auxiliary",
    "WDT": "Wh-determiner",
    "WP": "Wh-pronoun",
    "WRB": "Wh-adverb"
}

# Context-Free Grammar (CFG) Chunking Rules for Clinical Text
CLINICAL_CFG_GRAMMAR = r"""
  NP: {<DT>?<JJ.*|VBN>*<NN.*>+}         # Noun Phrase: e.g. "a severe headache", "blurred vision"
  PP: {<IN><CD|DT>?<JJ.*>*<NN.*>+}      # Prepositional Phrase: e.g. "for three days", "in the chest"
  VP: {<VB.*><RB>?<VBN|VBG>?}           # Verb Phrase: e.g. "have had", "been experiencing"
"""

class ClinicalSyntacticAnalyzer:
    """Performs POS Tagging and Context-Free Grammar syntactic chunking for clinical narratives."""

    def __init__(self):
        self.chunker = RegexpParser(CLINICAL_CFG_GRAMMAR)

    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text to produce POS tags and CFG syntactic constituency chunks."""
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)

        pos_tokens: List[POSToken] = []
        for i, (word, tag) in enumerate(tagged):
            desc = PENN_TAG_DESCRIPTIONS.get(tag, "Grammatical Token")
            # Syntactic head heuristic (closest following noun or verb)
            head_target = tagged[min(i + 1, len(tagged) - 1)][0] if i + 1 < len(tagged) else "ROOT"
            dep_label = "modifier" if tag.startswith("JJ") or tag.startswith("RB") else ("head" if tag.startswith("NN") else "rel")

            pos_tokens.append(
                POSToken(
                    token=word,
                    lemma=word.lower(),
                    pos=tag,
                    tag_desc=desc,
                    dep=dep_label,
                    head=head_target
                )
            )

        # CFG Parsing
        parse_tree = self.chunker.parse(tagged)
        chunks: List[SyntacticChunk] = []
        
        seen_chunks = set()
        for subtree in parse_tree.subtrees(filter=lambda t: hasattr(t, 'label') and t.label() in ('NP', 'PP', 'VP')):
            phrase = " ".join([w for w, tag in subtree.leaves()])
            label = subtree.label()
            
            if phrase.lower() in seen_chunks or len(phrase.split()) > 6 or phrase.isalnum() is False and len(phrase.split()) == 1:
                continue
            seen_chunks.add(phrase.lower())

            rule_map = {
                "NP": "CFG: NP -> (Det)? (Adj|VBN)* Noun+ (Clinical Symptom / Anatomy)",
                "PP": "CFG: PP -> Prep (Num)? Noun+ (Temporal Onset / Anatomical Location)",
                "VP": "CFG: VP -> Verb (Adv)? VerbParticiple? (Clinical Presentation)"
            }

            chunks.append(
                SyntacticChunk(
                    chunk_text=phrase,
                    phrase_type=f"{label} ({'Noun Phrase' if label=='NP' else ('Prepositional Phrase' if label=='PP' else 'Verb Phrase')})",
                    rule=rule_map.get(label, f"CFG: {label} Production")
                )
            )

        return {
            "pos_tokens": pos_tokens,
            "syntax_chunks": chunks[:10]
        }
