# Progress Log - RNAP Hack 2026

Team: **cepesin_chuy**  
Challenge: **Track 2 - News in 60 Seconds (Radio Cumbres)**  
Primary Metrics: **ROUGE (ROUGE-1, ROUGE-2, ROUGE-L) and Strict Word Count Limit ($\le 120$ words / 60 seconds)**  

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
