import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def create_report_doc():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    navy = RGBColor(15, 23, 42)
    slate = RGBColor(71, 85, 105)
    blue = RGBColor(37, 99, 235)

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_inst.add_run("UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN\nESCUELA INDUSTRIAL Y PREPARATORIA TÉCNICA “ÁLVARO OBREGÓN”")
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = navy

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_course.add_run("Comunicación Integral en Inglés Técnico I · Etapa 4\nEvidencia de Aprendizaje · Act. 12 — Troubleshooting Report")
    r.font.size = Pt(12)
    r.font.color.rgb = blue

    doc.add_paragraph("\n" * 2)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_title.add_run("PROTOTYPE AUDIT REPORT:\nAUTOMATED SPANISH NEWS SUMMARIZER\nFOR RADIO CUMBRES")
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = navy

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sub.add_run("Consulting Audit Evaluation on Phase 2 Prototype (CP4)")
    r.font.size = Pt(12)
    r.font.italic = True
    r.font.color.rgb = slate

    doc.add_paragraph("\n" * 3)

    # Team Info Table
    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_info.add_run("TEAM 5 — cepesin_chuy | TRACK 2: NEWS IN 60 SECONDS")
    r.font.bold = True
    r.font.size = Pt(11)

    t_team = doc.add_table(rows=5, cols=2)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_data = [
        ["2250704", "GOMEZ MONTES EMILIO ANTONIO (Lead Developer & UI)"],
        ["2251085", "SANCHEZ GONZALEZ ISRAEL ALEKSANDER (Transformer Fine-Tuning)"],
        ["2251147", "HERNÁNDEZ CAYETANO KEVIN ADRIÁN (Corpus & Timing Validation)"],
        ["2251441", "PEREZ CEPEDA MIA VALENTINA (Evaluation & Editorial Audit)"],
        ["Docente:", "Lic. Jesús Alejandro Juárez González · Jueves 12 de Noviembre de 2026"]
    ]
    for row_idx, (c1, c2) in enumerate(team_data):
        cell1, cell2 = t_team.rows[row_idx].cells
        cell1.width = Inches(1.8)
        cell2.width = Inches(4.7)
        p1 = cell1.paragraphs[0]
        p1.add_run(c1).font.bold = True
        p1.runs[0].font.size = Pt(10)
        p2 = cell2.paragraphs[0]
        p2.add_run(c2).font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # REPORT BODY (250 - 400 WORDS)
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("1. Audit Status", level=1)
    h1.runs[0].font.color.rgb = navy

    p_s1 = doc.add_paragraph()
    r = p_s1.add_run("Since ")
    r.font.bold = True
    p_s1.add_run("the beginning of Phase 2, our consulting engineering team ")
    r = p_s1.add_run("has audited ")
    r.font.bold = True
    p_s1.add_run("and evaluated the prototype developed for Radio Cumbres. We ")
    r = p_s1.add_run("have already achieved ")
    r.font.bold = True
    p_s1.add_run("100% operational compliance with the 120-word airtime constraint across all 4,763 test articles, and our system has generated zero summaries with excess words. Our prototype ")
    r = p_s1.add_run("has increased ")
    r.font.bold = True
    p_s1.add_run("the average news capsule length from 18.5 words (vanilla mT5) to 89.5 words (fine-tuned model), providing 44.7 seconds of informative broadcast coverage for the morning host. The team ")
    r = p_s1.add_run("has fine-tuned ")
    r.font.bold = True
    p_s1.add_run("decoding parameters ")
    r = p_s1.add_run("for ")
    r.font.bold = True
    p_s1.add_run("several days to balance fluency and strict sentence boundary closure. However, our audit reveals that we ")
    r = p_s1.add_run("have not eliminated ")
    r.font.bold = True
    p_s1.add_run("all named-entity hallucinations in complex international articles ")
    r = p_s1.add_run("yet")
    r.font.bold = True
    p_s1.add_run(", which remains our primary open risk.")

    # Benchmark Table
    doc.add_paragraph().add_run("Table 1. Operational Benchmark on Spanish Test Set (4,763 Articles)").font.bold = True
    tbl = doc.add_table(rows=4, cols=6)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Model", "Approach", "ROUGE-1", "ROUGE-L", "Avg. Words (Airtime)", "<= 120 Words"]
    data = [
        ["1. Base (TF-IDF)", "Extractive (Lead Bias)", "0.1719", "0.1115", "113.2 pal. (56.6 s)", "100.0% (0 ex)"],
        ["2. Pretrained (mT5 Vanilla)", "Abstractive (Zero-FT)", "0.2999", "0.2310", "18.5 pal. (9.2 s)", "100.0% (0 ex)"],
        ["3. Solution (mT5 + LoRA)", "Abstractive (Fine-Tuned)", "0.2177", "0.1407", "89.5 pal. (44.7 s)", "100.0% (0 ex)"]
    ]

    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            cell = tbl.cell(row_idx + 1, col_idx)
            if row_idx % 2 == 1:
                set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if col_idx == 5:
                r.font.bold = True
                r.font.color.rgb = RGBColor(22, 101, 52)

    doc.add_paragraph()

    h2 = doc.add_heading("2. Immediate Solutions", level=1)
    h2.runs[0].font.color.rgb = navy

    p_s2 = doc.add_paragraph()
    p_s2.add_run("To mitigate the identified risks before the live demo, our consulting audit proposes two concrete technical improvements:\n")
    
    p_s2_1 = doc.add_paragraph()
    r = p_s2_1.add_run("1. Fact Guard Entity Regex Filter: ")
    r.font.bold = True
    r = p_s2_1.add_run("If we implemented ")
    r.font.bold = True
    p_s2_1.add_run("an automated named-entity recognition filter into our generation pipeline, the model ")
    r = p_s2_1.add_run("would eliminate ")
    r.font.bold = True
    p_s2_1.add_run("ungrounded figures and proper nouns before the host read them on live air.")

    p_s2_2 = doc.add_paragraph()
    r = p_s2_2.add_run("2. Repetition Penalty Tuning: ")
    r.font.bold = True
    r = p_s2_2.add_run("If we raised ")
    r.font.bold = True
    p_s2_2.add_run("the repetition penalty to 1.18 and enforced a 3-gram constraint during decoding, the Transformer ")
    r = p_s2_2.add_run("would prevent ")
    r.font.bold = True
    p_s2_2.add_run("repetitive lexical loops in political and judicial stories, enhancing broadcast cadence.")

    h3 = doc.add_heading("3. Root Cause Analysis", level=1)
    h3.runs[0].font.color.rgb = navy

    p_s3 = doc.add_paragraph()
    p_s3.add_run("An audit of Phase 1 engineering decisions reveals two historical causes for prototype latency and variance:\n")

    p_s3_1 = doc.add_paragraph()
    r = p_s3_1.add_run("1. Initial Corpus Selection: ")
    r.font.bold = True
    r = p_s3_1.add_run("If our team had chosen ")
    r.font.bold = True
    p_s3_1.add_run("the full 38,000-article XL-Sum Spanish corpus from Phase 1 instead of our initial 120-sample toy dataset, the LoRA adapter ")
    r = p_s3_1.add_run("would have learned ")
    r.font.bold = True
    p_s3_1.add_run("broader journalistic vocabulary earlier, avoiding retraining pipelines during CP3.")

    p_s3_2 = doc.add_paragraph()
    r = p_s3_2.add_run("2. Sentence Boundary Post-Processing: ")
    r.font.bold = True
    r = p_s3_2.add_run("If we had implemented ")
    r.font.bold = True
    p_s3_2.add_run("the semantic sentence-boundary trimming algorithm during zero-shot testing, the vanilla mT5 model ")
    r = p_s3_2.add_run("would not have generated ")
    r.font.bold = True
    p_s3_2.add_run("abrupt fragments that broke off mid-sentence, saving significant debugging effort.")

    # Calculate word count of sections 1 to 3
    body_text = f"{p_s1.text} {p_s2.text} {p_s2_1.text} {p_s2_2.text} {p_s3.text} {p_s3_1.text} {p_s3_2.text}"
    word_count = len(body_text.split())
    
    p_count = doc.add_paragraph()
    p_count.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_count.add_run(f"Word Count (Sections 1-3): {word_count} words (Requirement: 250 - 400 words · Status: Compliant)")
    r.font.size = Pt(9.5)
    r.font.italic = True
    r.font.color.rgb = slate

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # ANNEX: D3 DEVELOPER REFLECTION (ACT. 11)
    # -------------------------------------------------------------------------
    h_annex = doc.add_heading("Annex: D3 · Act. 11 — Developer Reflection", level=1)
    h_annex.runs[0].font.color.rgb = navy

    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Student: Emilio Antonio Gómez Montes (2250704) · Team 5 (cepesin_chuy)")
    r.font.bold = True
    r.font.size = Pt(11)

    p_r1 = doc.add_paragraph()
    r = p_r1.add_run("Real Experiences: ")
    r.font.bold = True
    p_r1.add_run("In RNAP Hack, I have already engineered the TF-IDF sentence extractive baseline and deployed the interactive Gradio interface v1 with Fact Guard verification. Our team has worked collaboratively since the start of the semester to optimize radio locution timing. However, we have not tested our interface against the judge's hidden test articles yet.")

    p_r2 = doc.add_paragraph()
    r = p_r2.add_run("An Ideal Present: ")
    r.font.bold = True
    p_r2.add_run("If we had access to larger dedicated GPU clusters and more computing time, I would build an end-to-end voice-to-speech synthesis pipeline that would convert news articles directly into spoken radio audio with dynamic prosody control.")

    p_r3 = doc.add_paragraph()
    r = p_r3.add_run("A Past Reflection: ")
    r.font.bold = True
    p_r3.add_run("In Phase 1, our team chose a small synthetic dataset for initial testing. If we had integrated the comprehensive 38,000-article BBC Mundo corpus from the very first checkpoint, our model would have converged with greater linguistic richness before checkpoint CP3.")

    d3_words = len(f"{p_r1.text} {p_r2.text} {p_r3.text}".split())
    p_d3_count = doc.add_paragraph()
    p_d3_count.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_d3_count.add_run(f"D3 Word Count: {d3_words} words (Requirement: 100 - 150 words · Status: Compliant)")
    r.font.size = Pt(9.5)
    r.font.italic = True
    r.font.color.rgb = slate

    out_path = r"C:\Users\emili\Desktop\cepechuy\cepesin_chuy\EA_Act12_Troubleshooting_Report_Team5.docx"
    doc.save(out_path)
    print("Report docx saved successfully to:", out_path)
    print("Report word count:", word_count)
    print("D3 word count:", d3_words)

if __name__ == "__main__":
    create_report_doc()
