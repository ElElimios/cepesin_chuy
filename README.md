# RNAP Hack 2026 - Track 2: News in 60 Seconds
### Automated Spanish News Summarization for Radio Cumbres

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hackathon: RNAP 2026](https://img.shields.io/badge/UANL-RNAP%20Hack%202026-red.svg)](https://www.uanl.mx/)

> **Academic Course:** Neural Networks and Deep Learning (RNAP)
> **Institution:** UANL - Escuela Industrial y Preparatoria Técnica "Álvaro Obregón"
> **Team:** `cepesin_chuy` (Team 5)
> **Track:** Track 2 — News in 60 Seconds
> **Current Milestone:** Phase 2 Prototype — Fine-Tuned Transformer & Local Interface v1 (`CP3` & `CP4` - November 12, 2026)

---

## 1. Project Overview & Business Case

### The Client: Radio Cumbres
**Radio Cumbres** is a local radio station based in Nuevo León, Mexico, known for its dynamic morning news broadcast.

### The Problem
The morning radio host has **strictly 60 seconds per news story** on air. At a standard Spanish radio speech rate of approximately **2 words per second**, each summary must **strictly contain 120 words or fewer**. Previously, producers summarized stories manually starting at 5:00 a.m., causing bottlenecks, omitted facts, or scripts that exceeded airtime.

---

## 2. How Our Solution Works

1. **Restructured Dataset (`data/`):** We use the full Spanish news corpus divided into training (`spanish_train_sample.jsonl`), validation (`spanish_val.jsonl`), and test (`spanish_test.jsonl`) splits prior to training.
2. **Baseline Models (Phase 1):**
   * **Extractive Baseline:** TF-IDF sentence scoring (`notebooks/emilio_baseline.ipynb`).
   * **Zero-Shot Pretrained Model:** Unadjusted `csebuetnlp/mT5_multilingual_XLSum` (`notebooks/Modelo_preentrenado.ipynb`).
3. **Transformer Solution (Phase 2 - Fine-Tuning):**
   * We fine-tuned **`csebuetnlp/mT5_multilingual_XLSum`** on the Spanish news dataset (`notebooks/RNAP_Track2_AKS(CP3).ipynb` and `notebooks/Entrenamiento(ReporteFinal).ipynb`).
4. **Local Interface v1 (`app/app_penitencia_final.py`):**
   * A Gradio web interface running locally to load the heavy model weights without cloud RAM limitations.

---

## 3. Repository Structure

```text
cepesin_chuy/
├── README.md
├── PROGRESS.md
├── requirements.txt
├── app/
│   └── app_penitencia_final.py
├── data/
│   ├── README.md
│   ├── spanish_train_sample.jsonl
│   ├── spanish_val.jsonl
│   └── spanish_test.jsonl
├── notebooks/
|   ├── Entrenamiento(ReporteFinal).ipynb
|   ├── RNAP_Track2_AKS(CP3).ipynb
|   ├── RNAP_Track2_AKS.ipynb
|   ├── Modelo_preentrenado.ipynb
|   ├── emilio_baseline.ipynb
|   └── METRICAS_RD.ipynb
└── dimensiones/
    └── Todas las dimensiones de inglés 
