import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Colors
    c_navy_dark = RGBColor(15, 23, 42)      # #0F172A
    c_navy_card = RGBColor(30, 41, 59)      # #1E293B
    c_navy_light = RGBColor(51, 65, 85)     # #334155
    c_blue_accent = RGBColor(37, 99, 235)   # #2563EB
    c_cyan_accent = RGBColor(56, 189, 248)  # #38BDF8
    c_red_accent = RGBColor(239, 68, 68)    # #EF4444
    c_green_accent = RGBColor(34, 197, 94)  # #22C55E
    c_amber_accent = RGBColor(245, 158, 11) # #F59E0B
    c_purple_accent = RGBColor(168, 85, 247)# #A855F7
    c_text_white = RGBColor(255, 255, 255)
    c_text_slate = RGBColor(203, 213, 225)  # #CBD5E1
    c_text_muted = RGBColor(148, 163, 184)  # #94A3B8
    c_white_card = RGBColor(255, 255, 255)
    c_dark_body = RGBColor(30, 41, 59)
    c_light_bg = RGBColor(248, 250, 252)    # #F8FAFC
    c_card_border = RGBColor(226, 232, 240) # #E2E8F0

    def add_bg(slide, dark=False):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_navy_dark if dark else c_light_bg
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, subtitle_text, dark=False):
        # Badge
        tb_badge = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.35))
        tf_b = tb_badge.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = c_cyan_accent if dark else c_blue_accent

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.6))
        tf_t = tb_title.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = c_text_white if dark else c_navy_dark

        # Subtitle
        if subtitle_text:
            tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.4))
            tf_s = tb_sub.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle_text
            p_s.font.size = Pt(13)
            p_s.font.color.rgb = c_text_slate if dark else c_text_muted

    def add_footer(slide, current_page, total_pages=10, dark=False):
        tb_f = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.35))
        tf_f = tb_f.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p = tf_f.paragraphs[0]
        p.text = f"RNAP Hack 2026 · Team 5 (cepesin_chuy) · Track 2: Radio Cumbres · Page {current_page} of {total_pages}"
        p.font.size = Pt(10)
        p.font.color.rgb = c_text_muted if dark else RGBColor(148, 163, 184)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, dark=True)

    # Hero Badge
    tb_badge1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.3), Inches(0.4))
    tf1_b = tb_badge1.text_frame
    p1_b = tf1_b.paragraphs[0]
    p1_b.text = "UANL · EIAO · COMUNICACIÓN INTEGRAL EN INGLÉS TÉCNICO I · ETAPA 4"
    p1_b.font.size = Pt(12)
    p1_b.font.bold = True
    p1_b.font.color.rgb = c_cyan_accent

    # Title
    tb_title1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.4))
    tf1_t = tb_title1.text_frame
    tf1_t.word_wrap = True
    p1_t = tf1_t.paragraphs[0]
    p1_t.text = "Troubleshooting Report & Prototype Audit"
    p1_t.font.size = Pt(36)
    p1_t.font.bold = True
    p1_t.font.color.rgb = c_text_white

    p1_sub = tf1_t.add_paragraph()
    p1_sub.text = "Act. 12 (Team Prototype Audit) & Act. 11 (Developer Reflection) · Stage 4 Evidence"
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = c_amber_accent

    # Two column info cards
    # Card Left: Project Specs
    c_left = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.3), Inches(5.4), Inches(3.2))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = c_navy_card
    c_left.line.color.rgb = c_navy_light
    tf_cl = c_left.text_frame
    tf_cl.margin_left = Inches(0.3)
    tf_cl.margin_top = Inches(0.3)
    
    p = tf_cl.paragraphs[0]
    p.text = "AUDIT SPECIFICATIONS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_cyan_accent
    
    bullets_l = [
        ("Client Station:", "Radio Cumbres (Nuevo León, Mexico)"),
        ("Challenge Track:", "Track 2 · News in 60 Seconds"),
        ("Operational Ceiling:", "Strictly <= 120 words (60s at 2 words/sec)"),
        ("Zero Excess Words:", "100.0% compliance verified across test set"),
        ("Delivery Date:", "Thursday, November 12, 2026"),
        ("Teacher / Evaluator:", "Lic. Jesús Alejandro Juárez González")
    ]
    for label, val in bullets_l:
        p = tf_cl.add_paragraph()
        run1 = p.add_run()
        run1.text = f"{label} "
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = c_text_white
        run2 = p.add_run()
        run2.text = val
        run2.font.size = Pt(11)
        run2.font.color.rgb = c_text_slate

    # Card Right: Team Members
    c_right = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.3), Inches(5.5), Inches(3.2))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = c_navy_card
    c_right.line.color.rgb = c_navy_light
    tf_cr = c_right.text_frame
    tf_cr.margin_left = Inches(0.3)
    tf_cr.margin_top = Inches(0.3)

    p = tf_cr.paragraphs[0]
    p.text = "CONSULTING AUDIT TEAM · TEAM 5"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_green_accent

    team = [
        ("2250704", "GOMEZ MONTES EMILIO ANTONIO", "Lead Engineering & UI"),
        ("2251085", "SANCHEZ GONZALEZ ISRAEL ALEKSANDER", "LoRA Fine-Tuning & Weights"),
        ("2251147", "HERNÁNDEZ CAYETANO KEVIN ADRIÁN", "Corpus Curation & Timing"),
        ("2251441", "PEREZ CEPEDA MIA VALENTINA", "Evaluation & Editorial Audit")
    ]
    for mat, name, role in team:
        p = tf_cr.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {name} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_text_white
        r2 = p.add_run()
        r2.text = f"({mat})\n   Role: {role}"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = c_text_slate

    add_footer(s1, 1, dark=True)

    # -------------------------------------------------------------------------
    # SLIDE 2: Business Case & Consulting Audit Overview
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "EXECUTIVE SUMMARY · RADIO CUMBRES BUSINESS CASE", 
               "Client Context, Core Operational Problem & Audit Scope", 
               "Acting as an independent consulting firm evaluating Prototype v1 for Phase 2 (Checkpoint CP4)")

    # 3 Cards
    # Card 1: The Client Problem
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.6))
    c1.fill.solid()
    c1.fill.fore_color.rgb = c_white_card
    c1.line.color.rgb = c_card_border
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.25)
    p = tf1.paragraphs[0]
    p.text = "1. THE CLIENT PROBLEM"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_red_accent

    p = tf1.add_paragraph()
    p.text = "Morning Show Constraints:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_dark_body

    bullets_c1 = [
        "Radio Cumbres producers must summarize incoming Spanish news stories before 5:00 a.m.",
        "The host has strictly 60 seconds of on-air broadcast time per news story.",
        "At 2 words per second, every story must strictly stay within 120 words.",
        "Previous generic online tools hallucinated unverified figures and ran over the time limit."
    ]
    for b in bullets_c1:
        p = tf1.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(71, 85, 105)

    # Card 2: The Solution Architecture
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.6))
    c2.fill.solid()
    c2.fill.fore_color.rgb = c_white_card
    c2.line.color.rgb = c_card_border
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.25)
    p = tf2.paragraphs[0]
    p.text = "2. PROTOTYPE ARCHITECTURE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_blue_accent

    p = tf2.add_paragraph()
    p.text = "Engineered Technology Stack:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_dark_body

    bullets_c2 = [
        "Model: csebuetnlp/mT5_multilingual_XLSum fine-tuned with PEFT LoRA (r=16, alpha=32).",
        "Corpus: 38,000+ BBC Mundo articles in Spanish from the XL-Sum benchmark.",
        "Baseline: Sentence TF-IDF with lead-bias position weighting.",
        "Fact Guard Engine: Regex and NER cross-matching highlighting ungrounded names/numbers in red."
    ]
    for b in bullets_c2:
        p = tf2.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(71, 85, 105)

    # Card 3: Audit Objectives
    c3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.6))
    c3.fill.solid()
    c3.fill.fore_color.rgb = c_white_card
    c3.line.color.rgb = c_card_border
    tf3 = c3.text_frame
    tf3.margin_left = tf3.margin_right = tf3.margin_top = Inches(0.25)
    p = tf3.paragraphs[0]
    p.text = "3. AUDIT OBJECTIVES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_green_accent

    p = tf3.add_paragraph()
    p.text = "Audit Evaluation Criteria:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_dark_body

    bullets_c3 = [
        "Strict Word Ceiling: Guarantee 0 articles with word excess (> 120 words).",
        "Factual Fidelity: Detect hallucinations before reading numbers on live radio.",
        "Interface Readiness: Gradio v1 connected to live model inference.",
        "Rubric Mastery: Present Perfect (Status), Second Conditional (Solutions), Perfect Conditional (Root Cause)."
    ]
    for b in bullets_c3:
        p = tf3.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(71, 85, 105)

    add_footer(s2, 2)

    # -------------------------------------------------------------------------
    # SLIDE 3: Section 1 · Audit Status (Grammar: Present Perfect)
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "SECTION 1 · AUDIT STATUS · GRAMMAR FOCUS: PRESENT PERFECT", 
               "Current Prototype Milestones & Operational Audit Findings", 
               "Mandatory structures: Present Perfect with already, yet, since, and for (Rubric: >= 4 correct sentences)")

    # Status Box Top
    sb = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.6))
    sb.fill.solid()
    sb.fill.fore_color.rgb = c_white_card
    sb.line.color.rgb = c_card_border
    tfs = sb.text_frame
    tfs.margin_left = tfs.margin_right = tfs.margin_top = Inches(0.3)

    p = tfs.paragraphs[0]
    p.text = "FORMAL PROTOTYPE AUDIT STATEMENT (PRESENT PERFECT STRUCTURES)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = c_blue_accent

    statements = [
        ("1. Dataset & LoRA Training", 
         "Since the show started, Radio Cumbres has required rapid news capsules; our team has fine-tuned the multilingual mT5 model using LoRA adapters on over 3,500 curated Spanish articles."),
        ("2. Operational Word Ceiling", 
         "We have already achieved 100% operational compliance with the 120-word radio ceiling across all 4,763 test articles, and our system has generated zero summaries with excess words."),
        ("3. Airtime Coverage Expansion", 
         "Our prototype has increased the average spoken length from 18.5 words (vanilla mT5) to 89.5 words (fine-tuned model), providing 44.7 seconds of solid news coverage for the morning host."),
        ("4. Engineering Calibration", 
         "The engineering team has worked on decoding hyperparameters for several days to eliminate lexical repetition loops and maintain strict grammatical sentence endings."),
        ("5. Open Risk & Next Steps", 
         "However, our audit reveals that we have not eliminated all named-entity hallucinations in complex international stories yet, which remains our primary engineering priority for Phase 3.")
    ]

    for title, text in statements:
        p = tfs.add_paragraph()
        run_t = p.add_run()
        run_t.text = f"• {title}: "
        run_t.font.bold = True
        run_t.font.size = Pt(12)
        run_t.font.color.rgb = c_navy_dark

        run_body = p.add_run()
        run_body.text = text
        run_body.font.size = Pt(12)
        run_body.font.color.rgb = RGBColor(51, 65, 85)

    add_footer(s3, 3)

    # -------------------------------------------------------------------------
    # SLIDE 4: Section 1 · Quantitative Benchmark & Metrics Table
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "SECTION 1 · TECHNICAL DATA & BENCHMARKS", 
               "Quantitative Evaluation on Test Set (4,763 Articles)", 
               "Real data from notebooks/entrenamiento.ipynb comparing Baseline, Pretrained and Fine-Tuned Transformer")

    # Table Shape
    rows = 4
    cols = 9
    left = Inches(0.8)
    top = Inches(2.0)
    width = Inches(11.733)
    height = Inches(2.8)

    table_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table

    # Column widths
    col_widths = [Inches(2.3), Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.2), Inches(1.1), Inches(1.2), Inches(1.133)]
    for idx, w in enumerate(col_widths):
        tbl.columns[idx].width = w

    headers = ["Model Evaluated", "Approach", "ROUGE-1", "ROUGE-2", "ROUGE-L", "Avg. Words", "Locution", "<= 120 words", "Latency"]
    data = [
        ["1. Base Model (TF-IDF)", "Extractive (Lead Bias)", "0.1719", "0.0339", "0.1115", "113.2 pal.", "56.6 s", "100% (0 ex)", "5.26 ms"],
        ["2. Pretrained (mT5 Vanilla)", "Abstractive (Zero-FT)", "0.2999", "0.1119", "0.2310", "18.5 pal.", "9.2 s", "100% (0 ex)", "220.9 ms"],
        ["3. Solution (mT5 + LoRA)", "Abstractive (Fine-Tuned)", "0.2177", "0.0570", "0.1407", "89.5 pal.", "44.7 s", "100% (0 ex)", "231.6 ms"]
    ]

    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy_dark
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = c_text_white
        p.alignment = PP_ALIGN.CENTER

    for row_idx, row_data in enumerate(data):
        for col_idx, val in enumerate(row_data):
            cell = tbl.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if row_idx % 2 == 1 else c_white_card
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.color.rgb = c_dark_body
            if col_idx in [0, 1]:
                p.alignment = PP_ALIGN.LEFT
            else:
                p.alignment = PP_ALIGN.CENTER
            if col_idx == 7:
                p.font.bold = True
                p.font.color.rgb = c_green_accent

    # Highlight Card Below Table
    hc = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.5))
    hc.fill.solid()
    hc.fill.fore_color.rgb = RGBColor(236, 253, 245) # Mint
    hc.line.color.rgb = RGBColor(167, 243, 208)
    tf_hc = hc.text_frame
    tf_hc.margin_left = tf_hc.margin_right = tf_hc.margin_top = Inches(0.2)

    p = tf_hc.paragraphs[0]
    p.text = "🎯 AUDIT COMPLIANCE HIGHLIGHT: ZERO ARTICLES WITH EXCESS WORDS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(6, 95, 70)

    p = tf_hc.add_paragraph()
    p.text = ("• All three evaluated models achieved 100.0% compliance with Radio Cumbres' operational limit (max <= 120 words).\n"
              "• Zero articles produced word overflow errors. While vanilla mT5 produced brief 18.5-word fragments (9.2 seconds), "
              "our fine-tuned Transformer model successfully achieved an optimal broadcast duration of 44.7 seconds (89.5 words), "
              "effectively resolving the empty on-air time problem.")
    p.font.size = Pt(10.5)
    p.font.color.rgb = RGBColor(4, 120, 87)

    add_footer(s4, 4)

    # -------------------------------------------------------------------------
    # SLIDE 5: Section 2 · Immediate Solutions (Grammar: Second Conditional)
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "SECTION 2 · IMMEDIATE SOLUTIONS · GRAMMAR FOCUS: SECOND CONDITIONAL", 
               "Concrete Actionable Improvements for Current Week (CP4)", 
               "Mandatory structures: Second Conditional (If + Simple Past ... would + Base Verb) · Rubric: >= 2 solutions")

    solutions = [
        ("Solution 1: Fact Guard Entity Cross-Checker", 
         "If we integrated an automated named-entity recognition filter into the generation pipeline, the system would eliminate ungrounded numbers and dates before the host read them on air.",
         "Expected Impact: Factual hallucinations drop by 95%; zero risk of broadcasting incorrect financial or casualty figures."),
        ("Solution 2: Dynamic Token Budget Scaling", 
         "If we calibrated the minimum token threshold dynamically according to input article length, the Transformer would avoid artificial text padding on short news items under 250 words.",
         "Expected Impact: Cleaner phrasing on breaking news briefs and elimination of redundant secondary clauses."),
        ("Solution 3: Repetition Penalty & Beam Tuning", 
         "If we increased the repetition penalty to 1.18 and enforced a 3-gram restriction, the decoder would prevent repetitive lexical loops in legal and political news stories.",
         "Expected Impact: Enhanced oral broadcast cadence and professional radio script quality.")
    ]

    for idx, (title, cond_text, impact) in enumerate(solutions):
        top_pos = Inches(2.0 + idx * 1.55)
        sc = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.4))
        sc.fill.solid()
        sc.fill.fore_color.rgb = c_white_card
        sc.line.color.rgb = c_card_border
        tfs = sc.text_frame
        tfs.margin_left = tfs.margin_right = tfs.margin_top = Inches(0.2)

        p = tfs.paragraphs[0]
        p.text = f"PROPOSED IMPROVEMENT {idx + 1}: {title.upper()}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = c_blue_accent

        p = tfs.add_paragraph()
        r1 = p.add_run()
        r1.text = "Grammar Structure: "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_navy_dark
        r2 = p.add_run()
        r2.text = cond_text
        r2.font.size = Pt(11)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(30, 64, 175)

        p = tfs.add_paragraph()
        r_imp = p.add_run()
        r_imp.text = f"• {impact}"
        r_imp.font.size = Pt(10)
        r_imp.font.color.rgb = RGBColor(71, 85, 105)

    add_footer(s5, 5)

    # -------------------------------------------------------------------------
    # SLIDE 6: Section 3 · Root Cause Analysis (Grammar: Perfect Conditional)
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "SECTION 3 · ROOT CAUSE ANALYSIS · GRAMMAR FOCUS: PERFECT CONDITIONAL", 
               "Audit of Past Engineering Decisions and Counterfactual Effects", 
               "Mandatory structures: Perfect Conditional (If + Past Perfect ... would have + Past Participle) · Rubric: >= 2 causes")

    causes = [
        ("Root Cause 1: Initial Small Synthetic Corpus vs. Full XL-Sum", 
         "If our team had chosen the full 38,000-article XL-Sum Spanish corpus from Phase 1 instead of our initial 120-sample toy dataset, the LoRA adapter would have learned wider journalistic vocabulary much earlier.",
         "Audit Insight: Training on 120 samples limited early generalization, requiring a dataset restructuring in Phase 2."),
        ("Root Cause 2: Unconstrained Early Sequence Decoding", 
         "If we had implemented the sentence-boundary trimming algorithm during our initial baseline experiments, the vanilla mT5 model would not have generated fragmented sentences cut off at arbitrary word limits.",
         "Audit Insight: Rigid word truncation caused syntactically incomplete thoughts, solved via semantic punctuation clipping."),
        ("Root Cause 3: Equal Attention Weights on Numerical Quantities", 
         "If we had supervised cross-attention weights over numeric tokens during preprocessing, the attention mechanism would not have interpolated nearby numerical figures in financial reports.",
         "Audit Insight: Cross-attention averaging caused number hallucinations, necessitating the Fact Guard verification engine.")
    ]

    for idx, (title, cond_text, insight) in enumerate(causes):
        top_pos = Inches(2.0 + idx * 1.55)
        sc = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.4))
        sc.fill.solid()
        sc.fill.fore_color.rgb = c_white_card
        sc.line.color.rgb = c_card_border
        tfs = sc.text_frame
        tfs.margin_left = tfs.margin_right = tfs.margin_top = Inches(0.2)

        p = tfs.paragraphs[0]
        p.text = f"PAST DECISION {idx + 1}: {title.upper()}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = c_red_accent

        p = tfs.add_paragraph()
        r1 = p.add_run()
        r1.text = "Grammar Structure: "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = c_navy_dark
        r2 = p.add_run()
        r2.text = cond_text
        r2.font.size = Pt(11)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(185, 28, 28)

        p = tfs.add_paragraph()
        r_imp = p.add_run()
        r_imp.text = f"• {insight}"
        r_imp.font.size = Pt(10)
        r_imp.font.color.rgb = RGBColor(71, 85, 105)

    add_footer(s6, 6)

    # -------------------------------------------------------------------------
    # SLIDE 7: Prototype Interface v1 Architecture (CP4)
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "PROTOTYPE INTERFACE V1 (CP4) · GRADIO APPLICATION", 
               "Interactive Web App Connected to Model with Fact Guard Protection", 
               "Operational interface built for Phase 2 checkpoint evaluation and live judge demonstration")

    # 4 Module Cards
    modules = [
        ("1. Input Console", 
         "Full-text Spanish news submission area with 1-click test examples for rapid judge testing.", 
         c_blue_accent, 
         ["Textarea for raw articles", "Preset BBC Mundo stories", "Model selector dropdown"]),
        ("2. Multi-Model Inference", 
         "Enables side-by-side comparison between Baseline TF-IDF, Pretrained Zero-FT, and Fine-Tuned Transformer.", 
         c_purple_accent, 
         ["mT5 + LoRA radio summarizer", "TF-IDF lead-bias engine", "Vanilla mT5 headline generator"]),
        ("3. Locution Telemetry", 
         "Live word counter and reading time estimator enforcing Radio Cumbres' strict on-air broadcast window.", 
         c_green_accent, 
         ["Dynamic word counter (/120)", "Locution timer (/60.0 s)", "Zero excess words badge"]),
        ("4. Fact Guard Auditor", 
         "Automatic entity recognition and cross-referencing engine flagging hallucinations in bold red.", 
         c_red_accent, 
         ["Regex number extraction", "Named-entity matching", "Red highlight alert tag"])
    ]

    for idx, (title, desc, color, features) in enumerate(modules):
        left_pos = Inches(0.8 + idx * 2.95)
        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(2.0), Inches(2.8), Inches(4.6))
        c.fill.solid()
        c.fill.fore_color.rgb = c_white_card
        c.line.color.rgb = c_card_border
        tfc = c.text_frame
        tfc.margin_left = tfc.margin_right = tfc.margin_top = Inches(0.2)

        p = tfc.paragraphs[0]
        p.text = title.upper()
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color

        p = tfc.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = c_dark_body

        p = tfc.add_paragraph()
        p.text = "Key Components:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_navy_dark

        for f in features:
            p = tfc.add_paragraph()
            p.text = f"• {f}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = RGBColor(71, 85, 105)

    add_footer(s7, 7)

    # -------------------------------------------------------------------------
    # SLIDE 8: D3 · Act. 11 Developer Reflections
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "D3 · ACT. 11 — DEVELOPER REFLECTION", 
               "Individual & Team Engineering Perspectives on RNAP Hack", 
               "100 to 150 words structured into Real Experiences, An Ideal Present, and A Past Reflection")

    # Two columns: Left (Emilio's Individual Reflection), Right (Team Insights)
    c_emilio = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.6))
    c_emilio.fill.solid()
    c_emilio.fill.fore_color.rgb = c_white_card
    c_emilio.line.color.rgb = c_card_border
    tf_e = c_emilio.text_frame
    tf_e.margin_left = tf_e.margin_right = tf_e.margin_top = Inches(0.25)

    p = tf_e.paragraphs[0]
    p.text = "INDIVIDUAL REFLECTION · EMILIO GÓMEZ (2250704)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_blue_accent

    p = tf_e.add_paragraph()
    r1 = p.add_run()
    r1.text = "1. Real Experiences: "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r2 = p.add_run()
    r2.text = "In RNAP Hack, I have already engineered the TF-IDF sentence extraction baseline and integrated the Gradio interface v1 with Fact Guard protection. However, our team has not tested the live demo with hidden inputs from the judge yet."
    r2.font.size = Pt(10.5)

    p = tf_e.add_paragraph()
    r1 = p.add_run()
    r1.text = "2. An Ideal Present: "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r2 = p.add_run()
    r2.text = "If we had dedicated GPU clusters and more development time, I would build a custom multi-task model capable of generating real-time radio audio synthesis with automated prosody control for radio broadcasters."
    r2.font.size = Pt(10.5)

    p = tf_e.add_paragraph()
    r1 = p.add_run()
    r1.text = "3. A Past Reflection: "
    r1.font.bold = True
    r1.font.size = Pt(11)
    r2 = p.add_run()
    r2.text = "In Phase 1, our team chose a small dataset before switching to full XL-Sum. If we had selected the BBC Mundo corpus from the very beginning, we would have avoided retraining pipelines during checkpoint CP3."
    r2.font.size = Pt(10.5)

    # Right Card: Shared Team Reflections
    c_team = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.6))
    c_team.fill.solid()
    c_team.fill.fore_color.rgb = c_white_card
    c_team.line.color.rgb = c_card_border
    tf_t = c_team.text_frame
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = Inches(0.25)

    p = tf_t.paragraphs[0]
    p.text = "TEAM REFLECTION & KEY LESSONS LEARNED"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_green_accent

    team_points = [
        ("Balancing Metrics vs Utility:", "High ROUGE scores against 20-word headlines do not solve Radio Cumbres' needs. A longer 90-word summary with moderate ROUGE provides far superior on-air broadcast utility."),
        ("Strict Operational Constraints:", "Hard truncating words destroys comprehension. Linguistic boundary clipping (cerrar_oracion_radio) is essential to preserve professional journalism cadence."),
        ("Factual Grounding is Critical:", "In broadcast news, a single invented figure destroys station credibility. Automated entity auditing (Fact Guard) must accompany all generative NLP tools in media environments.")
    ]

    for title, desc in team_points:
        p = tf_t.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = RGBColor(71, 85, 105)

    add_footer(s8, 8)

    # -------------------------------------------------------------------------
    # SLIDE 9: 2-Minute Oral Presentation Pitch ("Audit Status Oral")
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "AUDIT STATUS ORAL · 2-MINUTE PRESENTATION SCRIPT", 
               "Timed Speaking Guide for Group Presentation in English Class", 
               "Structured delivery roadmap for delivering the 120-second audit pitch with maximum fluency")

    # 3 Column Timeline Cards
    times = [
        ("Part 1: Audit Status (0:00 - 0:40)", 
         c_blue_accent, 
         "Present Perfect Focus", 
         [
             "\"Good morning. As an audit consulting firm, we have evaluated prototype v1 for Radio Cumbres.\"",
             "\"Since the start of Phase 2, our team has fine-tuned the multilingual mT5 Transformer using LoRA adapters.\"",
             "\"We have already achieved 100% compliance with the 120-word ceiling across all 4,763 test articles.\"",
             "\"However, we have not eliminated all entity hallucinations in complex articles yet.\""
         ]),
        ("Part 2: Immediate Solutions (0:40 - 1:20)", 
         c_purple_accent, 
         "Second Conditional Focus", 
         [
             "\"To resolve these audit findings, we propose two concrete engineering solutions this week:\"",
             "\"First, if we integrated a named-entity regex filter into decoding, the model would eliminate 95% of hallucinated figures before broadcast.\"",
             "\"Second, if we raised the repetition penalty to 1.18, the decoder would prevent repetitive phrases in legal and political stories.\""
         ]),
        ("Part 3: Root Cause & Roadmap (1:20 - 2:00)", 
         c_amber_accent, 
         "Perfect Conditional Focus", 
         [
             "\"Reflecting on past decisions, if we had adopted the full 38,000-article XL-Sum corpus in Phase 1, our adapter would have converged much faster.\"",
             "\"And if we had implemented sentence boundary clipping earlier, vanilla mT5 would not have generated truncated fragments.\"",
             "\"Our prototype is 100% operational, fully audited, and ready for Phase 3. Thank you.\""
         ])
    ]

    for idx, (title, color, badge, script_lines) in enumerate(times):
        left_pos = Inches(0.8 + idx * 3.95)
        c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(2.0), Inches(3.8), Inches(4.6))
        c.fill.solid()
        c.fill.fore_color.rgb = c_white_card
        c.line.color.rgb = c_card_border
        tfc = c.text_frame
        tfc.margin_left = tfc.margin_right = tfc.margin_top = Inches(0.2)

        p = tfc.paragraphs[0]
        p.text = title.upper()
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color

        p = tfc.add_paragraph()
        p.text = f"[{badge}]"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = c_navy_dark

        for line in script_lines:
            p = tfc.add_paragraph()
            p.text = line
            p.font.size = Pt(10)
            p.font.color.rgb = RGBColor(71, 85, 105)

    add_footer(s9, 9)

    # -------------------------------------------------------------------------
    # SLIDE 10: Conclusion & Roadmap to Phase 3 (PIA v1.0)
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10, dark=True)

    tb_end = s10.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.2))
    tfe = tb_end.text_frame
    p = tfe.paragraphs[0]
    p.text = "Audit Verdict & Roadmap to Phase 3 (PIA)"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = c_text_white

    p2 = tfe.add_paragraph()
    p2.text = "Prototype v1 has successfully passed all Phase 2 operational and technical requirements."
    p2.font.size = Pt(16)
    p2.font.color.rgb = c_green_accent

    # Bottom summary box
    sc_end = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.0), Inches(11.3), Inches(3.5))
    sc_end.fill.solid()
    sc_end.fill.fore_color.rgb = c_navy_card
    sc_end.line.color.rgb = c_navy_light
    tf_end = sc_end.text_frame
    tf_end.margin_left = tf_end.margin_right = tf_end.margin_top = Inches(0.3)

    summary_bullets = [
        ("Operational Feasibility:", "100.0% adherence to Radio Cumbres' <= 120 words window (0 excess words) with average 44.7 seconds on-air coverage."),
        ("Interface Completeness:", "Gradio v1 application deployed with multi-model comparison, live word telemetry, and Fact Guard red highlighting."),
        ("Factual Protection:", "Automated entity cross-matching prevents the broadcast of hallucinated amounts, dates, or casualty numbers."),
        ("Phase 3 Deliverables (Thu Nov 19):", "Tagging git release v1.0, preparing the live demo with unexpected judge articles, and delivering the final 20-minute product presentation.")
    ]

    for label, text in summary_bullets:
        p = tf_end.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {label} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = c_cyan_accent
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(12)
        r2.font.color.rgb = c_text_slate

    add_footer(s10, 10, dark=True)

    # Save presentation
    out_path_1 = r"C:\Users\emili\Desktop\cepechuy\cepesin_chuy\RNAP_Hack_2026_English_Nov12_Troubleshooting_Report.pptx"
    out_path_2 = r"C:\Users\emili\Desktop\cepechuy\cepesin_chuy\EA_Act12_Troubleshooting_Report_Team5.pptx"
    prs.save(out_path_1)
    prs.save(out_path_2)
    print("Saved presentation to:", out_path_1)
    print("Saved presentation copy to:", out_path_2)

if __name__ == "__main__":
    create_deck()
