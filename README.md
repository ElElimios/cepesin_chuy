# RNAP Hack 2026 · Track 2: News in 60 Seconds
### Automated Spanish News Summarization for Radio Cumbres

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hackathon: RNAP 2026](https://img.shields.io/badge/UANL-RNAP%20Hack%202026-red.svg)](https://github.com/ElElimios/cepesin_chuy)
[![Status: Phase 2 Prototype CP4](https://img.shields.io/badge/Status-CP4%20Evaluated-brightgreen.svg)](https://github.com/ElElimios/cepesin_chuy)
[![Live Demo: GitHub Pages](https://img.shields.io/badge/Demo-GitHub%20Pages-blueviolet.svg)](https://elelimios.github.io/cepesin_chuy/)

**Escuela Industrial y Preparatoria Técnica "Álvaro Obregón" (UANL)**  
**Unidad de Aprendizaje:** Redes Neuronales y Aprendizaje Profundo & Comunicación Integral en Inglés Técnico I  
**Team:** `cepesin_chuy` (Team 5)  
**Deliverable:** Technical Report & Prototype Interface (`CP4` - November 12, 2026)

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
Develop an end-to-end NLP solution that summarizes Spanish news articles into concise, broadcast-ready summaries ($\le 120$ words / $\le 60$ seconds) with **100% factual fidelity** (zero invented facts, names, or numbers) and **0 articles with word excess**.

---

## 2. Repository Structure

```text
cepesin_chuy/
├── README.md                                    # Technical and product overview in English
├── PROGRESS.md                                  # Checkpoint audit log (CP1, CP2, CP3, CP4)
├── requirements.txt                             # Library dependencies (gradio, peft, torch, etc.)
├── RNAP_Hack_2026_English_Nov12_Troubleshooting_Report.pptx # English Act. 12 & D3 presentation
├── EA_Act12_Troubleshooting_Report_Team5.docx   # Written English troubleshooting report
├── app/
│   └── app.py                                   # Gradio interactive web UI with Fact Guard
├── app.py                                       # Root launcher for Gradio web application
├── data/                                        # Datasets and corpora
│   ├── README.md                                # Dataset metadata and documentation
│   ├── spanish_train_sample.jsonl               # XL-Sum Spanish training split (3,500 samples)
│   ├── spanish_val.jsonl                        # XL-Sum Spanish validation split (4,763 samples)
│   └── spanish_test.jsonl                       # XL-Sum Spanish test split (4,763 samples)
├── notebooks/                                   # Jupyter technical reports
│   ├── entrenamiento.ipynb                      # Master technical notebook (Sections 1 to 5)
│   ├── comparativa_fase2.png                    # Benchmark multi-metric chart
│   └── RNAP_Track2_AKS(CP3).ipynb               # LoRA fine-tuning experimental run
└── [Official instructions and PDF rubrics]
```

---

## 3. Comparative Evaluation (Test Set: 4,763 Articles)

| Model | Approach | ROUGE-1 | ROUGE-2 | ROUGE-L | Avg. Words | Locution Time | $\le 120$ words | Excess Words | Latency / Art. |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Base Model (TF-IDF)** | Extractive (Lead Bias) | 0.1719 | 0.0339 | 0.1115 | 113.2 pal. | 56.6 s | **100.0%** | **0 (0.0%)** | 5.26 ms |
| **2. Pretrained (mT5 Vanilla)** | Abstractive (Zero-FT) | 0.2999 | 0.1119 | 0.2310 | 18.5 pal. | 9.2 s | **100.0%** | **0 (0.0%)** | 220.94 ms |
| **3. Solution (mT5 + LoRA Radio)** | Abstractive (Fine-Tuned) | 0.2177 | 0.0570 | 0.1407 | 89.5 pal. | 44.7 s | **100.0%** | **0 (0.0%)** | 231.66 ms |

### Key Achievements in Phase 2 (CP3 & CP4):
- **Zero Excess Words Guarantee:** 100.0% of generated test summaries strictly comply with $\le 120$ words ($0$ articles exceeded the threshold).
- **Broadcast Coverage:** Lifted generation length from 18.5 words (vanilla mT5) to **89.5 words (44.7 seconds on air)**, perfectly filling the morning news slot.
- **Fact Guard Protection:** Entity cross-matching highlights ungrounded numbers or names in bold red in the Gradio interface, ensuring live broadcast safety.

---

## 4. Setup & Quickstart

```bash
# Clone the repository
git clone https://github.com/ElElimios/cepesin_chuy.git
cd cepesin_chuy

# Install dependencies
pip install -r requirements.txt

# Run the interactive Gradio interface (v1)
python app.py

# Or explore the master technical report
jupyter notebook notebooks/entrenamiento.ipynb
```

---

## 5. Team & Responsibilities (Team 5)
- **Emilio Antonio Gómez Montes (2250704):** TF-IDF sentence extractive baseline, Gradio interface v1 development, Fact Guard entity engine, and master notebook integration.
- **Israel Aleksander Sánchez González (2251085):** mT5 LoRA fine-tuning training loop on GPU, hyperparameter tuning, and checkpoint evaluations.
- **Kevin Adrián Hernández Cayetano (2251147):** XL-Sum dataset curation, locution timing validation, and error case categorization.
- **Mía Valentina Pérez Cepeda (2251441):** Data analysis, editorial criteria evaluation, and English troubleshooting audit documentation.

---
*Developed for RNAP Hack 2026 · Etapa 4 y PIA · UANL EIAO.*
