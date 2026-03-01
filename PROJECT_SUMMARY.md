# Multi‑Lab Clinical Reasoning Evaluation with Gemini 2.0 Flash

This repository contains a fully reproducible research pipeline for evaluating multi‑lab clinical reasoning in large language models (LLMs). The project uses a curated dataset of abnormal laboratory panels, deterministic Clinical Decision Support (CDS) baselines, structured LLM prompts, rubric‑based scoring, and automated analysis notebooks. All data, code, and outputs are included to ensure transparency and reproducibility.

The goal is to provide a lightweight, accessible framework for studying how LLMs interpret abnormal labs, detect physiologic relationships, and maintain narrative discipline—without requiring paid API access or large datasets.

---

## Project Structure
```
ai-lab-cds/
├── data
│   └── panels.csv
│
├── outputs
│   ├── cds
│   │   └── <panel_id>_cds.txt
│   │
│   ├── llm
│   │   └── gemini_v1
│   │       └── <panel_id>_llm.txt
│   │
│   ├── scoring
│   │   └── <panel_id>_score.json
│   │
│   └── dataset
│       └── merged_dataset.csv
│
├── notebooks
│   ├── analysis.ipynb
│   ├── analysis_stats.ipynb
│   └── analysis_visuals.ipynb
│
├── METHODS.md
├── RESULTS.md
└── README.md
```
---

## Overview of the Pipeline

### 1. Dataset Construction
A set of nine laboratory panels was manually curated. Each panel contains three abnormal values selected to represent a coherent clinical scenario spanning metabolic, renal, hepatic, endocrine, hematologic, or cardiovascular domains.

Panels are stored in:

data/panels.csv


### 2. CDS Baseline Generation
A deterministic CDS baseline provides short, per‑lab explanations with no relational reasoning. These serve as a minimal comparator for LLM outputs.

Outputs are stored in:

outputs/cds/


### 3. LLM Output Generation
Each panel is passed to **Gemini 2.0 Flash** using a structured prompt requiring:

- A. Individual Lab Explanations  
- B. Possible Relationships Between Abnormal Labs  

LLM responses are saved in:

outputs/llm/gemini_v2/


### 4. Rubric‑Based Scoring
Each LLM output is evaluated using an eight‑dimension scoring rubric:

- correctness  
- completeness  
- relationship detection  
- relationship accuracy  
- narrative drift  
- certainty language  
- mechanistic depth  
- structure adherence  

Scores are stored as JSON:

outputs/scoring/


### 5. Dataset Merging
All panel metadata, CDS outputs, LLM outputs, and scoring results are merged into a single analysis‑ready file:

outputs/dataset/merged_dataset.csv


### 6. Analysis Notebooks
Three notebooks provide descriptive, statistical, and visualization‑based analysis:

- `analysis.ipynb` — descriptive statistics, drift analysis, output length comparisons  
- `analysis_stats.ipynb` — t‑tests, ANOVA, PCA, clustering  
- `analysis_visuals.ipynb` — ridge plot (auto‑skip), violin plots, correlation heatmap  

---

## Key Findings

A detailed summary is available in **RESULTS.md**. Highlights include:

- Gemini 2.0 Flash achieved **25/25** on all nine panels.  
- Outputs were **accurate, structured, and mechanistically grounded**.  
- Narrative drift was minimal, with appropriate use of conditional language.  
- The model consistently identified direct, indirect, and research‑supported relationships.  
- CDS outputs remained strictly per‑lab, while LLM outputs demonstrated multi‑lab reasoning.  

These findings demonstrate that even with a small dataset and free‑tier API access, structured prompts and rubric‑based scoring can meaningfully evaluate LLM clinical reasoning.

---

## Reproducibility

This repository is designed for full transparency:

- All raw data, intermediate outputs, and final datasets are included.  
- All scripts are deterministic and require no manual intervention.  
- All notebooks can be executed end‑to‑end.  
- No proprietary data or paid API features were used.  

Researchers can reproduce the entire study using only:

- the free Gemini API  
- the included dataset  
- the provided notebooks  

---

## Limitations

- The dataset is intentionally small due to free‑tier API constraints.  
- Ceiling effects are expected in well‑structured panels.  
- Results are not intended to generalize to all clinical scenarios.  

The primary contribution is methodological: a reproducible framework for evaluating multi‑lab reasoning in LLMs.

---

## Citation

If you use this repository or adapt the methodology, please cite:

Jason Lehman (2026). Multi‑Lab Clinical Reasoning Evaluation with Gemini 2.0 Flash.
GitHub Repository.

---

## Contact

For questions, collaboration, or extensions of this work, feel free to open an issue or reach out directly.
