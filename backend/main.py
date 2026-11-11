import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .nlp_engine.extractor import ClinicalExtractionEngine
from .nlp_engine.schemas import ClinicalStructuredRepresentation, ExtractRequest

app = FastAPI(
    title="Clinical Triage Information Extraction API",
    description="Stage 1 Clinical Information Extractor with 5 Target Labels, Negation, and Uncertainty attributes",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ClinicalExtractionEngine()

PRESET_CASES = [
    {
        "id": "case-neuro-prompt",
        "title": "Case 1: Acute Neurological (Benchmark)",
        "subtitle": "Severe headache with acute onset visual disturbance & nausea",
        "text": "I've had a severe headache for three days, and since this morning I've been experiencing nausea and blurred vision.",
        "category": "Neurology / Acute Warning",
        "key_highlights": ["Duration binding", "Selective severity", "Associated symptoms pair"]
    },
    {
        "id": "case-cardiac-negation",
        "title": "Case 2: Cardiac Presentation with Negations",
        "subtitle": "Substernal chest pain with explicit exclusions (NegEx)",
        "text": "Patient presents with severe substernal chest pain for 2 hours. Denies fever, no shortness of breath, and no cough. Possibly experiencing mild dizziness and sweating.",
        "category": "Cardiology / Emergency",
        "key_highlights": ["Pre-negation detection", "Uncertainty scoping", "Body location mapping"]
    },
    {
        "id": "case-peds-fever",
        "title": "Case 3: Pediatric Respiratory & Fever",
        "subtitle": "Multi-day high fever with airway signs and absence of GI symptoms",
        "text": "Child has high-grade fever for 4 days accompanied by barking cough and mild wheezing. Denies nausea, no vomiting, and no abdominal pain.",
        "category": "Pediatrics / Respiratory",
        "key_highlights": ["Severity attribution", "Multi-symptom negation", "Associated pairs"]
    },
    {
        "id": "case-gi-acute",
        "title": "Case 4: Acute Abdomen (Surgical Triage)",
        "subtitle": "Localized acute right lower quadrant pain with associated emesis",
        "text": "Severe abdominal pain localized to the lower right quadrant for 12 hours. Experiencing nausea and vomiting since last night. Denies diarrhea, no fever.",
        "category": "Gastroenterology / Urgent",
        "key_highlights": ["Specific anatomical region", "Co-occurring emesis", "Negated diarrhea"]
    },
    {
        "id": "case-neuro-uncertainty",
        "title": "Case 5: Neurological / Transient Symptoms",
        "subtitle": "Hypothetical / uncertain symptoms with temporal onset",
        "text": "Possibly experiencing dizziness and blurred vision since yesterday. Denies headache or loss of consciousness. Mild numbness in fingers reported.",
        "category": "Neurology / Outpatient",
        "key_highlights": ["Uncertainty preservation", "Affirmed vs negated contrast", "Mild severity"]
    },
    {
        "id": "case-spellcheck-nlp",
        "title": "Case 6: Typo & Edit Distance Normalization (Unit 2)",
        "subtitle": "Patient narrative with multiple spelling errors normalized via Levenshtein DP",
        "text": "I have sever headeche and nauesa for 2 days. Feeling dizzines and blury vision since morning. Denies feever.",
        "category": "NLP Unit 2 / Levenshtein Correction",
        "key_highlights": ["Dynamic Programming Matrix", "Sub-word edit distance", "Automated clinical normalization"]
    },
    {
        "id": "case-anaphora-nlp",
        "title": "Case 7: Cross-Sentence Anaphora Resolution (Unit 3)",
        "subtitle": "Discourse pronoun resolution linking modifiers across sentences",
        "text": "Patient reports severe chest pain. It started three hours ago after climbing stairs. It is accompanied by shortness of breath and sweating.",
        "category": "NLP Unit 3 / Discourse Anaphora",
        "key_highlights": ["Recency-salience Hobbs resolution", "Cross-sentence modifier binding", "SBAR NLG synthesis"]
    }
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "stage": "Stage 1: Clinical Information Extraction", "version": "1.0.0"}

@app.get("/api/presets")
def get_presets():
    return {"presets": PRESET_CASES}

@app.post("/api/extract", response_model=ClinicalStructuredRepresentation)
def extract_clinical_info(req: ExtractRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    try:
        result = engine.extract(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction error: {str(e)}")

# Mount static frontend build if it exists
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if full_path and os.path.exists(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

