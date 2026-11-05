# RNAP Hack 2026 · Track 2: News in 60 Seconds
### Automated Spanish News Summarization for Radio Cumbres

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hackathon: RNAP 2026](https://img.shields.io/badge/UANL-RNAP%20Hack%202026-red.svg)](https://www.uanl.mx/)

> **Academic Course:** Neural Networks and Deep Learning (RNAP)  
> **Institution:** UANL · Escuela Industrial y Preparatoria Técnica "Álvaro Obregón"  
> **Team:** `cepesin_chuy`  
> **Track:** Track 2 — News in 60 Seconds  
> **Phase 1 Milestone:** Baseline Models & Technical Report (`CP2` - November 5, 2026)

---

## 1. Project Overview & Business Case

### The Client: Radio Cumbres
**Radio Cumbres** is a local radio station based in Nuevo León, Mexico, known for its dynamic morning news broadcast.

### The Problem
The morning radio host has **strictly 60 seconds per news story** on air. At a standard Spanish radio speech rate of approximately **2 words per second**, each summary must strictly contain **at most 120 words**. 

Historically, two news producers summarized incoming stories manually starting at 5:00 a.m. Previous attempts with generic online summarization tools failed because:
1. Generated texts exceeded the 60-second airtime window.
2. Models hallucinated figures and names (e.g., broadcasting an incorrect financial figure on live radio).

### The Objective
Develop an end-to-end NLP solution that summarizes Spanish news articles into concise, broadcast-ready summaries ($\le 120$ words / $\le 60$ seconds) with **100% factual fidelity** (zero invented facts, names, or numbers).

---

## 2. Repository Structure

```text
cepesin_chuy/
├── README.md                # Technical and product overview in English (PIA English deliverable)
├── PROGRESS.md              # Checkpoint log (CP1, CP2, CP3, CP4)
├── requirements.txt         # Library dependencies
├── RNAP_Hack_2026_Challenge_Tracks.pdf # Official competition tracks
├── RNAP_Hack_2026_Guia_GitHub.pdf      # GitHub workflow instructions
├── RNAP_Hack_2026_Instrucciones_Redes_Neuronales.pdf # Evaluation rubric
├── data/                    # Dataset samples, splits, and documentation
│   ├── README.md            # Dataset specification and metadata
│   ├── dataset_sample.csv   # Master corpus (120 articles across 10 categories)
│   ├── train.csv            # Stratified training split (70% - 84 articles)
│   ├── val.csv              # Stratified validation split (15% - 18 articles)
│   └── test.csv             # Stratified test split (15% - 18 articles)
├── notebooks/               # Jupyter technical reports
│   ├── entrenamiento.ipynb  # Master technical notebook (Sections 1 to 6)
│   └── emilio_baseline.ipynb# Emilio's individual experimental baseline notebook
└── app/                     # Gradio interface (scheduled for Phases 2 & 3)
```

---

## 3. Phase 1 (Baseline Models) Summary

### Evaluation Metrics
- **Primary Quality Metrics:** **ROUGE-1, ROUGE-2, and ROUGE-L** (F1 scores) evaluated against journalist-written reference summaries (*XL-Sum standard*).
- **Primary Operational Constraints:**
  - **Word Limit:** $\le 120$ words (100% compliance required).
  - **Estimated On-Air Read Time:** $\le 60.0$ seconds.
  - **Factual Faithfulness:** 0 ungrounded facts or invented numbers.

### Text Representation
- **Baseline (Extractive):** **Sentence-level TF-IDF with Lead Position Weighting (*lead bias*)**. Prioritizes informative sentences located in the news lead (inverted pyramid structure) and selects sentences greedily within the 120-word budget.
- **Advanced (Phases 2 & 3):** Contextual subword tokenization (SentencePiece) and cross-attention encoder-decoder representations via `csebuetnlp/mT5_multilingual_XLSum`.

### Comparative Results on Test Set (18 Articles)
| Model | Approach | ROUGE-1 | ROUGE-2 | ROUGE-L | Avg. Words | Read Time | $\le 120$ words | Factual Faithfulness | Latency |
|---|---|---|---|---|---|---|---|---|---|
| **Base Model (Extractive TF-IDF)** | Extractive (supervised) | **0.3482** | **0.0896** | **0.2110** | 101.0 words | **50.5 s** | **100.0%** | **100% (zero hallucination)** | **0.78 ms / art.** |
| **Pretrained Model (XL-Sum Abstractive)** | Abstractive (no fine-tuning) | **0.4184** | **0.2494** | **0.2927** | 65.6 words | **32.8 s** | **100.0%** | Requires Fact Guard | **< 0.01 ms / art.** |

#### Key Takeaway & Phase 2 Roadmap:
- The TF-IDF extractive baseline provides **100% factual safety** (never invents figures) and strictly respects the radio broadcast time ($\le 60$ s) with sub-millisecond execution.
- In **Phase 2 (November 12)**, we will fine-tune **mT5_multilingual_XLSum** and integrate a **Fact Guard** verification engine to highlight in red any numbers or names not found in the source article.

---

## 4. Setup & Quickstart

```bash
# Clone the repository
git clone https://github.com/ElElimios/cepesin_chuy.git
cd cepesin_chuy

# Install dependencies
pip install -r requirements.txt

# Run the master technical report
jupyter notebook notebooks/entrenamiento.ipynb
```

---

## 5. Team & Responsibilities
- **Emilio (ElElimios):** TF-IDF sentence extractive algorithm, position weighting logic, ROUGE metric calculations, and technical report notebook integration.
- **Chuy / Teammate:** Dataset collection and category stratification based on XL-Sum standards, broadcast time constraint validation.

---
*Developed for RNAP Hack 2026 · Etapa 4 y PIA · UANL EIAO.*
