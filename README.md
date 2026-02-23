# Studying How Large Language Models Reframe Disease Risk in Lab Result Explanations

## Overview

This project explores how large language models (LLMs) — such as Gemini — frame clinical meaning when explaining abnormal laboratory results. Traditional electronic health record (EHR) systems rely on deterministic, rule‑based logic to interpret labs. LLMs, by contrast, generate narrative explanations based on patterns learned from medical text.

This shift introduces a new question:

**Do LLM‑generated explanations subtly broaden or reframe associations with comorbid conditions compared to traditional rule‑based clinical decision support?**

This repository documents a structured, reproducible set of experiments to answer that question.

---

## Why This Matters

As health systems integrate generative AI into clinical workflows, explanation generation becomes part of the production system. That means:

- framing affects clinical interpretation  
- narrative drift becomes a system behavior  
- LLM outputs become part of the safety surface  
- DevOps teams must monitor not just accuracy, but *language*  

Traditional CDS is deterministic and testable.  
LLM‑based explanations are probabilistic and narrative.

Understanding this difference is essential before AI systems “speak” for the medical record.

---

## Research Questions

This project evaluates whether LLM‑generated explanations differ from rule‑based CDS in:

- **breadth of associated conditions**  
- **strength of associative or causal language**  
- **certainty framing**  
- **implied clinical significance**  
- **narrative expansion beyond guideline‑encoded rules**

This work does *not* evaluate clinical correctness or provide medical advice.  
It evaluates **framing behavior**.

---

## Methodology

### 1. Labs‑Only Scenarios
Each experiment uses a single abnormal lab value (e.g., elevated uric acid) with no additional clinical context.

### 2. Two Explanation Sources
- **Rule‑based CDS**: deterministic, threshold‑based logic  
- **LLM‑generated explanation**: Gemini, using a controlled prompt  

### 3. Evaluation Dimensions
Each explanation is scored on:

- number of conditions mentioned  
- associative language strength  
- certainty language  
- implied clinical significance  
- narrative breadth  

### 4. Reproducible Prompting
All LLM prompts are:

- fixed  
- version‑controlled  
- executed with temperature = 0.0 when possible  
- logged for reproducibility  

### 5. Output Comparison
Outputs are compared qualitatively and quantitatively to identify framing differences.

---

## Planned Deliverables

- A dataset of lab‑only scenarios  
- A reproducible Gemini prompt suite  
- A comparison table of rule‑based vs. LLM explanations  
- A write‑up summarizing framing differences  
- A LinkedIn article series documenting findings  

---

## Repository Structure (Proposed)

