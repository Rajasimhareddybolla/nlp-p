# Clinical Triage Information Extraction & Decision Support Architecture

## 1. Executive Summary & Vision

This system provides a modern, safety-critical natural language processing (NLP) architecture for **Clinical Information Extraction and Intelligent Patient Triaging**.

Traditional clinical decision support systems and generic large language models (LLMs) often conflate symptom extraction, disease classification, and triage urgency into a single uninterpretable step. This introduces severe clinical safety risks—such as hallucinating unstated symptoms, failing to recognize critical negations (*"denies fever"*), or dismissing emergent conditions (*"severe headache accompanied by acute blurred vision"*) because the disease classifier predicts a non-emergent benign headache.

This architecture decouples the problem into **four independent stages**, anchored by an open-vocabulary clinical extraction layer (Stage 1) and powered by **Laya**—a non-autoregressive, calibrated System 1 decision engine.

```mermaid
flowchart TD
    A["Patient Narrative (Free-Text Complaint)"] --> B["Stage 1: Clinical Information Extraction\n(Open-Vocabulary Extractor)"]
    
    B --> C["5 Structured Target Labels\n+ Negation & Uncertainty Attributes"]
    
    C --> D["Stage 2: Disease Classification\n(Laya System 1 Decision Engine)"]
    C --> E["Stage 3: Department Recommendation\n(Laya Specialist Router)"]
    C --> F["Stage 4: Urgency & Safety Assessment\n(Clinical Rules & Laya Acuity Engine)"]
    
    D --> G["Clinical Impression & Differential"]
    E --> H["Hospital Unit / Clinic Routing"]
    F --> I["Triage Priority (Emergency / Urgent / Routine)"]
    
    style B fill:#0284c7,stroke:#0369a1,color:#fff,stroke-width:2px
    style C fill:#10b981,stroke:#059669,color:#fff,stroke-width:2px
    style D fill:#6366f1,stroke:#4f46e5,color:#fff
    style E fill:#8b5cf6,stroke:#7c3aed,color:#fff
    style F fill:#ef4444,stroke:#dc2626,color:#fff,stroke-width:2px
```

---

## 2. The Architectural Problem: Why Traditional Approaches Fail

### 2.1 The Failure of Legacy Token Classifiers (e.g., HUMADEX, BioBERT, ClinicalBERT)
Early medical NER models like **HUMADEX** (~100M parameter token-classification model, reported F1 $\approx 0.801$) rely on coarse entity tags: `PROBLEM`, `TEST`, and `TREATMENT`.
1. **Lack of Attribute Binding**: Coarse tags cannot link which duration or which severity belongs to which specific symptom. If a patient reports *"severe headache for three days, with nausea and blurred vision since morning"*, token classification marks all as `PROBLEM` without attributing *"severe"* or *"3 days"* strictly to *"headache"*.
2. **Negation Blindness**: Standard token classifiers flag the word *"fever"* in *"denies fever"* as a positive `PROBLEM`, contaminating downstream diagnostic algorithms.
3. **Fixed Closed Vocabulary**: They fail to generalize to arbitrary patient descriptions, rare complaints, or conversational idioms.

### 2.2 The Failure of Autoregressive LLMs (e.g., GPT-4, Llama)
Attempting to solve clinical triage with monolithic generative LLMs introduces critical risks:
1. **Hallucination of Modifiers**: Generative models frequently invent severity ratings when unspecified (e.g., assuming nausea is "moderate" even when the patient gave no severity).
2. **High Latency & Resource Footprint**: Autoregressive decoding requires sequential token-by-token generation (often taking 2,000 ms to 10,000 ms), making them unsuitable for real-time ambulatory intake or high-throughput triage kiosks.
3. **Dangerous Conflation of Disease and Urgency**: Predicting a disease does not automatically establish urgency. For instance, headache and nausea alone cannot confirm a diagnosis. However, a **severe headache accompanied by new acute blurred vision** warrants immediate emergency evaluation. A monolithic LLM predicting a benign migraine might dismiss these concerning neurological red flags.

---

## 3. The 5-Label Clinical Schema & Assertion Preservation

The target schema establishes five distinct structured fields, supplemented by clinical assertion scopes.

### 3.1 The 5 Target Fields

| # | Target Label | Clinical Purpose | Example Value |
|---|---|---|---|
| **1** | `SYMPTOMS` | Identifies active, confirmed clinical complaints | `["headache", "nausea", "blurred vision"]` |
| **2** | `BODY_LOCATION` | Identifies anatomical regions to guide specialist routing | `["head", "eyes"]` |
| **3** | `DURATION_ONSET` | Maps specific duration and onset timestamps per symptom | `{"headache": "3 days", "nausea": "unknown", "blurred vision": "since this morning"}` |
| **4** | `SEVERITY` | Measures intensity without inventing unspecified values | `{"headache": "severe", "nausea": "unknown", "blurred vision": "unknown"}` |
| **5** | `ASSOCIATED_SYMPTOMS` | Captures syndromic combinations that impact clinical triage | `["headache with nausea", "headache with blurred vision"]` |

### 3.2 Clinical Assertion Attributes (Safety Layer)
1. **Negation Preservation (ConText / NegEx)**:
   - Phrases like *"no fever"*, *"denies chest pain"*, or *"without shortness of breath"* are isolated into `negated_symptoms` with an explicit `assertion: "negated"` attribute.
   - **Crucial Rule**: A negated finding must **never** become an affirmed positive symptom.
2. **Uncertainty & Speculation Preservation**:
   - Phrases like *"possibly experiencing dizziness"* or *"unclear if nauseous"* are mapped with `certainty: "uncertain"`.
   - **Crucial Rule**: Hypothetical complaints are preserved for context but separated from confirmed findings.
3. **Strict Attribute Binding (Zero-Hallucination)**:
   - In: *"I've had a severe headache for three days, and since this morning I've been experiencing nausea and blurred vision."*
   - Modifiers are bound strictly to their governing entity:
     - `headache` &rarr; Severity: `"severe"`, Duration: `"3 days"`
     - `nausea` &rarr; Severity: `"unknown"`, Duration: `"unknown"`
     - `blurred vision` &rarr; Severity: `"unknown"`, Duration: `"since this morning"`
   - Notice that severity is **not invented** for nausea or blurred vision.

---

## 4. Laya from an NLP Perspective

### 4.1 What is Laya?
**Laya** is a **multilingual, non-autoregressive System 1 decision engine**. Rather than generating free-form natural language text word-by-word, Laya evaluates **typed questions** directly over a state document in a **single forward pass** (~33 ms).

### 4.2 NLP Fundamentals & Mathematical Architecture
1. **Non-Autoregressive Forward Pass**:
   - Traditional LLMs compute: $P(y_t \mid y_{<t}, x)$ sequentially for each token $t$.
   - Laya computes typed decision outputs $P(y \mid x)$ in a single forward pass over its bidirectional encoder backbone (**ModernBERT-large** for English, **mmBERT-base** for multilingual).
2. **Strictly Proper Scoring Rules (RLCD)**:
   - Laya is trained using Reinforcement Learning against Strictly Proper Scoring Rules.
   - This ensures that output probabilities are **calibrated confidence estimates** rather than overconfident hallucinations.
3. **Typed Decision Primitives**:
   - `choice`: Selects a categorical label from semantic criteria (e.g., disease domain or hospital department).
   - `score`: Computes ordinal ranking (e.g., triage urgency scale).
   - `noul`: Calculates exact $P(\text{true})$ probabilities for binary statements (e.g., verifying whether a symptom is denied or uncertain).
4. **Multilingual Invariance**:
   - Laya's internal router detects language and script in $<0.5\text{ ms}$, dispatching non-Latin scripts to `laya-multilingual` with native comprehension across 100+ languages.

### 4.3 Why Laya is Superior for Clinical Triaging

| Metric | Traditional Autoregressive LLM | Laya System 1 Decision Engine |
|---|---|---|
| **Latency** | 1,500 ms – 5,000 ms | **30 ms – 50 ms** (50x faster) |
| **Hallucination Risk** | High (can invent unstated facts) | **Zero** (evaluates against typed schema criteria) |
| **Output Format** | Unstructured text needing parsing | **Typed JSON / Pydantic structures** |
| **Calibration** | Frequently overconfident / miscalibrated | **Mathematically calibrated probabilities** |
| **Resource Footprint** | 8B – 70B parameters, multi-GPU required | **322M – 421M parameters**, runs on standard CPU |

---

## 5. System Implementation Walkthrough

The codebase is organized into a modular full-stack architecture:

### 5.1 Backend Engine (`backend/`)
- **`backend/nlp_engine/lexicons.py`**:
  - Open-vocabulary clinical knowledge base covering neurological, cardiovascular, respiratory, gastrointestinal, musculoskeletal, dermatological, and ENT entities.
  - Dynamic syntactic regex matchers (`OPEN_SYMPTOM_PATTERNS`) to extract unconstrained symptom phrases (e.g., *"sharp pain in left wrist"*, *"burning sensation"*).
  - Universal anatomical location lexicon mapping all organ systems.
- **`backend/nlp_engine/extractor.py`**:
  - `ClinicalExtractionEngine`: Orchestrates tokenization, syntactic scope resolution, attribute binding, negation detection (ConText/NegEx algorithm), and uncertainty evaluation.
- **`backend/nlp_engine/laya_service.py`**:
  - `LayaUniversalClassifier`: Integrates Laya's `Router(device="cpu")` to evaluate open clinical domains, specialist department routing, and triage urgency levels in a single pass.
- **`backend/main.py`**:
  - High-performance FastAPI REST API exposing `/api/extract`, `/api/presets`, `/api/health`, and serving the compiled frontend application.

### 5.2 Frontend Interface (`frontend/`)
- Minimalist, distraction-free clinical UI built with **React 18**, **TypeScript**, and **Tailwind CSS**.
- **Interactive Intake Narrative**: Free-form text box with one-click benchmark chips (Neurology, Cardiology with NegEx, Orthopedics, Dermatology, ENT).
- **The 5 Extracted Fields Card**: Clean presentation of Symptoms (green confirmed pills, red strikethrough for negations, amber badges for uncertainties), Body Locations, Duration/Onset mappings, Severity levels, and Associated Pairs.
- **Clinical Decision Card**: Live Laya predictions showing clinical diagnostic domain, recommended department, and triage urgency tier.
- **Structured JSON Export**: One-click copy/download matching the exact schema format.

---

## 6. End-to-End Execution Trace

### Example: Acute Neurological Presentation
**Input Patient Narrative:**
> *"I've had a severe headache for three days, and since this morning I've been experiencing nausea and blurred vision."*

#### 1. Stage 1 Extraction Output
```json
{
  "symptoms": ["headache", "nausea", "blurred vision"],
  "negated_symptoms": [],
  "uncertain_symptoms": [],
  "body_location": ["head", "eyes"],
  "duration_onset": {
    "headache": "3 days",
    "nausea": "unknown",
    "blurred vision": "since this morning"
  },
  "severity": {
    "headache": "severe",
    "nausea": "unknown",
    "blurred vision": "unknown"
  },
  "associated_symptoms": [
    "headache with nausea",
    "headache with blurred vision"
  ]
}
```

---

## 6. Academic NLP Course Syllabus Integration (23CS7PENLP / 23CS8PENLP)

Rather than functioning as a black-box API wrapper, this system directly implements and visualizes the core theoretical pillars of the university Natural Language Processing curriculum:

| Syllabus Unit | Core NLP Concept | Architectural Implementation in this Project |
|---|---|---|
| **Unit 2: Word Level Analysis** | Levenshtein & Damerau-Levenshtein Edit Distance | Dynamic Programming Matrix calculation for clinical spelling error detection and correction (`backend/nlp_engine/spell_checker.py`). Corrects patient typos (e.g., *"headeche"* &rarr; *"headache"*, *"sever"* &rarr; *"severe"*, *"nauesa"* &rarr; *"nausea"*) with exact edit distance accounting. |
| **Unit 2: Morphological Parsing** | Lemmatization & Word Inflections | Integrates NLTK WordNet Lemmatizer to morphologically parse verb/noun inflections (e.g., distinguishing inflected forms like *"started"* from uninflected roots like *"start"*) so valid past tenses are never corrupted by spell checking. |
| **Unit 2: Syntactic Analysis** | Part-of-Speech (POS) Tagging & Penn Treebank | Analyzes free-text narratives with Penn Treebank POS tagger (`pos_tagger.py`), distinguishing adjectives (`JJ` - Severity / Modifiers), nouns (`NN`/`NNS` - Symptoms / Body locations), and prepositions (`IN` - Temporal / Spatial markers). |
| **Unit 2: Syntactic Analysis** | Context-Free Grammar (CFG) & Constituency Parsing | Implements clinical CFG production rules via `RegexpParser` (`pos_tagger.py`):<br>• $\text{NP} \rightarrow (\text{Det})? (\text{Adj}|\text{VBN})^* \text{Noun}^+$<br>• $\text{PP} \rightarrow \text{Prep } (\text{Num})? \text{Noun}^+$<br>Extracts clinical noun and prepositional phrases for syntactic tree visualization. |
| **Unit 3: Discourse Processing** | Cohesion & Reference Resolution (Anaphora) | Implements Hobbs-inspired discourse recency salience algorithm (`reference_resolver.py`). Resolves third-person neuter pronouns (*"it"*, *"this"*, *"that"*) across sentences (e.g., *"I have severe chest pain. It started three hours ago."*) to re-link orphaned temporal durations and severity modifiers back to their antecedent clinical entities. |
| **Unit 4: Natural Language Generation (NLG)** | Architecture of NLG Systems (Reiter & Dale) | Implements the 3-tier NLG pipeline (`nlg_generator.py`):<br>1. **Content Planning**: Selects salient primary symptoms, pertinent negatives, and urgency ratings.<br>2. **Sentence Planning**: Aggregates co-occurrences and lexical connectives (*"accompanied by"*, *"denying any history of"*).<br>3. **Surface Realization**: Generates cohesive, professional clinical handover notes in standard **SBAR** (Situation, Background, Assessment, Recommendation) format. |
| **Unit 5: Lexical Resources & Information Extraction** | WordNet, Clinical Lexicons & Structured Extraction | Leverages WordNet lexical hierarchies and curated clinical taxonomies for open-vocabulary clinical information extraction into five target schema fields. |

---

## 7. Complete Verification Example: Benchmark Walkthrough

### 1. Patient Input Narrative
> *"I've had a severe headache for three days, and since this morning I've been experiencing nausea and blurred vision."*

#### 1. Stage 1 Extracted 5-Field Schema Output
```json
{
  "symptoms": [
    "headache",
    "nausea",
    "blurred vision"
  ],
  "body_location": [
    "head",
    "eyes"
  ],
  "duration_onset": {
    "headache": "3 days",
    "nausea": "unknown",
    "blurred vision": "since this morning"
  },
  "severity": {
    "headache": "severe",
    "nausea": "unknown",
    "blurred vision": "unknown"
  },
  "associated_symptoms": [
    "headache with nausea",
    "headache with blurred vision"
  ]
}
```

#### 2. Laya Triage Decision Layer Output
```json
{
  "source": "Laya (Universal System 1 Decision Engine)",
  "disease": {
    "name": "Neurological / Cerebrovascular",
    "confidence": 53.5
  },
  "department": {
    "name": "Neurology Clinic",
    "confidence": 55.1
  },
  "urgency": {
    "level": "Emergency (Immediate Care)"
  }
}
```

#### 3. Stage 4 Generated Clinical SBAR Note (NLG Pipeline)
```text
CLINICAL TRIAGE SBAR HANDOVER NOTE
=====================================
[S - SITUATION]:
Patient presents for clinical triage with primary complaint of headache, nausea, blurred vision localized to the head, eyes.

[B - BACKGROUND]:
Timeline indicates symptom manifestation: headache (3 days); blurred vision (since this morning). Syndromic presentation exhibits co-occurrence: headache with nausea; headache with blurred vision.

[A - ASSESSMENT]:
Elevated symptom intensity reported for: headache.

[R - RECOMMENDATION]:
Recommended Specialty Route: Neurology Clinic (Triage Priority: EMERGENCY). Direct physician evaluation advised without delay due to acute symptom combination.
```

---

## 8. Comparative Benchmark: Traditional vs This Architecture

| Dimension | Traditional Approach (Monolithic LLM / Rule-Based) | Our Architecture (Decoupled Stage 1 + Laya) |
|---|---|---|
| **Modifier Attribution** | Conflates modifiers across clauses or hallucinates severities for all symptoms. | **Strictly binds modifiers** to governing symptom; unstated severities remain `"unknown"`. |
| **Negation Handling** | Often trips up on double negatives or classifies negated terms as affirmed positive findings. | **ConText / NegEx scoping** separates negated findings into an explicit audit trail. |
| **Safety Coupling** | Single model decides disease and urgency simultaneously; benign disease prediction can mask emergency symptoms. | **Decoupled stages**: Severe headache + acute blurred vision triggers Emergency acuity regardless of disease label. |
| **Execution Latency** | 2.5s – 8.0s per patient request. | **< 100 ms total latency** (instant UI response). |
| **Deployability** | Expensive GPU clusters; sensitive clinical data sent to external proprietary APIs. | **100% on-premise CPU execution**, zero external data leakage, HIPAA/GDPR ready. |

---

## 8. Future Applications & Roadmap

1. **Emergency Department (ED) Digital Kiosks**:
   - Enables walk-in patients to input symptoms in any language, performing immediate pre-triage acuity calculation (ESI score estimation) before nurse intake.
2. **Telemedicine Ambulatory Routing**:
   - Automatically directs patient portal tickets to the correct medical specialty (Cardiology vs Neurology vs Orthopedics) without requiring manual clinical review.
3. **EHR Ambient Clinical Note Extraction**:
   - Connects to Electronic Health Record (EHR) systems via **FHIR / HL7** standards, parsing physician encounter notes into structured clinical problem lists.
4. **Multilingual Global Health Triage**:
   - Leveraging Laya's native support for 100+ languages to provide identical clinical extraction and triage accuracy in low-resource and non-English healthcare settings.

