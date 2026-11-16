# Progress Log - RNAP Hack 2026

Team: **cepesin_chuy** (Team 5)  
Challenge: **Track 2 - News in 60 Seconds (Radio Cumbres)**  
Primary Metrics: **ROUGE (ROUGE-1, ROUGE-2, ROUGE-L), Strict Word Limit ($\le 120$ words / $\le 60$ s on air), and Zero Excess Words Guarantee**  
Repository Checkpoint: **CP4 (Fase 2: Evidencia de Aprendizaje · Prototipo)** — November 12, 2026  

---

## CP4 - 2026-11-12
- **What we have done**:
  - Built and deployed the interactive web application interface v1 (`app/app.py` and root `app.py`) powered by **Gradio**, fulfilling all operational requirements for Track 2 and the Phase 2 rubric.
  - Connected the interface to all three evaluated models:
    1. **Solución Transformer:** `csebuetnlp/mT5_multilingual_XLSum` with LoRA adapter fine-tuned for radio news capsules.
    2. **Modelo Base:** Sentence-level extractive TF-IDF with lead-bias position weighting.
    3. **Modelo Preentrenado:** `mT5_multilingual_XLSum` vanilla zero-shot.
  - Implemented the **Live Locution Dashboard**:
    - Real-time word counter with progress against the 120-word budget (`palabras / 120`).
    - Estimated radio broadcast read time (`palabras / 2.0` seconds).
    - Status badge: `✅ CUMPLE ESTÁNDAR RADIO CUMBRES: <= 120 palabras (Sin exceso de palabras)`.
  - Implemented the **Fact Guard** verification engine:
    - Extracts all numeric amounts, percentages, currencies, dates, and named entities (capitalized entities).
    - Cross-references generated tokens against the full original Spanish news source.
    - Dynamically highlights ungrounded numbers or names in **bold red** (`#dc2626`) with an alert tooltip warning the radio host against live broadcasting.
    - Displays a real-time **Factual Faithfulness Score** (% of grounded entities) and detailed audit notes.
  - Completed **Section 5 (Evaluación y Errores)** in the master technical notebook (`notebooks/entrenamiento.ipynb`):
    - Comparative evaluation table across 4,763 articles on the Spanish XL-Sum test set.
    - Generated Matplotlib multi-metric visualization (`notebooks/comparativa_fase2.png`) comparing ROUGE-1, ROUGE-2, ROUGE-L and airtime vs the 60-second broadcast ceiling.
    - Conducted an in-depth qualitative and quantitative error analysis across **5 real failure modes**:
      1. *Numeric Interpolation / Hallucination* (cross-attention averaging nearby quantities).
      2. *Premature Truncation on Run-on Subordinate Clauses* (sentence boundary cutter stepping back).
      3. *Proper Noun Simplification* (SentencePiece subword penalty on non-Romance names).
      4. *Lexical Repetition Loops* (insufficient repetition penalty in administrative texts).
      5. *Temporal Anchor Bias* ("today" breaking news bias on historical retrospectives).
  - Validated the strict operational condition: **Zero articles with excess words**. 100.0% of generated test summaries strictly comply with $\le 120$ words ($0$ out of $4,763$ articles exceeded the limit).
  - Updated `requirements.txt` with all dependencies (`gradio`, `peft`, `accelerate`, `transformers`, `torch`, `python-docx`, `python-pptx`, `tabulate`).
- **What we haven't done yet**:
  - Live demo deployment and testing with surprise inputs from the judge (Phase 3 / PIA).
  - Writing Section 6 in the notebook covering cross-attention architectural deep dive and radio operating manual (Phase 3 / PIA).
  - Marking official git release tag `v1.0`.
- **Next step**:
  - Package local offline standalone runner for the laptop demo before the judge.
  - Rehearse the 20-minute product presentation and 5-minute live demo for November 19.
- **Who did what**:
  - Emilio: Designed and programmed the Gradio interface v1 (`app/app.py`), the Fact Guard entity matching engine with red highlighting, and integrated the complete evaluation and error analysis into `notebooks/entrenamiento.ipynb`.
  - Aleks / Israel: Calibrated the LoRA generation parameters, tested interactive inference on sample articles, and curated test failure cases.
  - Kevin & Mía: Audited test case groundings, validated locution timing benchmarks, and prepared the technical documentation.

---

## CP3 - 2026-11-12
- **What we have done**:
  - Transitioned the training and evaluation corpus to the full-scale Spanish subset of **XL-Sum (BBC Mundo)**, incorporating 3,500 training articles, 4,763 validation articles, and 4,763 test articles (`data/spanish_*.jsonl`).
  - Constructed the **Solución con Transformer**: selected and fine-tuned `csebuetnlp/mT5_multilingual_XLSum` (582M parameters Seq2Seq encoder-decoder) using **PEFT LoRA (Low-Rank Adaptation)**.
  - Configured LoRA with rank $r=16$, $\alpha=32$, dropout $0.05$, targeting query (`q`) and value (`v`) attention projection matrices, training only 1,843,200 parameters (0.316% of total) in 2.89 minutes on GPU T4 without catastrophic forgetting.
  - Designed the specialized radio training target (`construir_objetivo_radio`) combining lead facts with non-redundant salient sentences to establish a consistent 90-120 word broadcast capsule style.
  - Created the prompt prefix: `"Resume esta noticia para radio en 100 a 120 palabras usando solo datos del texto: "`.
  - Calibrated Seq2Seq generation hyperparameters: `min_new_tokens=138`, `max_new_tokens=168`, `repetition_penalty=1.15`, `no_repeat_ngram_size=3`, `num_beams=1`.
  - Engineered the radio sentence closure algorithm `cerrar_oracion_radio(texto, max_words=120)` with a double safety check, strictly guaranteeing **zero articles with excess words** ($\le 120$ words across 100% of cases).
  - Completed **Section 4 (Solución con Transformer)** in `notebooks/entrenamiento.ipynb` with complete architecture justification, hyperparameter table, and parameter effect analysis.
  - Evaluated on test set: ROUGE-1: 0.2177, ROUGE-2: 0.0570, ROUGE-L: 0.1407, Average words: 89.5, On-air time: 44.7 s, Compliance $\le 120$ words: 100.0%, Excess words: 0 (0.0%).
- **What we haven't done yet**:
  - Interactive Gradio graphical user interface (addressed in CP4).
  - Fact Guard hallucination highlighter (addressed in CP4).
- **Next step**:
  - Develop Gradio web UI and Fact Guard audit engine for CP4.
- **Who did what**:
  - Aleks / Israel: Configured and executed the LoRA fine-tuning training loop on Colab GPU, generated comparative checkpoint metrics, and logged training loss curves.
  - Emilio: Implemented the `cerrar_oracion_radio` word-capping algorithm, formulated the prompt conditioning strategy, and integrated Section 4 documentation into the master technical report.
  - Kevin & Mía: Formatted the XL-Sum dataset splits, analyzed target length distributions, and verified hyperparameter logging.

---

## CP2 - 2026-11-05
- **What we have done**:
  - Defined the challenge problem: developing an automated Spanish news summarizer for **Radio Cumbres** (a local radio station in Nuevo León) where the morning host has exactly 60 seconds per news story, requiring summaries strictly within 120 words ($\le 60$ seconds at 2 words/sec) with zero hallucinated figures or names.
  - Selected and justified the primary evaluation metrics: **ROUGE (ROUGE-1, ROUGE-2, ROUGE-L)** to measure n-gram overlap and longest common subsequence against journalist reference summaries, combined with an operational **word limit constraint ($\le 120$ words)** and **read-aloud time ($\le 60$ seconds)**.
  - Justified the text representation: used **sentence-level TF-IDF with lead position weighting (lead bias)** for the baseline. In journalism (inverted pyramid structure), the opening sentences carry the core facts (who, what, when, where, why). TF-IDF identifies salient vocabulary in milliseconds, and extractive selection guarantees 100% factual faithfulness (impossible to invent numbers or names).
  - Prepared and stratified the dataset into Training (70%, 84 articles), Validation (15%, 18 articles), and Test (15%, 18 articles) across 10 balanced thematic categories using fixed random seed (`random_state=42`) to prevent data leakage.
  - Built, trained, and executed the extractive baseline model from scratch (`TF-IDF + Lead Bias Ranking`), achieving 100% compliance with the 120-word limit (average: 101.0 words, 50.5 s read time; ROUGE-1: 0.3482, ROUGE-2: 0.0896, ROUGE-L: 0.2110; latency: 0.78 ms/article).
  - Applied the off-the-shelf pretrained summarizer without fine-tuning (`mT5_multilingual_XLSum` style) on the exact same test set (100% compliance with $\le 120$ words, average: 65.6 words; ROUGE-1: 0.4184, ROUGE-2: 0.2494, ROUGE-L: 0.2927).
  - Measured processing times and inference latency for both models.
  - Built a comparative summary table and visualization figures (EDA word count histograms, ROUGE scores, radio read-aloud time benchmarks).
  - Completed Sections 1, 2, and 3 in the master technical notebook (`notebooks/entrenamiento.ipynb`) and individual baseline notebook (`notebooks/emilio_baseline.ipynb`).
  - Checkpoint status: All 10 criteria of the official evaluation checklist completed and validated.
- **What we haven't done yet**:
  - Fine-tuning the `csebuetnlp/mT5_multilingual_XLSum` encoder-decoder model on the Spanish training split (scheduled for Phase 2 / CP3).
  - Developing the **Fact Guard** verification module to flag ungrounded numbers or names in red (scheduled for Phase 2 / CP4).
  - Building the interactive Gradio web application with live word counter and timer (v1 for Phase 2 / CP4, final v1.0 for Phase 3).
- **Next step**:
  - Set up the mT5 fine-tuning pipeline with PyTorch and Hugging Face Seq2SeqTrainer.
  - Implement regex / NER entity matching for the Fact Guard module.
- **Who did what**:
  - Emilio: Implemented TF-IDF sentence extraction baseline, position weighting algorithm, ROUGE evaluation suite, and technical report notebook integration.
  - Team / Chuy: Curated the Spanish news dataset following the BBC Mundo / XL-Sum format, validated stratified category splits, and tested pretrained summary generation.

---

## CP1 - 2026-11-05
- **What we have done**:
  - Scaffolding of the repository architecture according to official competition rules (`README.md`, `PROGRESS.md`, `notebooks/`, `data/`, `requirements.txt`).
  - Selected Track 2: **News in 60 Seconds**.
  - Formulated the operational parameters for Radio Cumbres: 60 seconds air time limit, 120 words maximum, factual accuracy.
  - Curated a balanced 120-article Spanish news corpus across 10 categories with journalist reference summaries based on XL-Sum standards.
  - Configured project dependencies in `requirements.txt`.
- **What we haven't done yet**:
  - Implement TF-IDF sentence extractive baseline and evaluate against pretrained model (addressed in CP2).
  - Complete technical report Sections 1, 2, and 3 (addressed in CP2).
- **Next step**:
  - Code TF-IDF scoring algorithm with word budget constraint.
  - Compute ROUGE metrics and produce comparative evaluation report for CP2.
- **Who did what**:
  - Emilio: Initial git repository setup, dependencies configuration, and baseline architecture design.
  - Team / Chuy: Track 2 requirements analysis, news dataset collection, and reference summary formatting.
