# Progress Log - RNAP Hack 2026

Team: **cepesin_chuy**  
Challenge: **Reto 1 - Human or Machine? (AI vs Human Text Detection in Spanish)**  
Primary Metric: **Macro F1-Score**  

---

## CP2 - 2026-11-05
- **What we have done**:
  - Defined the challenge scope: binary classification to detect AI-generated vs human-written text in Spanish.
  - Selected and justified the primary evaluation metric: **Macro F1-Score** ($F_1 = 0.9667$ on test set), supported by Accuracy ($96.67\%$), Precision ($96.69\%$), and Recall ($96.67\%$). F1 was chosen because it penalizes both false positives (wrongfully flagging human writing as AI) and false negatives (failing to identify synthetic text).
  - Justified text representations: used **TF-IDF with unigrams and bigrams** (`ngram_range=(1,2)`) for the baseline to capture discriminative formulaic markers and lexical patterns typical of LLMs with minimal latency ($0.07$ ms/sample). Acknowledged subword tokenization and contextual embeddings for the upcoming Transformer fine-tuning stage.
  - Stratified dataset into Training (70%, 420 samples), Validation (15%, 90 samples), and Test (15%, 90 samples) with strict stratification (`stratify=y`, `random_state=42`) to prevent data leakage.
  - Built, trained, and validated the baseline model from scratch (`TF-IDF + Logistic Regression`), achieving full end-to-end execution.
  - Evaluated the off-the-shelf pretrained language model without fine-tuning (Zero-Shot / Language Perplexity baseline) on the exact same test partition ($F_1 = 0.6848$, Accuracy = $71.11\%$).
  - Measured and benchmarked processing times: baseline training time ($0.038$ s), baseline inference latency ($0.07$ ms/sample), pretrained inference latency ($0.08$ ms/sample).
  - Built a comprehensive comparative table and visualization plots (class distributions, confusion matrices, latency comparisons).
  - Formulated Sections 1, 2, and 3 in the technical notebook (`notebooks/entrenamiento.ipynb`) and verified individual baseline notebook (`notebooks/emilio_baseline.ipynb`).
- **What we haven't done yet**:
  - Fine-tuning a deep Spanish Transformer model (scheduled for Phase 2 / CP3).
  - Detailed error analysis of 5+ edge cases for the fine-tuned Transformer (scheduled for Phase 2 / CP4).
  - Web interactive user interface (v1 scheduled for Phase 2 / CP4, full release v1.0 for Phase 3).
- **Next step**:
  - Select and prepare the Spanish Transformer backbone (BETO / RoBERTa-BNE) for supervised fine-tuning in Phase 2.
  - Design the initial UI prototype with Streamlit / Gradio.
- **Who did what**:
  - Emilio: Led baseline training pipeline, TF-IDF vectorizer configuration, evaluation metrics, and technical report integration.
  - Team / Chuy: Curated the Spanish text dataset, verified stratified splits, and tested zero-shot evaluation hypotheses.

---

## CP1 - 2026-11-05
- **What we have done**:
  - Created team repository structure following the official guidelines (`README.md`, `PROGRESS.md`, `notebooks/`, `data/`, `requirements.txt`).
  - Selected Challenge 1: **Human or Machine?**
  - Formulated dataset specifications and curated a balanced Spanish corpus of 600 samples across multiple domains (science, history, philosophy, tech, literature).
  - Set up environment dependencies in `requirements.txt` (numpy, pandas, scikit-learn, matplotlib, seaborn, transformers, torch).
- **What we haven't done yet**:
  - Train baseline and evaluate pretrained zero-shot model (addressed in CP2).
  - Complete technical report notebook sections 1, 2, and 3 (addressed in CP2).
- **Next step**:
  - Implement TF-IDF baseline and evaluate on stratified test set.
  - Generate comparative tables, confusion matrices, and update progress log for CP2.
- **Who did what**:
  - Emilio: Repository scaffolding, environment configuration, dependency tracking, and initial git commit.
  - Team / Chuy: Domain research for Challenge 1 and data sourcing.
