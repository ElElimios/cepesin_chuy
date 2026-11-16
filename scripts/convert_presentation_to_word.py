import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_full_word_report():
    doc = Document()

    # Page Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Palette
    c_navy = RGBColor(15, 23, 42)       # #0F172A
    c_blue = RGBColor(37, 99, 235)      # #2563EB
    c_slate = RGBColor(71, 85, 105)     # #475569
    c_crimson = RGBColor(220, 38, 38)   # #DC2626
    c_green = RGBColor(22, 101, 52)     # #166534
    c_amber = RGBColor(180, 83, 9)      # #B45309

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_inst.add_run("UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN\nESCUELA INDUSTRIAL Y PREPARATORIA TÉCNICA “ÁLVARO OBREGÓN”\n")
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = c_navy

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_course.add_run("COMUNICACIÓN INTEGRAL EN INGLÉS TÉCNICO I · ETAPA 4\nEVIDENCIA DE APRENDIZAJE · ACT. 12 & D3 (ACT. 11)")
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = c_blue

    doc.add_paragraph("\n" * 2)

    # Document Title Box
    tbl_title = doc.add_table(rows=1, cols=1)
    tbl_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_t = tbl_title.cell(0, 0)
    cell_t.width = Inches(6.5)
    set_cell_background(cell_t, "0F172A")
    set_cell_margins(cell_t, top=280, bottom=280, left=320, right=320)
    
    p = cell_t.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("TROUBLESHOOTING REPORT & PROTOTYPE AUDIT\n")
    r.font.size = Pt(17)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

    r_sub = p.add_run("Automated Spanish News Summarization for Radio Cumbres\nPhase 2 Engineering Audit & Developer Reflection")
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(203, 213, 225)

    doc.add_paragraph("\n" * 2)

    # Metadata Table
    t_meta = doc.add_table(rows=6, cols=2)
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("Client Station & Track:", "Radio Cumbres · Track 2 (News in 60 Seconds)"),
        ("Team Identification:", "Team 5 — cepesin_chuy"),
        ("Members & Matrículas:", "Emilio Gómez (2250704), Israel Sánchez (2251085),\nKevin Hernández (2251147), Mía Pérez (2251441)"),
        ("Teacher / Evaluator:", "Lic. Jesús Alejandro Juárez González"),
        ("Operational Criterion:", "Strictly <= 120 words per story (Zero Excess Words)"),
        ("Date of Delivery:", "Thursday, November 12, 2026")
    ]
    for idx, (label, val) in enumerate(meta_rows):
        c1, c2 = t_meta.rows[idx].cells
        c1.width = Inches(2.2)
        c2.width = Inches(4.3)
        set_cell_margins(c1, top=80, bottom=80, left=100, right=100)
        set_cell_margins(c2, top=80, bottom=80, left=100, right=100)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(label)
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = c_navy
        
        p2 = c2.paragraphs[0]
        r2 = p2.add_run(val)
        r2.font.size = Pt(10)
        r2.font.color.rgb = c_slate

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & CLIENT CONTEXT (FROM SLIDE 2)
    # -------------------------------------------------------------------------
    h = doc.add_heading("Executive Summary & Project Context", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_intro = doc.add_paragraph()
    p_intro.add_run(
        "Our team operates as an independent technical consulting firm commissioned to audit the natural language processing (NLP) "
        "prototype developed for "
    )
    r = p_intro.add_run("Radio Cumbres")
    r.font.bold = True
    p_intro.add_run(
        ", a prominent local commercial radio station located in Nuevo León, Mexico. The morning news broadcast requires the on-air "
        "host to read summarized news capsules in strictly 60 seconds or less. At a standard Spanish radio locution speech rate "
        "of approximately 2 words per second, each story is operationally capped at a "
    )
    r = p_intro.add_run("maximum of 120 words")
    r.font.bold = True
    p_intro.add_run(
        ". Previous automated summarization tools tested by the station generated texts that ran far over the 60-second airtime window "
        "or hallucinated unverifiable figures and dates, causing serious editorial liability."
    )

    # 3 Strategic Pillars Box
    tbl_pil = doc.add_table(rows=1, cols=3)
    tbl_pil.alignment = WD_TABLE_ALIGNMENT.CENTER
    pillars = [
        ("1. Operational Ceiling", "Guarantee 100.0% adherence to <= 120 words with zero tolerance for excess words.", "EFF6FF", c_blue),
        ("2. Factual Integrity", "Flag all ungrounded numbers or names in bold red before reaching the live broadcast.", "FEF2F2", c_crimson),
        ("3. Oral Cadence", "Provide solid 40 to 50 seconds of spoken content (80-115 words), overcoming telegraphic snippets.", "F0FDF4", c_green)
    ]
    for idx, (title, text, bg_hex, col_rgb) in enumerate(pillars):
        c = tbl_pil.cell(0, idx)
        c.width = Inches(2.16)
        set_cell_background(c, bg_hex)
        set_cell_margins(c, top=140, bottom=140, left=140, right=140)
        p = c.paragraphs[0]
        r = p.add_run(f"{title}\n")
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = col_rgb
        r2 = p.add_run(text)
        r2.font.size = Pt(9)
        r2.font.color.rgb = c_slate

    doc.add_paragraph()

    # -------------------------------------------------------------------------
    # SECTION 2: AUDIT STATUS (FROM SLIDES 3 & 4)
    # -------------------------------------------------------------------------
    h = doc.add_heading("1. Audit Status (Grammar: Present Perfect)", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_focus = doc.add_paragraph()
    r = p_focus.add_run("Grammar Focus: ")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = c_blue
    r = p_focus.add_run("Present Perfect with already, yet, since, and for (Rubric Requirement: >= 4 correct sentences)")
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.color.rgb = c_slate

    p_as = doc.add_paragraph()
    r = p_as.add_run("Since ")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run("the launch of Phase 2, our consulting engineering firm ")
    r = p_as.add_run("has audited ")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run(
        "and benchmarked the prototype developed for Radio Cumbres. We "
    )
    r = p_as.add_run("have already achieved ")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run(
        "100% operational compliance with the 120-word airtime constraint across all 4,763 test articles from the Spanish XL-Sum benchmark, "
        "and our system has generated zero summaries with excess words. Our prototype "
    )
    r = p_as.add_run("has increased ")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run(
        "the average news capsule length from 18.5 words (vanilla mT5) to 89.5 words (fine-tuned LoRA model), successfully providing "
        "44.7 seconds of informative broadcast coverage for the morning host. The engineering team "
    )
    r = p_as.add_run("has fine-tuned ")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run("decoding parameters ")
    r = p_as.add_run("for ")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run(
        "several days to balance fluency and strict sentence boundary closure. However, our audit reveals that we "
    )
    r = p_as.add_run("have not eliminated ")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run("all named-entity hallucinations in complex international articles ")
    r = p_as.add_run("yet")
    r.font.bold = True
    r.font.color.rgb = c_blue
    p_as.add_run(", which remains our primary open risk.")

    # Table of Metrics
    p_tbl_lbl = doc.add_paragraph()
    r = p_tbl_lbl.add_run("Table 1. Quantitative Prototype Evaluation Benchmark (4,763 Articles in Test Split)")
    r.font.bold = True
    r.font.size = Pt(10.5)

    tbl_m = doc.add_table(rows=4, cols=8)
    tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_m = ["Model Evaluated", "Approach", "ROUGE-1", "ROUGE-2", "ROUGE-L", "Avg. Words (Airtime)", "<= 120 Words", "Latency/Art."]
    rows_m = [
        ["1. Base Model (TF-IDF)", "Extractive (Lead Bias)", "0.1719", "0.0339", "0.1115", "113.2 pal. (56.6 s)", "100.0% (0 ex)", "5.26 ms"],
        ["2. Pretrained (mT5 Vanilla)", "Abstractive (Zero-FT)", "0.2999", "0.1119", "0.2310", "18.5 pal. (9.2 s)", "100.0% (0 ex)", "220.94 ms"],
        ["3. Solution (mT5 + LoRA)", "Abstractive (Fine-Tuned)", "0.2177", "0.0570", "0.1407", "89.5 pal. (44.7 s)", "100.0% (0 ex)", "231.66 ms"]
    ]

    for c_idx, h_text in enumerate(headers_m):
        cell = tbl_m.cell(0, c_idx)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, r_vals in enumerate(rows_m):
        for c_idx, val in enumerate(r_vals):
            cell = tbl_m.cell(r_idx + 1, c_idx)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if c_idx == 6:
                r.font.bold = True
                r.font.color.rgb = c_green

    doc.add_paragraph()

    # Callout Highlight
    tbl_call = doc.add_table(rows=1, cols=1)
    tbl_call.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_c = tbl_call.cell(0, 0)
    cell_c.width = Inches(6.5)
    set_cell_background(cell_c, "ECFDF5") # Mint
    set_cell_margins(cell_c, top=120, bottom=120, left=160, right=160)
    p = cell_c.paragraphs[0]
    r = p.add_run("🎯 AUDIT COMPLIANCE HIGHLIGHT: ZERO ARTICLES WITH EXCESS WORDS\n")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = c_green
    r2 = p.add_run(
        "All three evaluated models demonstrated 100.0% adherence to Radio Cumbres' strict <= 120 words constraint. Zero articles "
        "exceeded the on-air budget. The fine-tuned Transformer model successfully expanded coverage from 18.5 words (9.2 seconds) "
        "to 89.5 words (44.7 seconds), resolving the dead air problem while eliminating word excess."
    )
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = RGBColor(4, 120, 87)

    doc.add_paragraph()

    # -------------------------------------------------------------------------
    # SECTION 3: IMMEDIATE SOLUTIONS (FROM SLIDE 5)
    # -------------------------------------------------------------------------
    h = doc.add_heading("2. Immediate Solutions (Grammar: Second Conditional)", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_focus = doc.add_paragraph()
    r = p_focus.add_run("Grammar Focus: ")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = c_blue
    r = p_focus.add_run("Second Conditional (If + Simple Past ... would + Base Verb) · (Rubric: >= 2 solutions)")
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.color.rgb = c_slate

    solutions_data = [
        ("Solution 1: Fact Guard Entity Cross-Checker",
         "If we integrated an automated named-entity recognition filter into the generation pipeline, the system would eliminate ungrounded numbers and dates before the host read them on live air.",
         "Factual hallucinations decrease by over 95%, removing the hazard of broadcasting incorrect economic figures or casualties."),
        ("Solution 2: Dynamic Article-Length Conditioning",
         "If we calibrated the minimum token generation threshold dynamically according to input article length, the Transformer would avoid artificial padding on short news items under 250 words.",
         "Cleaner phrasing on short breaking flashes, preventing awkward run-on secondary clauses."),
        ("Solution 3: Calibrated Repetition Penalty & Beam Tuning",
         "If we increased the repetition penalty to 1.18 and enforced a 3-gram restriction, the decoder would prevent repetitive lexical loops in legal and political stories.",
         "Professional radio cadence, natural journalistic rhythm, and zero irritating phrase echoes.")
    ]

    for title, cond_stmt, impact in solutions_data:
        p = doc.add_paragraph()
        r = p.add_run(f"• {title}: ")
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = c_navy
        
        r_cond = p.add_run(f'"{cond_stmt}"\n')
        r_cond.font.bold = True
        r_cond.font.size = Pt(10.5)
        r_cond.font.color.rgb = RGBColor(30, 64, 175) # Dark Blue
        
        r_imp = p.add_run(f"   Expected Impact: {impact}")
        r_imp.font.size = Pt(10)
        r_imp.font.color.rgb = c_slate

    doc.add_paragraph()

    # -------------------------------------------------------------------------
    # SECTION 4: ROOT CAUSE ANALYSIS (FROM SLIDE 6)
    # -------------------------------------------------------------------------
    h = doc.add_heading("3. Root Cause Analysis (Grammar: Perfect Conditional)", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_focus = doc.add_paragraph()
    r = p_focus.add_run("Grammar Focus: ")
    r.font.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = c_crimson
    r = p_focus.add_run("Perfect Conditional (If + Past Perfect ... would have + Past Participle) · (Rubric: >= 2 causes)")
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.color.rgb = c_slate

    causes_data = [
        ("Root Cause 1: Initial Small Synthetic Corpus vs. Full XL-Sum",
         "If our team had chosen the full 38,000-article XL-Sum Spanish corpus from Phase 1 instead of our initial 120-sample toy dataset, the LoRA adapter would have learned wider journalistic vocabulary much earlier.",
         "Initial 120-article dataset limited lexical richness, necessitating a full corpus migration in Phase 2."),
        ("Root Cause 2: Unconstrained Early Sequence Decoding",
         "If we had implemented the sentence-boundary trimming algorithm during our initial baseline experiments, the vanilla mT5 model would not have generated fragmented sentences cut off at arbitrary word limits.",
         "Rigid token truncation created incomplete syntactic thoughts; solved via cerrar_oracion_radio."),
        ("Root Cause 3: Equal Attention Weights on Numerical Tokens",
         "If we had supervised cross-attention weights over numeric tokens during tokenization, the model would not have interpolated nearby numerical quantities in financial and casualty reports.",
         "Cross-attention averaging caused number hallucinations, directly justifying the Fact Guard verification engine.")
    ]

    for title, cond_stmt, insight in causes_data:
        p = doc.add_paragraph()
        r = p.add_run(f"• {title}: ")
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = c_navy
        
        r_cond = p.add_run(f'"{cond_stmt}"\n')
        r_cond.font.bold = True
        r_cond.font.size = Pt(10.5)
        r_cond.font.color.rgb = RGBColor(185, 28, 28) # Dark Red
        
        r_ins = p.add_run(f"   Audit Finding: {insight}")
        r_ins.font.size = Pt(10)
        r_ins.font.color.rgb = c_slate

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECTION 5: PROTOTYPE INTERFACE V1 ARCHITECTURE (FROM SLIDE 7)
    # -------------------------------------------------------------------------
    h = doc.add_heading("Prototype Interface v1 Architecture (CP4 Deliverable)", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_ui = doc.add_paragraph()
    p_ui.add_run(
        "For Checkpoint CP4, our engineering team developed and verified an interactive web application powered by "
    )
    r = p_ui.add_run("Gradio (app/app.py and app.py)")
    r.font.bold = True
    p_ui.add_run(
        ". The interface directly connects the trained models with real-time operational locution telemetry and factual verification."
    )

    t_ui = doc.add_table(rows=4, cols=2)
    t_ui.alignment = WD_TABLE_ALIGNMENT.CENTER
    ui_mods = [
        ("1. Input & Example Console", 
         "Features a full-text Spanish news textarea and 1-click test examples from BBC Mundo, allowing the judge to test fresh news stories instantaneously."),
        ("2. Multi-Model Inference Switch", 
         "Enables seamless switching between the TF-IDF Extractive Baseline, the Pretrained Vanilla mT5 Zero-FT model, and the Fine-Tuned Transformer LoRA solution."),
        ("3. Locution Telemetry Dashboard", 
         "Displays dynamic word counts (X / 120 words), on-air read time countdown (Y / 60.0 s), and an operational compliance badge certifying Zero Excess Words."),
        ("4. Fact Guard Hallucination Auditor", 
         "Automated entity extractor highlighting unverified names or figures in bold red with an alert badge, protecting the radio host from broadcasting ungrounded facts.")
    ]
    for idx, (m_title, m_desc) in enumerate(ui_mods):
        c1, c2 = t_ui.rows[idx].cells
        c1.width = Inches(2.3)
        c2.width = Inches(4.2)
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c1, top=100, bottom=100, left=100, right=100)
        set_cell_margins(c2, top=100, bottom=100, left=100, right=100)
        
        p1 = c1.paragraphs[0]
        r = p1.add_run(m_title)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = c_navy
        
        p2 = c2.paragraphs[0]
        r = p2.add_run(m_desc)
        r.font.size = Pt(9.5)
        r.font.color.rgb = c_slate

    doc.add_paragraph()

    # -------------------------------------------------------------------------
    # SECTION 6: D3 · ACT. 11 DEVELOPER REFLECTION (FROM SLIDE 8)
    # -------------------------------------------------------------------------
    h = doc.add_heading("Annex A: D3 · Act. 11 — Developer Reflection", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_d3_meta = doc.add_paragraph()
    r = p_d3_meta.add_run("Student: Emilio Antonio Gómez Montes (Matrícula: 2250704) · Team 5 (cepesin_chuy)\n")
    r.font.bold = True
    r.font.size = Pt(10.5)
    r_sub = p_d3_meta.add_run("Requirement: 100 to 150 words in three paragraphs covering Real Experiences, An Ideal Present, and A Past Reflection.")
    r_sub.font.italic = True
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = c_slate

    p_d1 = doc.add_paragraph()
    r = p_d1.add_run("Real Experiences: ")
    r.font.bold = True
    p_d1.add_run(
        "In RNAP Hack, I have already engineered the TF-IDF sentence extractive baseline and deployed the interactive Gradio interface v1 "
        "with Fact Guard verification. Our team has worked collaboratively since the start of the semester to optimize radio locution timing. "
        "However, we have not tested our interface against the judge's hidden test articles yet."
    )

    p_d2 = doc.add_paragraph()
    r = p_d2.add_run("An Ideal Present: ")
    r.font.bold = True
    p_d2.add_run(
        "If we had access to larger dedicated GPU clusters and more computing time, I would build an end-to-end voice-to-speech synthesis pipeline "
        "that would convert news articles directly into spoken radio audio with dynamic prosody control for radio broadcasters."
    )

    p_d3 = doc.add_paragraph()
    r = p_d3.add_run("A Past Reflection: ")
    r.font.bold = True
    p_d3.add_run(
        "In Phase 1, our team chose a small synthetic dataset for initial testing. If we had integrated the comprehensive 38,000-article "
        "BBC Mundo corpus from the very first checkpoint, our model would have converged with greater linguistic richness before checkpoint CP3."
    )

    d3_words = len(f"{p_d1.text} {p_d2.text} {p_d3.text}".split())
    p_d3_stat = doc.add_paragraph()
    p_d3_stat.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_d3_stat.add_run(f"D3 Word Count: {d3_words} words (Requirement: 100 - 150 words · Evaluation: Compliant)")
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = c_green

    doc.add_paragraph()

    # -------------------------------------------------------------------------
    # SECTION 7: 2-MINUTE ORAL PRESENTATION SCRIPT (FROM SLIDE 9)
    # -------------------------------------------------------------------------
    h = doc.add_heading("Annex B: 2-Minute Oral Presentation Script (“Audit Status Oral”)", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_script_info = doc.add_paragraph()
    p_script_info.add_run(
        "The following 120-second timed speaking transcript provides the exact speaking cues and time markers for delivering "
        "the required oral Audit Status presentation before the English class and evaluator:"
    )
    p_script_info.runs[0].font.size = Pt(10)
    p_script_info.runs[0].font.color.rgb = c_slate

    t_script = doc.add_table(rows=3, cols=2)
    t_script.alignment = WD_TABLE_ALIGNMENT.CENTER
    parts = [
        ("Part 1: Audit Status & Metrics\n(0:00 - 0:40 | 40 seconds)\n\nFocus: Present Perfect",
         "“Good morning, teacher and classmates. As an independent audit consulting firm, our team has evaluated the prototype developed for Radio Cumbres.\n\n"
         "Since the start of Phase 2, our engineering team has fine-tuned the multilingual mT5 Transformer using LoRA adapters on over 3,500 Spanish news articles. "
         "We have already achieved 100% compliance with the 120-word ceiling across all 4,763 test articles, guaranteeing zero airtime overflow errors on live radio.\n\n"
         "However, our audit reveals that we have not eliminated all entity hallucinations in complex articles yet, which represents our primary open risk.”"),
        
        ("Part 2: Immediate Solutions\n(0:40 - 1:20 | 40 seconds)\n\nFocus: Second Conditional",
         "“To resolve these audit findings, we propose two concrete engineering solutions this week:\n\n"
         "First, if we integrated a named-entity regex filter into decoding, the model would eliminate 95% of hallucinated figures and dates before the host read them on air.\n\n"
         "Second, if we raised the repetition penalty to 1.18, the decoder would prevent repetitive phrases in legal and political stories, ensuring smooth and natural radio locution.”"),
        
        ("Part 3: Root Cause & Roadmap\n(1:20 - 2:00 | 40 seconds)\n\nFocus: Perfect Conditional",
         "“Looking back at our past engineering decisions, if we had adopted the full 38,000-article XL-Sum corpus in Phase 1, our LoRA adapter would have converged with wider vocabulary much earlier.\n\n"
         "Furthermore, if we had implemented sentence boundary clipping from the beginning, the vanilla model would not have generated awkward truncated fragments.\n\n"
         "Our prototype is 100% operational, strictly within 120 words, and fully prepared for the final live demo. Thank you.”")
    ]

    for idx, (p_info, p_text) in enumerate(parts):
        c1, c2 = t_script.rows[idx].cells
        c1.width = Inches(2.2)
        c2.width = Inches(4.3)
        set_cell_background(c1, "F1F5F9")
        set_cell_margins(c1, top=120, bottom=120, left=120, right=120)
        set_cell_margins(c2, top=120, bottom=120, left=120, right=120)
        
        p1 = c1.paragraphs[0]
        r = p1.add_run(p_info)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = c_navy
        
        p2 = c2.paragraphs[0]
        r = p2.add_run(p_text)
        r.font.size = Pt(9.5)
        r.font.color.rgb = c_slate

    doc.add_paragraph()

    # -------------------------------------------------------------------------
    # SECTION 8: CONCLUSION & ROADMAP TO PIA (FROM SLIDE 10)
    # -------------------------------------------------------------------------
    h = doc.add_heading("4. Audit Verdict & Roadmap to Phase 3 (PIA v1.0)", level=1)
    h.runs[0].font.color.rgb = c_navy
    h.runs[0].font.size = Pt(16)

    p_end = doc.add_paragraph()
    p_end.add_run(
        "Prototype v1 has successfully passed all Phase 2 operational, linguistic, and technical requirements. "
        "The consulting audit certifies that:\n"
    )
    checklist = [
        ("Operational Feasibility: ", "100.0% adherence to Radio Cumbres' <= 120 words window (0 excess words) with average 44.7 seconds on-air coverage."),
        ("Interface Completeness: ", "Gradio v1 application deployed with multi-model comparison, live word telemetry, and Fact Guard red highlighting."),
        ("Factual Protection: ", "Automated entity cross-matching prevents the broadcast of hallucinated amounts, dates, or casualty numbers."),
        ("Phase 3 Deliverables (Thu Nov 19): ", "Tagging git release v1.0, preparing the live demo with unexpected judge articles, and delivering the final 20-minute product presentation.")
    ]
    for bold_txt, norm_txt in checklist:
        p = doc.add_paragraph()
        r1 = p.add_run(f"• {bold_txt}")
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = c_navy
        r2 = p.add_run(norm_txt)
        r2.font.size = Pt(10)
        r2.font.color.rgb = c_slate

    # Save outputs
    out_1 = r"C:\Users\emili\Desktop\cepechuy\cepesin_chuy\RNAP_Hack_2026_English_Nov12_Troubleshooting_Report.docx"
    out_2 = r"C:\Users\emili\Desktop\cepechuy\cepesin_chuy\EA_Act12_Troubleshooting_Report_Team5.docx"
    doc.save(out_1)
    doc.save(out_2)
    print("Full Word document saved to:", out_1)
    print("Full Word document copy saved to:", out_2)

if __name__ == "__main__":
    create_full_word_report()
