# Results

This study evaluated the clinical reasoning performance of **Gemini 2.X Flash** on a curated set of nine multi‑lab panels. Each panel contained three abnormal laboratory values spanning metabolic, renal, hepatic, endocrine, hematologic, or cardiovascular domains. The model was assessed using a structured scoring rubric measuring correctness, completeness, relationship detection, relationship accuracy, narrative drift, certainty language, mechanistic depth, and structural adherence.

All results were generated using a fully reproducible pipeline, including automated LLM generation, rubric‑based scoring, dataset merging, and analysis notebooks.

---

## Overall Performance

Across all nine panels, Gemini 2.X Flash demonstrated **consistently high performance**. Every panel achieved the maximum total score of **25/25**, with perfect or near‑perfect scores in all rubric dimensions.

### Summary of scoring outcomes

| Dimension | Max Score | Mean | Std Dev | Interpretation |
|----------|-----------|------|---------|----------------|
| Correctness | 4 | 4.0 | 0.0 | Accurate interpretation of all abnormal labs |
| Completeness | 3 | 3.0 | 0.0 | All abnormal labs addressed |
| Relationship Detection | 4 | 4.0 | 0.0 | All direct, indirect, and research‑supported relationships identified |
| Relationship Accuracy | 3 | 3.0 | 0.0 | Physiologic mechanisms described correctly |
| Narrative Drift | 3 | 3.0 | 0.0 | No unsupported assumptions or hallucinations |
| Certainty Language | 2 | 2.0 | 0.0 | Appropriate use of conditional phrasing |
| Mechanistic Depth | 4 | 4.0 | 0.0 | Strong physiologic explanations |
| Structure Adherence | 2 | 2.0 | 0.0 | Perfect compliance with required output format |
| **Total Score** | **25** | **25.0** | **0.0** | Consistent high‑quality reasoning |

These results indicate that, for the curated panel set used in this study, Gemini 2.X Flash produced **accurate, structured, and mechanistically grounded clinical reasoning** with minimal drift.

---

## CDS vs LLM Output Characteristics

To contextualize LLM performance, each panel also included a deterministic **Clinical Decision Support (CDS)** baseline consisting of short, per‑lab explanations with no relational reasoning.

### Key differences observed

- **LLM outputs were substantially longer** than CDS outputs, reflecting richer narrative and mechanistic detail.
- **CDS outputs remained strictly per‑lab**, while the LLM consistently produced **multi‑lab relational reasoning**, identifying physiologic, metabolic, and research‑supported connections.
- **LLM outputs adhered to the required structure**, while CDS outputs were intentionally minimal.

A scatterplot of CDS vs LLM output length showed a clear separation, with LLM outputs clustering at significantly higher character counts.

---

## Drift and Mechanistic Reasoning

Narrative drift was consistently low across all panels. The model:

- avoided unsupported diagnoses  
- used conditional language appropriately  
- distinguished between established mechanisms and research‑supported associations  
- maintained focus on the provided labs without introducing extraneous speculation  

Mechanistic reasoning was uniformly strong. The model consistently explained:

- enzyme pathways  
- renal clearance mechanisms  
- metabolic interactions  
- endocrine feedback loops  
- inflammatory and oxidative stress pathways  

This depth contributed to high relationship accuracy scores.

---

## Relationship Detection

Gemini 2.0 Flash reliably identified:

- direct physiologic relationships (e.g., creatinine ↔ eGFR)  
- indirect or research‑supported relationships (e.g., iron overload ↔ hypertension)  
- shared underlying mechanisms (e.g., metabolic syndrome, inflammation, oxidative stress)  

The model also correctly qualified weaker or non‑causal associations, demonstrating appropriate epistemic caution.

---

## Outlier Analysis

Because all panels scored identically, no statistical outliers were observed. However, qualitative inspection confirmed that the model maintained consistent structure, depth, and accuracy across diverse panel types.

---

## Qualitative Examples

Manual inspection of representative panels (e.g., P001, P003, P005) showed:

- clear, structured explanations for each abnormal lab  
- accurate physiologic mechanisms  
- correct identification of multi‑lab relationships  
- appropriate use of uncertainty language  
- no hallucinations or irrelevant content  

These examples illustrate the model’s ability to produce clinically coherent reasoning even in a small dataset.

---

## Interpretation of Findings

The small dataset used in this study limits generalizability, but the results demonstrate that:

- The **pipeline is fully functional**, reproducible, and scalable.  
- The **scoring rubric is effective** at evaluating multi‑lab reasoning.  
- Gemini 2.0 Flash performs **consistently well** on curated, well‑structured panels.  
- The model exhibits **low drift**, **high mechanistic depth**, and **strong relational reasoning**.  

These findings support the feasibility of using structured lab panels and rubric‑based scoring to evaluate LLM clinical reasoning, even with limited API resources.

---

## Reproducibility

All data, code, scoring outputs, and analysis notebooks are included in the repository:

- `data/panels.csv`  
- `outputs/cds/`  
- `outputs/llm/gemini_v1/`  
- `outputs/scoring/`  
- `outputs/dataset/merged_dataset.csv`  
- `notebooks/analysis.ipynb`  
- `notebooks/analysis_stats.ipynb`  
- `notebooks/analysis_visuals.ipynb`  

This ensures full transparency and enables other researchers to reproduce or extend the study.
