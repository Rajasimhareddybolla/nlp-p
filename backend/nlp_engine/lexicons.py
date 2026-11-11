"""Universal Medical Lexicons and Open-Vocabulary Clinical Knowledge Base."""

import re

# Comprehensive canonical symptoms across all medical specialties
SYMPTOM_LEXICON = {
    # Neurological / Cranial
    "headache": ["headache", "head pain", "cephalea", "migraine", "head pressure", "throbbing head", "head ache"],
    "dizziness": ["dizziness", "dizzy", "lightheaded", "lightheadedness", "vertigo", "spinning sensation", "unsteadiness", "disequilibrium", "loss of balance"],
    "blurred vision": ["blurred vision", "blurry vision", "fuzzy vision", "loss of focus in eyes", "visual disturbance", "diplopia", "double vision", "impaired vision", "vision changes"],
    "numbness": ["numbness", "loss of sensation", "tingling", "paresthesia", "pins and needles", "numb sensation"],
    "weakness": ["weakness", "loss of strength", "faintness", "asthenia", "muscle weakness", "paresis"],
    "confusion": ["confusion", "disorientation", "altered mental state", "fogginess", "brain fog", "delirium", "memory loss"],
    "syncope": ["syncope", "passed out", "fainted", "blackout", "loss of consciousness", "presyncope", "fainting spell"],
    "stiff neck": ["stiff neck", "neck stiffness", "meningismus", "nuchal rigidity"],
    "photophobia": ["photophobia", "sensitivity to light", "light sensitivity"],
    "phonophobia": ["phonophobia", "sound sensitivity", "sensitivity to noise"],
    "tremor": ["tremor", "trembling", "shaking", "shaky hands", "involuntary twitching"],
    "seizures": ["seizure", "seizures", "convulsions", "fit", "fits", "epileptic episode"],
    "tinnitus": ["tinnitus", "ringing in ears", "buzzing in ears", "ear ringing", "ear buzzing"],

    # ENT / Ophthalmic
    "eye pain": ["eye pain", "ocular pain", "pain in eye", "pain in eyes", "eye soreness"],
    "eye redness": ["red eye", "red eyes", "eye redness", "bloodshot eyes", "conjunctivitis"],
    "earache": ["earache", "ear pain", "pain in ear", "otalgia"],
    "ear discharge": ["ear discharge", "drainage from ear", "fluid from ear", "otorrhea"],
    "hearing loss": ["hearing loss", "diminished hearing", "hard of hearing", "deafness"],
    "sore throat": ["sore throat", "throat pain", "scratchy throat", "pharyngitis", "pain swallowing", "odynophagia", "raw throat"],
    "hoarseness": ["hoarseness", "raspy voice", "loss of voice", "laryngitis", "dysphonia"],
    "dysphagia": ["dysphagia", "difficulty swallowing", "trouble swallowing", "swallowing problem"],
    "nasal congestion": ["nasal congestion", "stuffy nose", "blocked nose", "runny nose", "rhinorrhea", "sinus pressure"],
    "nosebleed": ["nosebleed", "bloody nose", "epistaxis", "bleeding from nose"],

    # Gastrointestinal
    "nausea": ["nausea", "feeling sick", "queasy", "upset stomach", "nauseous", "nauseated", "sick to stomach"],
    "vomiting": ["vomiting", "vomited", "emesis", "threw up", "throwing up", "puking"],
    "hematemesis": ["vomiting blood", "blood in vomit", "hematemesis", "coffee ground emesis"],
    "abdominal pain": ["abdominal pain", "stomach ache", "belly pain", "cramps", "tummy ache", "gut pain", "pelvic pain", "epigastric pain", "stomach cramps"],
    "diarrhea": ["diarrhea", "loose stools", "watery stools", "frequent bowel movements", "runny stools"],
    "constipation": ["constipation", "unable to pass stool", "hard stools", "difficulty passing stool"],
    "heartburn": ["heartburn", "acid reflux", "indigestion", "pyrosis", "gerd", "acid regurgitation"],
    "bloating": ["bloating", "abdominal distension", "gassy", "swollen abdomen"],
    "blood in stool": ["blood in stool", "rectal bleeding", "melena", "black tarry stools", "hematochezia"],

    # Cardiovascular
    "chest pain": ["chest pain", "angina", "chest tightness", "chest pressure", "substernal pressure", "crushing chest pain", "heavy chest", "chest discomfort", "substernal chest pain"],
    "palpitations": ["palpitations", "racing heart", "heart pounding", "fluttering heart", "irregular heartbeat", "tachycardia", "skipped beats"],
    "shortness of breath": ["shortness of breath", "sob", "breathlessness", "difficulty breathing", "dyspnea", "trouble breathing", "winded", "labored breathing"],
    "edema": ["edema", "swelling in legs", "swollen ankles", "swollen feet", "fluid retention", "puffy legs"],

    # Respiratory
    "cough": ["cough", "coughing", "dry cough", "productive cough", "hacking cough", "barking cough", "phlegm cough"],
    "wheezing": ["wheezing", "whistling breathing", "stridor", "whistling sound when breathing"],
    "hemoptysis": ["coughing blood", "blood in sputum", "hemoptysis", "bloody cough"],

    # Musculoskeletal
    "back pain": ["back pain", "lower back pain", "upper back pain", "lumbago", "lumbar pain", "flank pain", "sciatica", "spine pain"],
    "neck pain": ["neck pain", "cervical pain", "sore neck", "pain in neck"],
    "joint pain": ["joint pain", "arthralgia", "aching joints", "joint swelling", "joint stiffness", "knee pain", "shoulder pain", "wrist pain", "hip pain", "ankle pain", "elbow pain"],
    "muscle pain": ["muscle pain", "myalgia", "muscle aches", "muscle cramps", "muscle spasm", "sore muscles"],

    # Dermatological
    "rash": ["rash", "eruption", "hives", "erythema", "skin bumps", "itching", "pruritus", "dermatitis", "itchy skin", "red skin", "skin lesions", "blisters"],
    "swelling": ["swelling", "swollen", "edema", "lump", "mass", "inflammation"],
    "bruising": ["bruising", "bruises", "ecchymosis", "hematoma", "purple discoloration"],

    # Genitourinary
    "dysuria": ["painful urination", "burning urination", "dysuria", "pain peeing", "burning when peeing"],
    "hematuria": ["blood in urine", "hematuria", "pink urine", "red urine"],
    "urinary frequency": ["frequent urination", "peeing often", "urinary urgency", "bladder pressure"],

    # Systemic / Constitutional
    "fever": ["fever", "high temperature", "febrile", "pyrexia", "hot to touch", "feverish"],
    "chills": ["chills", "shivering", "rigors", "shivering fits", "cold sweats"],
    "fatigue": ["fatigue", "exhaustion", "lethargy", "tiredness", "malaise", "worn out", "weakness"],
    "sweating": ["sweating", "diaphoresis", "night sweats", "profuse sweating", "perspiration"],
    "weight loss": ["unexplained weight loss", "weight loss", "losing weight"],
    "body aches": ["body aches", "generalized aches", "feeling achy all over"]
}

# Open-vocabulary regex patterns to extract ANY arbitrary symptom phrase:
# e.g. "severe pain in left wrist", "burning sensation when urinating", "itching in scalp", etc.
OPEN_SYMPTOM_PATTERNS = [
    # "[pain/ache/discomfort/swelling/etc.] in [location]"
    re.compile(r"\b((?:sharp|dull|throbbing|burning|shooting|stabbing|crushing|severe|mild|moderate)?\s*(?:pain|ache|aches|discomfort|pressure|cramps?|soreness|burning|stiffness|swelling|numbness|tingling|weakness|itching|rash|spasms?))\b", re.IGNORECASE),
    # "difficulty [verb-ing]"
    re.compile(r"\b((?:difficulty|trouble|inability)\s+(?:breathing|swallowing|walking|sleeping|hearing|seeing|speaking|urinating|moving))\b", re.IGNORECASE),
    # "loss of [function]"
    re.compile(r"\b(loss\s+of\s+(?:balance|vision|taste|smell|sensation|consciousness|strength|appetite))\b", re.IGNORECASE),
    # "swollen [part]"
    re.compile(r"\b(swollen\s+[a-z]+)\b", re.IGNORECASE)
]

# Universal Anatomical Body Locations (Every major organ system & body region)
BODY_LOCATIONS = {
    "head": ["head", "cranial", "forehead", "temple", "temples", "scalp", "skull", "face", "facial", "jaw", "chin", "cheek", "cheeks"],
    "eyes": ["eye", "eyes", "ocular", "vision", "pupil", "pupils", "eyeball", "eyeballs", "eyelid", "eyelids", "visual"],
    "ears": ["ear", "ears", "canal", "eardrum", "auricle", "inner ear"],
    "nose": ["nose", "nasal", "sinus", "sinuses", "nostril", "nostrils"],
    "throat": ["throat", "pharynx", "larynx", "tonsils", "tonsil", "airway", "vocal cord", "vocal cords", "trachea"],
    "neck": ["neck", "cervical", "nuchal", "nape"],
    "chest": ["chest", "substernal", "thoracic", "precordial", "sternum", "ribs", "breast", "breasts", "rib cage"],
    "heart": ["heart", "cardiac"],
    "lungs": ["lung", "lungs", "pulmonary", "bronchial", "chest cavity"],
    "abdomen": ["abdomen", "abdominal", "stomach", "belly", "tummy", "epigastric", "gut", "pelvis", "pelvic", "lower right quadrant", "lower left quadrant", "upper right quadrant", "upper left quadrant", "ruq", "rlq", "luq", "llq", "navel", "umbilicus", "groin", "inguinal"],
    "back": ["back", "lumbar", "flank", "flanks", "spine", "spinal", "upper back", "lower back", "mid back", "sacrum", "tailbone"],
    "limbs": ["arm", "arms", "leg", "legs", "shoulder", "shoulders", "bicep", "tricep", "forearm", "elbow", "elbows", "wrist", "wrists", "hand", "hands", "finger", "fingers", "thumb", "thumbs", "thigh", "thighs", "knee", "knees", "shin", "shins", "calf", "calves", "ankle", "ankles", "foot", "feet", "heel", "heels", "toe", "toes", "extremity", "extremities"],
    "skin": ["skin", "cutaneous", "dermal", "epidermis"]
}

# Symptom to natural anatomical region default mapping
SYMPTOM_DEFAULT_LOCATION = {
    "headache": "head",
    "blurred vision": "eyes",
    "eye pain": "eyes",
    "eye redness": "eyes",
    "earache": "ears",
    "tinnitus": "ears",
    "stiff neck": "neck",
    "neck pain": "neck",
    "sore throat": "throat",
    "hoarseness": "throat",
    "dysphagia": "throat",
    "chest pain": "chest",
    "palpitations": "chest",
    "shortness of breath": "lungs",
    "cough": "throat",
    "wheezing": "lungs",
    "hemoptysis": "lungs",
    "abdominal pain": "abdomen",
    "heartburn": "abdomen",
    "bloating": "abdomen",
    "back pain": "back",
    "dysuria": "abdomen",
    "hematuria": "abdomen"
}

# Universal Severity Scale
SEVERITY_LEXICON = {
    "severe": [
        "severe", "severely", "excruciating", "intense", "sharp", "worst", 
        "unbearable", "extreme", "terrible", "crushing", "10/10", "9/10", "8/10",
        "very high", "high-grade", "profuse", "acute severe", "debilitating", "incapacitating"
    ],
    "moderate": [
        "moderate", "moderately", "noticeable", "uncomfortable", "medium", 
        "significant", "5/10", "6/10", "7/10", "fairly bad", "constant ache"
    ],
    "mild": [
        "mild", "mildly", "slight", "slightly", "minor", "minimal", "low-grade", 
        "1/10", "2/10", "3/10", "4/10", "dull", "faint", "manageable", "tolerable"
    ]
}

# Universal Negation Triggers (ConText / NegEx)
PRE_NEGATION_TRIGGERS = [
    "no", "not", "without", "denies", "denied", "denying", 
    "negative for", "free of", "rules out", "ruled out", 
    "no evidence of", "no sign of", "no signs of", 
    "does not have", "doesn't have", "did not experience", "haven't had", 
    "hasn't had", "no report of", "patient denies", "never had", "absent of",
    "not having", "without any"
]

POST_NEGATION_TRIGGERS = [
    "absent", "is absent", "unremarkable", "ruled out", "negative", "resolved", "none"
]

PSEUDO_NEGATIONS = [
    "no wonder", "not only", "not cause for", "without hesitation", "no doubt"
]

# Universal Uncertainty Triggers
UNCERTAINTY_TRIGGERS = [
    "possibly", "possible", "suspected", "suspect", "potential", 
    "questionable", "unclear if", "feels like", "might be", "might have", 
    "maybe", "could be", "borderline", "cannot rule out", "cannot exclude", 
    "evaluating for", "perhaps", "seems like", "feeling a bit of", "unconfirmed"
]
