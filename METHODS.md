# Methods

This project presents a fully reproducible pipeline for evaluating multi‑lab clinical reasoning in large language models (LLMs). The pipeline uses a curated set of nine laboratory panels, deterministic Clinical Decision Support (CDS) baselines, Gemini 2.0 Flash outputs, a structured scoring rubric, and automated analysis notebooks. All code, data, and outputs are included in the repository to ensure transparency and reproducibility.

---

## Dataset Construction

### Panel Design
Each panel consists of **three abnormal laboratory values** selected to represent a coherent clinical scenario. Panels span multiple physiologic domains, including:

- Metabolic  
- Renal  
- Hepatic  
- Endocrine  
- Hematologic  
- Cardiovascular  

Panels were manually curated to ensure:

- clear abnormal values  
- clinically meaningful combinations  
- opportunities for multi‑lab relational reasoning  

Panels are stored in:

data/panels.csv


Each row includes:

- `panel_id`  
- lab names, values, units, reference ranges  
- category labels  
- placeholders for LLM and CDS outputs  

---

## CDS Baseline Generation

A deterministic **Clinical Decision Support (CDS)** baseline was created for each panel. CDS outputs provide:

- short, per‑lab explanations  
- no relational reasoning  
- no mechanistic depth  
- no narrative structure  

These serve as a minimal, rule‑based comparator for LLM outputs.

outputs/cds/<panel_id>_cds.txt


---

## LLM Output Generation

### Model
All LLM outputs were generated using **Gemini 2.0 Flash** via the free Google AI Studio API.

### Prompt Template
Each panel was passed to the model using a structured prompt requiring:

- **A. Individual Lab Explanations**  
- **B. Possible Relationships Between Abnormal Labs**  

The prompt enforces:

- structured output  
- conditional language  
- mechanistic reasoning  
- identification of direct, indirect, and research‑supported relationships  

### Output Storage
Each model response is saved as:

outputs/llm/gemini_v2/<panel_id>_llm.txt


This ensures one LLM output per panel.

---

## Scoring Rubric

A structured scoring rubric was developed to evaluate eight dimensions of clinical reasoning:

1. **Correctness** (0–4)  
2. **Completeness** (0–3)  
3. **Relationship Detection** (0–4)  
4. **Relationship Accuracy** (0–3)  
5. **Narrative Drift** (0–3)  
6. **Certainty Language** (0–2)  
7. **Mechanistic Depth** (0–4)  
8. **Structure Adherence** (0–2)  

The rubric emphasizes:

- physiologic accuracy  
- appropriate uncertainty  
- multi‑lab reasoning  
- avoidance of hallucinations  
- adherence to required output format  

### Automated Scoring
Each LLM output is scored automatically using a rubric‑driven evaluation script. Scores and explanations are saved as JSON:

outputs/scoring/<panel_id>_score.json


---

## Dataset Merging

A merging script consolidates:

- panel metadata  
- CDS outputs  
- LLM outputs  
- scoring results  

into a single analysis‑ready CSV:

outputs/dataset/merged_dataset.csv


This file contains one row per panel with all relevant fields.

---

## Analysis Pipeline

Three Jupyter notebooks provide descriptive, statistical, and visualization‑based analysis.

### 1. `analysis.ipynb`
Performs:

- descriptive statistics  
- score distributions  
- correlation heatmaps  
- CDS vs LLM output length comparison  
- drift vs performance analysis  
- panel‑level inspection  

### 2. `analysis_stats.ipynb`
Performs:

- t‑tests  
- ANOVA  
- PCA  
- k‑means clustering  
- hierarchical clustering  

### 3. `analysis_visuals.ipynb`
Generates publication‑quality figures:

- ridge plots  
- violin plots  
- radar charts  
- heatmaps  
- Sankey‑style flow diagrams  

All notebooks operate directly on the merged dataset.

---

## Reproducibility

The entire pipeline is designed for full transparency and reproducibility:

- All raw data, intermediate outputs, and final datasets are included.  
- All scripts are deterministic and require no manual intervention.  
- All analysis notebooks can be executed end‑to‑end.  
- No proprietary data or paid API features were used.  

This ensures that other researchers can reproduce the study using only:

- the free Gemini API  
- the provided code  
- the included dataset  

---

## Limitations

This study uses a **small, curated dataset** due to free‑tier API constraints. As such:

- results are not intended to generalize to all clinical scenarios  
- statistical power is limited  
- ceiling effects are expected in well‑structured panels  

The primary contribution is methodological: a reproducible framework for evaluating multi‑lab clinical reasoning in LLMs.

---

## Summary

This pipeline demonstrates a transparent, reproducible method for evaluating LLM clinical reasoning using structured lab panels, deterministic CDS baselines, rubric‑based scoring, and automated analysis. The approach is intentionally lightweight and accessible, enabling meaningful evaluation even with limited API resources.

CDS files are stored in:

