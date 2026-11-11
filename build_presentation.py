"""Script to update PP2-Presentation-Format (1).pptx with Clinical Triage NLP System content."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette
# -----------------------------------------------------------------------------
NAVY_DARK    = RGBColor(15, 23, 42)      # #0F172A
TEXT_DARK    = RGBColor(30, 41, 59)      # #1E293B
TEXT_MUTED   = RGBColor(100, 116, 139)   # #64748B
BRAND_BLUE   = RGBColor(2, 132, 199)     # #0284C7 (Sky Blue)
BRAND_INDIGO = RGBColor(79, 70, 229)     # #4F46E5
EMERALD_GREEN= RGBColor(16, 185, 129)    # #10B981
EMERALD_DARK = RGBColor(5, 150, 105)     # #059669
ROSE_RED     = RGBColor(225, 29, 72)     # #E11D48
AMBER_ORANGE = RGBColor(217, 119, 6)     # #D97706
BG_LIGHT     = RGBColor(248, 250, 252)   # #F8FAFC
BG_BLUE_TINT = RGBColor(240, 249, 255)   # #F0F9FF
BG_GREEN_TINT= RGBColor(236, 253, 245)   # #ECFDF5
BG_ROSE_TINT = RGBColor(255, 241, 242)   # #FFF1F2
BORDER_GRAY  = RGBColor(226, 232, 240)   # #E2E8F0
WHITE        = RGBColor(255, 255, 255)

FONT_HEADING = "Calibri"
FONT_BODY    = "Calibri"

def clear_content_placeholders(slide):
    """Remove existing content placeholder shape while keeping Title, Logo, Footers."""
    for s in list(slide.shapes):
        if s.name in ['Content Placeholder 2', 'Subtitle 2']:
            sp = s._element
            sp.getparent().remove(sp)

def setup_headers_and_footers(slide, slide_num, title_text, subtitle_text=None):
    """Format Title and update Footers."""
    # Find Title shape
    title_shape = None
    for s in slide.shapes:
        if s.name == 'Title 1':
            title_shape = s
            break

    if title_shape and title_shape.has_text_frame:
        title_shape.left = Inches(0.8)
        title_shape.top = Inches(0.35)
        title_shape.width = Inches(10.2)
        title_shape.height = Inches(0.95)
        tf = title_shape.text_frame
        tf.word_wrap = True
        tf.clear()
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.name = FONT_BODY
            p2.font.size = Pt(11)
            p2.font.bold = False
            p2.font.color.rgb = BRAND_BLUE

    # Update Footer Placeholder
    for s in slide.shapes:
        if 'Footer' in s.name and s.has_text_frame:
            s.text_frame.text = "Clinical Triage NLP System — Department of CSE, BMSCE"
            for p in s.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9)
                p.font.color.rgb = TEXT_MUTED
        elif 'Slide Number' in s.name and s.has_text_frame:
            s.text_frame.text = str(slide_num)
            for p in s.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9)
                p.font.color.rgb = TEXT_MUTED
        elif 'Date' in s.name and s.has_text_frame:
            s.text_frame.text = "2025-2026"
            for p in s.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9)
                p.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=BG_LIGHT, border_color=BORDER_GRAY):
    """Add a card container rectangle with rounded or sharp corners."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()
    return shape

def add_badge(slide, left, top, width, height, text, bg_color=BRAND_BLUE, text_color=WHITE, font_size=10):
    """Add a small badge pill."""
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()
    tf = badge.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_HEADING
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    return badge

# -----------------------------------------------------------------------------
# Main Builder
# -----------------------------------------------------------------------------
def build_deck():
    ppt_path = "PP2-Presentation-Format (1).pptx"
    prs = Presentation(ppt_path)
    print(f"Loaded {ppt_path} with {len(prs.slides)} slides.")

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides[0]
    clear_content_placeholders(s1)
    
    # Title shape
    t1 = [s for s in s1.shapes if s.name == 'Title 1'][0]
    t1.left = Inches(0.8)
    t1.top = Inches(0.9)
    t1.width = Inches(10.0)
    t1.height = Inches(2.2)
    tf1 = t1.text_frame
    tf1.word_wrap = True
    tf1.clear()
    
    p = tf1.paragraphs[0]
    p.text = "Clinical Triage NLP System"
    p.font.name = FONT_HEADING
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p_sub = tf1.add_paragraph()
    p_sub.text = "Turning messy patient narratives into structured, safe, explainable triage"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(16)
    p_sub.font.bold = True
    p_sub.font.color.rgb = BRAND_BLUE

    p_course = tf1.add_paragraph()
    p_course.text = "Natural Language Processing | Course Code: 23CS7PENLP"
    p_course.font.name = FONT_BODY
    p_course.font.size = Pt(12)
    p_course.font.bold = True
    p_course.font.color.rgb = TEXT_MUTED

    # 3 Team Member Cards
    team = [
        ("TEAM MEMBER 1", "Chethan K S", "USN: 1BM23CS074"),
        ("TEAM MEMBER 2", "Bolla Raja Simha", "USN: 1BM23CS070"),
        ("TEAM MEMBER 3", "Irfan Sudarani", "USN: 1BM23CS119")
    ]
    
    card_w = Inches(3.6)
    card_h = Inches(1.8)
    card_top = Inches(3.3)
    start_left = Inches(0.8)
    spacing = Inches(0.4)

    for i, (role, name, usn) in enumerate(team):
        cur_left = start_left + i * (card_w + spacing)
        add_card(s1, cur_left, card_top, card_w, card_h, BG_LIGHT, BORDER_GRAY)
        
        # Text box inside card
        tb = s1.shapes.add_textbox(cur_left + Inches(0.2), card_top + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = role
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = BRAND_BLUE
        
        p1 = tf.add_paragraph()
        p1.text = name
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        
        p2 = tf.add_paragraph()
        p2.text = usn
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED

    # College Department Footer Card
    dept_box = s1.shapes.add_textbox(Inches(0.8), Inches(5.3), Inches(11.6), Inches(0.8))
    dtf = dept_box.text_frame
    dtf.word_wrap = True
    dp1 = dtf.paragraphs[0]
    dp1.text = "Department of Computer Science and Engineering"
    dp1.font.name = FONT_HEADING
    dp1.font.size = Pt(13)
    dp1.font.bold = True
    dp1.font.color.rgb = NAVY_DARK

    dp2 = dtf.add_paragraph()
    dp2.text = "B.M.S. College of Engineering, Bull Temple Road, Bengaluru - 560019"
    dp2.font.name = FONT_BODY
    dp2.font.size = Pt(11)
    dp2.font.color.rgb = TEXT_MUTED

    setup_headers_and_footers(s1, 1, "Clinical Triage NLP System")
    print("Slide 1 formatted.")

    # =========================================================================
    # SLIDE 2: Outline
    # =========================================================================
    s2 = prs.slides[1]
    clear_content_placeholders(s2)
    setup_headers_and_footers(s2, 2, "OUTLINE", "Presentation Agenda & Engineering Overview")

    outline_col1 = [
        ("01", "The Problem & Clinical Urgency", "Messy patient narratives, high-stakes time critical triage"),
        ("02", "Why Existing AI Falls Short", "Generative LLM hallucinations vs legacy classifier blindness"),
        ("03", "Our Solution at a Glance", "5 stages, 5 fields, <100 ms on CPU, 0 hallucinations"),
        ("04", "The 5-Stage Sequential Pipeline", "End-to-end architecture from raw text to physician SBAR note"),
        ("05", "Stage 2: Linguistic NLP Grounding", "Units 2 & 3: Levenshtein DP, WordNet, POS/CFG, Anaphora"),
        ("06", "Stage 3: The 5 Target Clinical Fields", "Strict attribute binding, ConText/NegEx negation & uncertainty")
    ]

    outline_col2 = [
        ("07", "Stage 4 & 5: Laya Engine & SBAR Note", "Non-autoregressive System 1 inference & 4-quadrant NLG note"),
        ("08", "Live Clinical Demo Cases", "Benchmark Neuro, Cardiology NegEx, Levenshtein DP, Anaphora"),
        ("09", "System Architecture & Tech Stack", "FastAPI, Modular NLP Engine, React UI, Pydantic contracts"),
        ("10", "Academic Syllabus Mapping", "Direct alignment with 23CS7PENLP / 23CS8PENLP curriculum"),
        ("11", "SDGs & Healthcare Impact", "SDG 3 (Good Health) & SDG 9 (Infrastructure), hospital collaboration"),
        ("12", "Conclusion & Key Takeaways", "Summary of innovations, clinical safety benefits & engineering rigor")
    ]

    def render_outline_col(slide, items, left, top_start, width):
        for i, (num, title, desc) in enumerate(items):
            cur_top = top_start + i * Inches(0.72)
            add_card(slide, left, cur_top, width, Inches(0.65), BG_LIGHT, BORDER_GRAY)
            
            # Number badge
            add_badge(slide, left + Inches(0.12), cur_top + Inches(0.12), Inches(0.42), Inches(0.4), num, BRAND_BLUE, WHITE, 10)
            
            # Text
            tb = slide.shapes.add_textbox(left + Inches(0.62), cur_top + Inches(0.06), width - Inches(0.7), Inches(0.52))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_HEADING
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = NAVY_DARK

            p_desc = tf.add_paragraph()
            p_desc.text = desc
            p_desc.font.name = FONT_BODY
            p_desc.font.size = Pt(9)
            p_desc.font.color.rgb = TEXT_MUTED

    render_outline_col(s2, outline_col1, Inches(0.8), Inches(1.5), Inches(5.6))
    render_outline_col(s2, outline_col2, Inches(6.8), Inches(1.5), Inches(5.6))
    print("Slide 2 formatted.")

    # =========================================================================
    # SLIDE 3: The Problem
    # =========================================================================
    s3 = prs.slides[2]
    clear_content_placeholders(s3)
    setup_headers_and_footers(s3, 3, "The Problem: Unstructured Clinical Narratives", "Why triage desks and emergency portals struggle with patient free text")

    # Left Card: Typical Patient Input
    add_card(s3, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.5), BG_LIGHT, BORDER_GRAY)
    add_badge(s3, Inches(1.1), Inches(1.75), Inches(2.8), Inches(0.35), "TYPICAL PATIENT INPUT", BRAND_BLUE, WHITE, 11)

    # Quote box
    add_card(s3, Inches(1.1), Inches(2.25), Inches(5.0), Inches(1.6), BG_BLUE_TINT, BRAND_BLUE)
    q_box = s3.shapes.add_textbox(Inches(1.2), Inches(2.35), Inches(4.8), Inches(1.4))
    q_tf = q_box.text_frame
    q_tf.word_wrap = True
    qp = q_tf.paragraphs[0]
    qp.text = "“I’ve had a severe headache for three days, and since this morning I’ve been experiencing nausea and blurred vision.”"
    qp.font.name = FONT_BODY
    qp.font.size = Pt(13)
    qp.font.italic = True
    qp.font.color.rgb = NAVY_DARK

    # Bullets below quote
    b_box = s3.shapes.add_textbox(Inches(1.1), Inches(3.95), Inches(5.0), Inches(1.8))
    b_tf = b_box.text_frame
    b_tf.word_wrap = True

    pts = [
        ("Unstructured & Colloquial:", " Natural patient phrasing mixes timelines, severity descriptors, and multiple symptoms without clear boundaries."),
        ("Noisy & Imperfect:", " Text frequently contains typing typos (headeche, nauesa), informal shorthand, and ambiguous pronouns (it, this).")
    ]
    for i, (b_title, b_desc) in enumerate(pts):
        p = b_tf.paragraphs[0] if i == 0 else b_tf.add_paragraph()
        run1 = p.add_run()
        run1.text = "• " + b_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = BRAND_BLUE
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(11)
        run2.font.color.rgb = TEXT_DARK

    # Right Card: Clinical Challenges
    add_card(s3, Inches(6.8), Inches(1.5), Inches(5.6), Inches(4.5), BG_LIGHT, BORDER_GRAY)
    add_badge(s3, Inches(7.1), Inches(1.75), Inches(3.0), Inches(0.35), "CRITICAL TRIAGE CHALLENGES", ROSE_RED, WHITE, 11)

    r_box = s3.shapes.add_textbox(Inches(7.1), Inches(2.3), Inches(5.0), Inches(3.5))
    r_tf = r_box.text_frame
    r_tf.word_wrap = True

    crit_pts = [
        ("Time-Critical Nature", "Triage staff and emergency nurses must extract actionable clinical fields within seconds to make life-saving routing decisions."),
        ("High-Stakes Safety Boundary", "A missed emergent warning sign (e.g. sudden vision changes with headache) or misclassifying a negation ('no fever') risks patient mortality."),
        ("Zero Room for Hallucination", "Generic AI models that guess or invent unstated severities (e.g. assuming nausea is 'moderate') violate clinical safety protocols."),
        ("Fragmented EHR Handoffs", "Free-text narratives cannot be queried by downstream Electronic Health Record (EHR) diagnostic tools without structured normalization.")
    ]
    for i, (title, desc) in enumerate(crit_pts):
        p = r_tf.paragraphs[0] if i == 0 else r_tf.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = "• " + title + ": "
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = NAVY_DARK
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = TEXT_DARK

    print("Slide 3 formatted.")

    # =========================================================================
    # SLIDE 4: Why Existing AI Falls Short
    # =========================================================================
    s4 = prs.slides[3]
    clear_content_placeholders(s4)
    setup_headers_and_footers(s4, 4, "Why Existing AI Falls Short", "Comparing Generative LLMs, Legacy Token Classifiers, and our Hybrid NLP Pipeline")

    cols = [
        ("Generative LLMs", "GPT-4, Llama, Claude", ROSE_RED, BG_ROSE_TINT, [
            ("Invent details:", "Hallucinates modifiers (e.g. inventing 'moderate nausea' when no severity was given)."),
            ("Blurs urgency with disease:", "Predicts a benign disease label like migraine and inadvertently ignores emergent red flags."),
            ("High latency & resource footprint:", "Requires 2–8 seconds per prompt and expensive GPU clusters, making kiosk intake impractical."),
            ("Privacy risks:", "Sends raw patient clinical data to external cloud APIs.")
        ]),
        ("Legacy Classifiers", "HUMADEX, BioBERT, ClinicalBERT", AMBER_ORANGE, BG_LIGHT, [
            ("Attribute blindness:", "Tags coarse PROBLEM spans, but cannot tell which duration or severity belongs to which symptom."),
            ("Negation failure:", "In 'denies fever', standard token classification still tags 'fever' as an active illness."),
            ("Fixed closed vocabulary:", "Cannot generalize to colloquial terms or open-vocabulary symptom descriptions."),
            ("No clinical synthesis:", "Produces isolated token spans without clinical handoff reports or triage decision routing.")
        ]),
        ("Our Hybrid System", "Classical NLP + Laya Decision", EMERALD_DARK, BG_GREEN_TINT, [
            ("Strict attribute binding:", "Exact modifier binding; unstated severities strictly remain 'unknown' (zero hallucination)."),
            ("Negations & uncertainty kept apart:", "ConText/NegEx scoping isolates pertinent negatives ('denies fever')."),
            ("Ultra-fast on laptop CPU:", "End-to-end inference in <100 ms on standard CPU with calibrated confidence."),
            ("100% on-premise & private:", "Zero external cloud dependencies, fully HIPAA/GDPR compatible.")
        ])
    ]

    col_w = Inches(3.65)
    col_gap = Inches(0.35)
    start_x = Inches(0.8)

    for i, (head, subhead, border_col, bg_col, bullets) in enumerate(cols):
        cx = start_x + i * (col_w + col_gap)
        add_card(s4, cx, Inches(1.5), col_w, Inches(4.5), bg_col, border_col)
        add_badge(s4, cx + Inches(0.2), Inches(1.7), col_w - Inches(0.4), Inches(0.35), head, border_col, WHITE, 11)

        tb = s4.shapes.add_textbox(cx + Inches(0.2), Inches(2.15), col_w - Inches(0.4), Inches(3.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p_sub = tf.paragraphs[0]
        p_sub.text = subhead
        p_sub.font.name = FONT_HEADING
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_MUTED

        for b_title, b_desc in bullets:
            p = tf.add_paragraph()
            p.space_before = Pt(6)
            run1 = p.add_run()
            run1.text = "• " + b_title + " "
            run1.font.bold = True
            run1.font.size = Pt(10)
            run1.font.color.rgb = NAVY_DARK
            run2 = p.add_run()
            run2.text = b_desc
            run2.font.size = Pt(9.5)
            run2.font.color.rgb = TEXT_DARK

    print("Slide 4 formatted.")

    # =========================================================================
    # SLIDE 5: Our Solution at a Glance
    # =========================================================================
    s5 = prs.slides[4]
    clear_content_placeholders(s5)
    setup_headers_and_footers(s5, 5, "Our Solution at a Glance", "High-impact, explainable clinical intelligence decoupled from heavy LLM dependencies")

    # 4 Stat Cards across top
    stats = [
        ("5", "Pipeline Stages", "Sequential end-to-end NLP workflow", BRAND_BLUE),
        ("5", "Target Clinical Fields", "Strictly attribute-bound schema", BRAND_INDIGO),
        ("<100 ms", "Decision Time on CPU", "Ultra-fast System 1 inference", EMERALD_DARK),
        ("0", "Hallucinated Modifiers", "Zero invented clinical ratings", ROSE_RED)
    ]

    stat_w = Inches(2.68)
    stat_gap = Inches(0.32)
    s_x = Inches(0.8)

    for i, (val, label, sub, color) in enumerate(stats):
        cur_x = s_x + i * (stat_w + stat_gap)
        add_card(s5, cur_x, Inches(1.5), stat_w, Inches(1.6), BG_LIGHT, BORDER_GRAY)
        
        tb = s5.shapes.add_textbox(cur_x + Inches(0.15), Inches(1.55), stat_w - Inches(0.3), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_val = tf.paragraphs[0]
        p_val.text = val
        p_val.font.name = FONT_HEADING
        p_val.font.size = Pt(28)
        p_val.font.bold = True
        p_val.font.color.rgb = color
        p_val.alignment = PP_ALIGN.CENTER
        
        p_lbl = tf.add_paragraph()
        p_lbl.text = label
        p_lbl.font.name = FONT_HEADING
        p_lbl.font.size = Pt(11)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = NAVY_DARK
        p_lbl.alignment = PP_ALIGN.CENTER

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.alignment = PP_ALIGN.CENTER

    # Bottom 3 Cards: Architectural Core
    add_card(s5, Inches(0.8), Inches(3.3), Inches(11.6), Inches(2.7), BG_LIGHT, BORDER_GRAY)

    b_tb = s5.shapes.add_textbox(Inches(1.1), Inches(3.45), Inches(11.0), Inches(2.4))
    btf = b_tb.text_frame
    btf.word_wrap = True

    sol_pts = [
        ("Input to Output Contract:", "Messy natural language narrative enters the pipeline → Output produces 5 structured fields, calibrated triage decisions, and an automated SBAR handover note."),
        ("Decoupled Urgency Safety Layer:", "Symptom extraction is decoupled from urgency assessment. For example, a severe headache accompanied by acute blurred vision immediately triggers an emergency protocol, regardless of what disease category is predicted."),
        ("Grounded Classical NLP (Units 2–4):", "Built entirely on proven, interpretable NLP algorithms—Levenshtein dynamic programming, Context-Free Grammars, and Hobbs discourse salience—combined with the Laya decision engine for instant, safe execution.")
    ]
    for i, (title, desc) in enumerate(sol_pts):
        p = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
        p.space_before = Pt(8)
        run1 = p.add_run()
        run1.text = title + " "
        run1.font.name = FONT_HEADING
        run1.font.bold = True
        run1.font.size = Pt(12)
        run1.font.color.rgb = BRAND_BLUE
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = FONT_BODY
        run2.font.size = Pt(11.5)
        run2.font.color.rgb = TEXT_DARK

    print("Slide 5 formatted.")

    # =========================================================================
    # SLIDE 6: The 5-Stage Sequential Pipeline
    # =========================================================================
    s6 = prs.slides[5]
    clear_content_placeholders(s6)
    setup_headers_and_footers(s6, 6, "The 5-Stage Sequential Pipeline", "A disciplined, multi-tier NLP pipeline transforming unstructured narratives into safe clinical assets")

    stages = [
        ("STAGE 1", "Patient Narrative", "Messy free-text paragraph typed by patient or intake desk.", BRAND_BLUE),
        ("STAGE 2", "NLP Grounding", "Levenshtein spellcheck, lemmatization, POS & CFG chunking, pronoun resolution.", BRAND_INDIGO),
        ("STAGE 3", "5-Field Extraction", "Affirmed symptoms, locations, timelines, severities & syndromic pairs.", EMERALD_DARK),
        ("STAGE 4", "Laya Decision", "Clinical disease domain, specialist clinic, and urgency in <100 ms.", AMBER_ORANGE),
        ("STAGE 5", "SBAR Handover", "Auto-synthesized physician note: Situation, Background, Assessment, Rec.", EMERALD_GREEN)
    ]

    st_w = Inches(2.15)
    st_gap = Inches(0.21)
    sx0 = Inches(0.8)

    for i, (badge, title, desc, color) in enumerate(stages):
        cur_x = sx0 + i * (st_w + st_gap)
        add_card(s6, cur_x, Inches(1.5), st_w, Inches(4.5), BG_LIGHT, BORDER_GRAY)
        add_badge(s6, cur_x + Inches(0.15), Inches(1.75), st_w - Inches(0.3), Inches(0.35), badge, color, WHITE, 11)

        tb = s6.shapes.add_textbox(cur_x + Inches(0.15), Inches(2.25), st_w - Inches(0.3), Inches(3.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p_desc = tf.add_paragraph()
        p_desc.space_before = Pt(8)
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = TEXT_DARK

    print("Slide 6 formatted.")

    # =========================================================================
    # SLIDE 7: Stage 2: Linguistic NLP Grounding
    # =========================================================================
    s7 = prs.slides[6]
    clear_content_placeholders(s7)
    setup_headers_and_footers(s7, 7, "Stage 2: Linguistic NLP Grounding", "Implementing core theoretical concepts from Syllabus Units 2 & 3")

    nlp_cards = [
        ("Levenshtein Spellcheck (Unit 2)", BRAND_BLUE, [
            ("Dynamic Programming Matrix:", "Computes Levenshtein and Damerau transposition edit distance token-by-token."),
            ("Normalizes patient typos:", "Automatically repairs typos: headeche → headache, sever → severe, nauesa → nausea, blury → blurry."),
            ("Exact cost accounting:", "Maintains full audit log with edit distance metrics for clinical verification.")
        ]),
        ("WordNet Lemmatization (Unit 2)", BRAND_INDIGO, [
            ("Morphological Parsing:", "Separates inflectional affixes (-ed, -ing, -s) from canonical base roots."),
            ("Preserves valid English:", "Reduces inflected verbs (e.g. started → root start) so grammatical past tenses are never erroneously 'corrected'."),
            ("Lexical verification:", "Leverages WordNet vocabulary to keep clinical descriptions intact.")
        ]),
        ("POS Tagging & CFG Chunks (Unit 2)", EMERALD_DARK, [
            ("Penn Treebank Tagset:", "Tags adjectives (JJ - severity), nouns (NN/NNS - symptoms/locations), and relators (IN/CD - durations)."),
            ("Context-Free Grammar Rules:", "CFG production rules: NP -> Det? Adj* Noun+, PP -> Prep NP."),
            ("Constituency Extraction:", "Identifies clinical noun phrases ('a severe headache') and temporal spans ('for three days').")
        ]),
        ("Anaphora Resolution (Unit 3)", ROSE_RED, [
            ("Hobbs Recency Salience:", "Implements discourse reference resolution for ambiguous pronouns (it, this, that)."),
            ("Cross-Sentence Modifier Binding:", "In 'Patient reports chest pain. It started 3 hours ago.', correctly binds '3 hours' to chest pain."),
            ("Discourse Coherence:", "Eliminates orphaned timelines across sentence boundaries.")
        ])
    ]

    # 2x2 grid
    gw = Inches(5.6)
    gh = Inches(2.15)

    for i, (title, color, bullets) in enumerate(nlp_cards):
        col = i % 2
        row = i // 2
        x = Inches(0.8) + col * Inches(6.0)
        y = Inches(1.5) + row * Inches(2.35)

        add_card(s7, x, y, gw, gh, BG_LIGHT, BORDER_GRAY)
        add_badge(s7, x + Inches(0.2), y + Inches(0.15), gw - Inches(0.4), Inches(0.3), title, color, WHITE, 10.5)

        tb = s7.shapes.add_textbox(x + Inches(0.2), y + Inches(0.5), gw - Inches(0.4), gh - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (b_title, b_desc) in enumerate(bullets):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_before = Pt(3)
            r1 = p.add_run()
            r1.text = "• " + b_title + " "
            r1.font.bold = True
            r1.font.size = Pt(10)
            r1.font.color.rgb = NAVY_DARK
            r2 = p.add_run()
            r2.text = b_desc
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = TEXT_DARK

    print("Slide 7 formatted.")

    # =========================================================================
    # SLIDE 8: Stage 3: The 5 Target Clinical Fields
    # =========================================================================
    s8 = prs.slides[7]
    clear_content_placeholders(s8)
    setup_headers_and_footers(s8, 8, "Stage 3: The 5 Target Clinical Fields", "Core extraction schema preserving exact attribute binding with zero modifier hallucination")

    # Table: 6 rows (1 header + 5 fields), 3 columns
    tbl_shape = s8.shapes.add_table(6, 3, Inches(0.8), Inches(1.5), Inches(11.6), Inches(3.2))
    table = tbl_shape.table
    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(5.0)

    headers = ["Target Field", "Example Extracted Value", "Why It Matters Clinically"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    table_data = [
        ("1. SYMPTOMS", "headache, nausea, blurred vision", "Active confirmed clinical complaints; negations ('no fever') kept strictly apart."),
        ("2. BODY_LOCATION", "head, eyes", "Anatomical mapping that directly routes patients to the appropriate specialist clinic."),
        ("3. DURATION_ONSET", "headache: 3 days, vision: since morning", "Specific timeline per symptom; unstated durations (nausea) strictly remain 'unknown'."),
        ("4. SEVERITY", "headache: severe, nausea: unknown", "Captures reported intensity; never invents ratings for unrated symptoms (zero hallucination)."),
        ("5. ASSOCIATED_SYMPTOMS", "headache with nausea, headache with vision", "Identifies syndromic combinations that trigger emergency triage rules and red flags.")
    ]

    for i, row in enumerate(table_data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_LIGHT if i % 2 == 0 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            if j == 0:
                p.font.bold = True
                p.font.color.rgb = BRAND_BLUE
            elif j == 1:
                p.font.bold = True
                p.font.color.rgb = NAVY_DARK
            else:
                p.font.color.rgb = TEXT_DARK

    # Bottom Callout Card: Negation & Uncertainty Safety
    add_card(s8, Inches(0.8), Inches(4.9), Inches(11.6), Inches(1.2), BG_GREEN_TINT, EMERALD_DARK)
    c_tb = s8.shapes.add_textbox(Inches(1.0), Inches(4.95), Inches(11.2), Inches(1.1))
    ctf = c_tb.text_frame
    ctf.word_wrap = True

    cp1 = ctf.paragraphs[0]
    cr1 = cp1.add_run()
    cr1.text = "🛡️ Critical Assertion Safety Layer: "
    cr1.font.bold = True
    cr1.font.size = Pt(11)
    cr1.font.color.rgb = EMERALD_DARK

    cr2 = cp1.add_run()
    cr2.text = "Negation Preservation (ConText / NegEx): 'No fever' or 'denies chest pain' is isolated into Pertinent Negatives and NEVER becomes a positive finding. "
    cr2.font.size = Pt(10)
    cr2.font.color.rgb = TEXT_DARK

    cp2 = ctf.add_paragraph()
    cr3 = cp2.add_run()
    cr3.text = "Uncertainty Preservation: 'Possibly experiencing dizziness' is isolated into Uncertain Symptoms with an explicit audit trail, protecting clinical safety."
    cr3.font.size = Pt(10)
    cr3.font.color.rgb = TEXT_DARK

    print("Slide 8 formatted.")

    # =========================================================================
    # SLIDE 9: Stage 4 & 5: Laya Engine and SBAR Handover
    # =========================================================================
    s9 = prs.slides[8]
    clear_content_placeholders(s9)
    setup_headers_and_footers(s9, 9, "Stage 4 & 5: Laya Engine and SBAR Handover", "Non-autoregressive decision inference coupled with structured physician note generation")

    # Left: Laya Decision Engine
    add_card(s9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.5), BG_LIGHT, BORDER_GRAY)
    add_badge(s9, Inches(1.1), Inches(1.7), Inches(5.0), Inches(0.35), "STAGE 4: LAYA SYSTEM 1 DECISION ENGINE", AMBER_ORANGE, WHITE, 11)

    l_tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(3.6))
    ltf = l_tb.text_frame
    ltf.word_wrap = True

    laya_pts = [
        ("Non-Autoregressive Architecture:", "Executes in a single forward pass, completely eliminating token-by-token generation overhead."),
        ("Ultra-Low Latency (<100 ms on CPU):", "Processes full clinical syndromes instantly without GPU clusters or cloud dependencies."),
        ("Predicted Clinical Domain:", "Identifies primary medical specialty category (e.g. Neurological / Cerebrovascular, 53.5% confidence)."),
        ("Recommended Department Routing:", "Routes patient directly to appropriate hospital clinic (e.g. Neurology Clinic, 55.1%)."),
        ("Decoupled Urgency Safety Layer:", "Urgency is evaluated independently of disease classification—severe headache with blurred vision triggers Emergency Acuity regardless of benign disease labels.")
    ]
    for i, (btitle, bdesc) in enumerate(laya_pts):
        p = ltf.paragraphs[0] if i == 0 else ltf.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + btitle + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p.add_run()
        r2.text = bdesc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_DARK

    # Right: SBAR Handover Note
    add_card(s9, Inches(6.8), Inches(1.5), Inches(5.6), Inches(4.5), BG_LIGHT, BORDER_GRAY)
    add_badge(s9, Inches(7.1), Inches(1.7), Inches(5.0), Inches(0.35), "STAGE 5: SBAR CLINICAL HANDOVER (UNIT 4 NLG)", EMERALD_DARK, WHITE, 11)

    sbar_quads = [
        ("[S] Situation (Presenting Complaint)", "Patient presents for clinical triage with primary complaint of severe headache, nausea, blurred vision localized to head, eyes.", BRAND_BLUE),
        ("[B] Background (Onset & Timeline)", "Timeline indicates symptom manifestation: headache (3 days); blurred vision (since this morning). Syndromic co-occurrence confirmed.", BRAND_INDIGO),
        ("[A] Assessment (Severity & Negatives)", "Elevated symptom intensity reported for headache. Explicitly denies fever (pertinent negative confirmed).", AMBER_ORANGE),
        ("[R] Recommendation (Routing & Priority)", "Recommended Specialty Route: Neurology Clinic. Triage Priority: EMERGENCY (Immediate Care direct physician evaluation advised).", ROSE_RED)
    ]

    for i, (stitle, sdesc, scolor) in enumerate(sbar_quads):
        qy = Inches(2.2) + i * Inches(0.92)
        add_card(s9, Inches(7.1), qy, Inches(5.0), Inches(0.85), BG_LIGHT, scolor)
        
        qtb = s9.shapes.add_textbox(Inches(7.2), qy + Inches(0.04), Inches(4.8), Inches(0.75))
        qtf = qtb.text_frame
        qtf.word_wrap = True
        
        qp1 = qtf.paragraphs[0]
        qp1.text = stitle
        qp1.font.name = FONT_HEADING
        qp1.font.size = Pt(10)
        qp1.font.bold = True
        qp1.font.color.rgb = scolor

        qp2 = qtf.add_paragraph()
        qp2.text = sdesc
        qp2.font.name = FONT_BODY
        qp2.font.size = Pt(8.5)
        qp2.font.color.rgb = TEXT_DARK

    print("Slide 9 formatted.")

    # =========================================================================
    # SLIDE 10: Live Demo Cases
    # =========================================================================
    s10 = prs.slides[9]
    clear_content_placeholders(s10)
    setup_headers_and_footers(s10, 10, "Live Clinical Demo & Verification Cases", "Tested and verified across challenging linguistic edge cases and distinct medical specialties")

    cases = [
        ("Case 1: Acute Neurological Benchmark", BRAND_BLUE, [
            ("Input:", "“I've had a severe headache for three days, and since this morning I've been experiencing nausea and blurred vision.”"),
            ("Extraction:", "Headache: severe (3 days); Vision: unknown (since this morning); Nausea: unknown (unknown)."),
            ("Clinical Decision:", "Emergency Priority → Neurology Clinic. Zero severity hallucinated for nausea.")
        ]),
        ("Case 2: Cardiology Negation Scoping (NegEx)", ROSE_RED, [
            ("Input:", "“Severe substernal chest pain for 2 hours. Denies fever, no shortness of breath, and no cough.”"),
            ("Extraction:", "Chest pain affirmed; Fever, SOB, Cough isolated into Pertinent Negatives."),
            ("Clinical Decision:", "Emergency Priority → Cardiology Emergency. Prevents positive misdiagnosis.")
        ]),
        ("Case 3: Typo Correction (Levenshtein DP)", AMBER_ORANGE, [
            ("Input:", "“I have sever headeche and nauesa for 2 days. Feeling dizzines and blury vision. Denies feever.”"),
            ("Extraction:", "DP matrix detects and fixes 5 typos before entity extraction."),
            ("Clinical Decision:", "100% extraction accuracy maintained despite noisy patient typing.")
        ]),
        ("Case 4: Cross-Sentence Anaphora Resolution", BRAND_INDIGO, [
            ("Input:", "“Patient reports severe chest pain. It started three hours ago after climbing stairs.”"),
            ("Extraction:", "Hobbs discourse resolver binds pronoun 'It' → 'chest pain'."),
            ("Clinical Decision:", "Correctly attributes 3-hour onset timeline to chest pain across sentence boundary.")
        ])
    ]

    for i, (title, color, bullets) in enumerate(cases):
        col = i % 2
        row = i // 2
        x = Inches(0.8) + col * Inches(6.0)
        y = Inches(1.5) + row * Inches(2.35)

        add_card(s10, x, y, Inches(5.6), Inches(2.15), BG_LIGHT, BORDER_GRAY)
        add_badge(s10, x + Inches(0.2), y + Inches(0.12), Inches(5.2), Inches(0.3), title, color, WHITE, 10.5)

        tb = s10.shapes.add_textbox(x + Inches(0.2), y + Inches(0.48), Inches(5.2), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (b_title, b_desc) in enumerate(bullets):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_before = Pt(3)
            r1 = p.add_run()
            r1.text = b_title + " "
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = NAVY_DARK
            r2 = p.add_run()
            r2.text = b_desc
            r2.font.size = Pt(9)
            r2.font.color.rgb = TEXT_DARK

    print("Slide 10 formatted.")

    # =========================================================================
    # SLIDE 11: Tech Stack and Structure
    # =========================================================================
    s11 = prs.slides[10]
    clear_content_placeholders(s11)
    setup_headers_and_footers(s11, 11, "Tech Stack and Repository Architecture", "Modular engineering with clean decoupled layers, strict schemas, and zero cloud lock-in")

    # Left: Technology Components
    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.5), BG_LIGHT, BORDER_GRAY)
    add_badge(s11, Inches(1.1), Inches(1.7), Inches(5.0), Inches(0.35), "TECHNOLOGY STACK", BRAND_BLUE, WHITE, 11)

    t_box = s11.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.0), Inches(3.6))
    ttf = t_box.text_frame
    ttf.word_wrap = True

    tech_items = [
        ("Backend Framework:", "FastAPI on Python 3.12 (Asynchronous REST API, high throughput, automated OpenAPI docs)."),
        ("NLP Engine Modules:", "Modular Python implementations for spellchecking, POS tagging, discourse resolution, and NLG."),
        ("Decision Engine:", "Laya v0.4.15 non-autoregressive classifier for instant, calibrated clinical triage predictions."),
        ("Lexical Corpora:", "NLTK (WordNet lemmatizer, Penn Treebank pos_tag, RegexpParser CFG chunker)."),
        ("Frontend UI:", "React 18 + TypeScript + Vite + Tailwind CSS (Sequential 5-stage explainable pipeline interface)."),
        ("Data Validation Contracts:", "Pydantic v2 schemas strictly enforcing clinical entity structures and API boundaries.")
    ]
    for i, (b_title, b_desc) in enumerate(tech_items):
        p = ttf.paragraphs[0] if i == 0 else ttf.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + b_title + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY_DARK
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = TEXT_DARK

    # Right: Repository Directory Tree
    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.6), Inches(4.5), NAVY_DARK, BRAND_BLUE)
    add_badge(s11, Inches(7.1), Inches(1.7), Inches(5.0), Inches(0.35), "MODULAR DIRECTORY STRUCTURE", BRAND_INDIGO, WHITE, 11)

    tree_box = s11.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.0), Inches(3.6))
    tr_tf = tree_box.text_frame
    tr_tf.word_wrap = True

    tree_text = """nlp-doc/
├── backend/
│   ├── main.py                     # FastAPI server & routes
│   └── nlp_engine/
│       ├── extractor.py            # Stage 3: Core 5-Field Extractor
│       ├── spell_checker.py        # Unit 2: Levenshtein DP Matrix
│       ├── pos_tagger.py           # Unit 2: POS Tagging & CFG Rules
│       ├── reference_resolver.py   # Unit 3: Discourse Anaphora
│       ├── nlg_generator.py        # Unit 4: SBAR Note Generator
│       ├── laya_service.py         # Stage 4: Laya Decision Engine
│       ├── lexicons.py             # Open-vocabulary knowledge base
│       └── schemas.py              # Pydantic data models
└── frontend/
    └── src/App.tsx                 # 5-Stage Sequential Web UI"""

    tp = tr_tf.paragraphs[0]
    tp.text = tree_text
    tp.font.name = "Consolas"
    tp.font.size = Pt(9.5)
    tp.font.color.rgb = RGBColor(186, 230, 253) # Light sky blue code

    print("Slide 11 formatted.")

    # =========================================================================
    # SLIDE 12: Academic NLP Syllabus Mapping
    # =========================================================================
    s12 = prs.slides[11]
    clear_content_placeholders(s12)
    setup_headers_and_footers(s12, 12, "Academic NLP Syllabus Mapping (23CS7PENLP)", "Rigorous theoretical grounding across core curriculum units")

    syl_units = [
        ("Unit 2: Word Level & Syntactic Analysis", BRAND_BLUE, [
            ("Levenshtein & Damerau Edit Distance:", "DP cost matrix for medical typo detection and correction."),
            ("Morphological Parsing:", "WordNet lemmatizer separating verbal and nominal inflectional affixes."),
            ("Part-of-Speech Tagging:", "Penn Treebank tags (JJ modifiers, NN symptoms, IN relators)."),
            ("CFG Constituency Parsing:", "Context-Free Grammar rules: NP -> Det? Adj* Noun+, PP -> Prep NP.")
        ]),
        ("Unit 3: Semantic Analysis & Discourse Processing", BRAND_INDIGO, [
            ("Pronominal Reference Resolution:", "Hobbs-inspired recency salience algorithm resolving cross-sentence pronouns."),
            ("Discourse Coherence & Structure:", "Linking multi-sentence timelines back to governing clinical entities."),
            ("Clinical Assertion Scoping:", "ConText/NegEx scoping isolating affirmed vs negated findings.")
        ]),
        ("Unit 4: Natural Language Generation (NLG)", EMERALD_DARK, [
            ("Reiter & Dale 3-Tier Architecture:", "Content Determination → Sentence Planning → Surface Realization."),
            ("Clinical Aggregation & Lexical Choice:", "Synthesizing symptoms, severity ratings, and pertinent negatives."),
            ("Structured Clinical Realization:", "Generating standardized SBAR (Situation, Background, Assessment, Recommendation) handovers.")
        ]),
        ("Unit 5: Lexical Resources & Information Extraction", AMBER_ORANGE, [
            ("WordNet Lexical Hierarchy:", "Lemmatization and semantic lexical lookups."),
            ("Clinical Knowledge Base:", "Open-domain canonical medical lexicons spanning major body systems."),
            ("Structured Information Extraction:", "Extracting 5-field target schema from unstructured narratives.")
        ])
    ]

    for i, (title, color, bullets) in enumerate(syl_units):
        col = i % 2
        row = i // 2
        x = Inches(0.8) + col * Inches(6.0)
        y = Inches(1.5) + row * Inches(2.35)

        add_card(s12, x, y, Inches(5.6), Inches(2.15), BG_LIGHT, BORDER_GRAY)
        add_badge(s12, x + Inches(0.2), y + Inches(0.12), Inches(5.2), Inches(0.3), title, color, WHITE, 10.5)

        tb = s12.shapes.add_textbox(x + Inches(0.2), y + Inches(0.48), Inches(5.2), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (b_title, b_desc) in enumerate(bullets):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_before = Pt(3)
            r1 = p.add_run()
            r1.text = "• " + b_title + " "
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = NAVY_DARK
            r2 = p.add_run()
            r2.text = b_desc
            r2.font.size = Pt(9)
            r2.font.color.rgb = TEXT_DARK

    print("Slide 12 formatted.")

    # =========================================================================
    # SLIDE 13: SDGs & Institutional Collaboration
    # =========================================================================
    s13 = prs.slides[12]
    clear_content_placeholders(s13)
    setup_headers_and_footers(s13, 13, "Sustainable Development Goals (SDGs) & Collaboration", "Fulfilling institutional criteria for community-oriented and multidisciplinary healthcare AI")

    sdgs = [
        ("SDG 3: Good Health & Well-being", EMERALD_DARK, [
            ("Target 3.8 - Universal Healthcare Access:", "Delivers rapid, automated pre-triage acuity calculation for under-resourced community health centers and emergency departments."),
            ("Reducing Clinical Diagnostic Delay:", "Instantly extracts critical red flags from patient intake descriptions, preventing fatal delays in acute neurological and cardiac presentations."),
            ("Pertinent Negative Safeguards:", "Prevents misdiagnosis and unnecessary medication by rigorously preserving negative assertions ('denies fever').")
        ]),
        ("SDG 9: Industry, Innovation & Infrastructure", BRAND_BLUE, [
            ("Target 9.5 - Sustainable Local AI:", "Runs 100% on standard commodity CPU hardware without requiring power-hungry GPU server farms."),
            ("Privacy-Preserving Architecture:", "Sensitive patient medical narratives are processed entirely on-premise, guaranteeing strict compliance with patient confidentiality laws (HIPAA/GDPR)."),
            ("High-Throughput Edge Deployment:", "Ideal for low-bandwidth ambulatory clinics, rural telehealth portals, and triage kiosks.")
        ]),
        ("Institutional Collaboration & Deployment", BRAND_INDIGO, [
            ("Hospital Emergency Departments (EDs):", "Automating walk-in intake kiosks to prioritize high-acuity patients before triage nurse evaluation."),
            ("Telemedicine Ambulatory Routing:", "Intelligently directing patient portal messages to appropriate specialty departments without manual clerical overhead."),
            ("EHR Interoperability:", "Outputs standard structured JSON compatible with HL7 / FHIR electronic health record standards.")
        ])
    ]

    for i, (title, color, bullets) in enumerate(sdgs):
        cy = Inches(1.5) + i * Inches(1.5)
        add_card(s13, Inches(0.8), cy, Inches(11.6), Inches(1.35), BG_LIGHT, BORDER_GRAY)
        add_badge(s13, Inches(1.0), cy + Inches(0.12), Inches(4.5), Inches(0.28), title, color, WHITE, 10.5)

        tb = s13.shapes.add_textbox(Inches(1.0), cy + Inches(0.42), Inches(11.2), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (b_title, b_desc) in enumerate(bullets):
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.space_before = Pt(2)
            r1 = p.add_run()
            r1.text = "• " + b_title + " "
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = NAVY_DARK
            r2 = p.add_run()
            r2.text = b_desc
            r2.font.size = Pt(9)
            r2.font.color.rgb = TEXT_DARK

    print("Slide 13 formatted.")

    # =========================================================================
    # SLIDE 14: Key Takeaways
    # =========================================================================
    s14 = prs.slides[13]
    clear_content_placeholders(s14)
    setup_headers_and_footers(s14, 14, "Key Takeaways & Conclusion", "Summary of innovations, engineering rigor, and clinical safety benefits")

    takeaways = [
        ("1. Hybrid Classical NLP Pipeline", "Turns messy free-text narratives into 5 structured clinical fields using interpretable, grounded NLP methods rather than fragile black-box LLMs.", BRAND_BLUE),
        ("2. Patient Safety by Design", "Strict modifier binding prevents hallucinated severities; ConText/NegEx scoping isolates pertinent negatives to protect patient diagnostic safety.", EMERALD_DARK),
        ("3. Decoupled Urgency Safety Layer", "Symptom extraction is decoupled from disease classification so life-threatening red flags are never ignored or masked by benign disease labels.", ROSE_RED),
        ("4. Ultra-Fast CPU Execution (<100 ms)", "Laya non-autoregressive decision engine classifies disease domain, specialty clinic, and urgency in under 100 ms on standard laptop hardware.", AMBER_ORANGE),
        ("5. Ready-to-Use SBAR Handover", "Automated 3-tier NLG generator produces standardized physician notes (Situation, Background, Assessment, Recommendation) for immediate clinical handoff.", BRAND_INDIGO)
    ]

    for i, (title, desc, color) in enumerate(takeaways):
        cy = Inches(1.5) + i * Inches(0.9)
        add_card(s14, Inches(0.8), cy, Inches(11.6), Inches(0.8), BG_LIGHT, BORDER_GRAY)
        add_badge(s14, Inches(1.0), cy + Inches(0.12), Inches(3.2), Inches(0.3), title, color, WHITE, 10.5)

        tb = s14.shapes.add_textbox(Inches(4.4), cy + Inches(0.12), Inches(7.8), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    print("Slide 14 formatted.")

    # =========================================================================
    # SLIDE 15: Thank You & Questions
    # =========================================================================
    s15 = prs.slides[14]
    clear_content_placeholders(s15)
    setup_headers_and_footers(s15, 15, "Thank You!")

    # Centered Thank You Card
    add_card(s15, Inches(2.2), Inches(1.5), Inches(8.8), Inches(4.5), BG_LIGHT, BORDER_GRAY)

    tb = s15.shapes.add_textbox(Inches(2.5), Inches(1.8), Inches(8.2), Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "Thank You!"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = BRAND_BLUE
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "Questions & Discussion"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = NAVY_DARK
    p1.alignment = PP_ALIGN.CENTER

    p_div = tf.add_paragraph()
    p_div.text = "─────────────────────────────────────────"
    p_div.font.size = Pt(10)
    p_div.font.color.rgb = BORDER_GRAY
    p_div.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "PROJECT TEAM MEMBERS:"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = BRAND_INDIGO
    p2.alignment = PP_ALIGN.CENTER

    members = [
        "Chethan K S — USN: 1BM23CS074",
        "Bolla Raja Simha — USN: 1BM23CS070",
        "Irfan Sudarani — USN: 1BM23CS119"
    ]
    for m in members:
        pm = tf.add_paragraph()
        pm.text = m
        pm.font.name = FONT_BODY
        pm.font.size = Pt(12)
        pm.font.bold = True
        pm.font.color.rgb = TEXT_DARK
        pm.alignment = PP_ALIGN.CENTER

    p_dept = tf.add_paragraph()
    p_dept.space_before = Pt(8)
    p_dept.text = "Department of Computer Science & Engineering | B.M.S. College of Engineering"
    p_dept.font.name = FONT_BODY
    p_dept.font.size = Pt(11)
    p_dept.font.color.rgb = TEXT_MUTED
    p_dept.alignment = PP_ALIGN.CENTER

    p_live = tf.add_paragraph()
    p_live.text = "Live Interactive System Running at: http://localhost:8050"
    p_live.font.name = FONT_HEADING
    p_live.font.size = Pt(10.5)
    p_live.font.bold = True
    p_live.font.color.rgb = EMERALD_DARK
    p_live.alignment = PP_ALIGN.CENTER

    print("Slide 15 formatted.")

    # Save presentation
    output_path = "PP2-Presentation-Format (1).pptx"
    prs.save(output_path)
    print(f"Successfully saved updated presentation to {output_path}!")

if __name__ == '__main__':
    build_deck()

