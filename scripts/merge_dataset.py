import os
import csv
import json
import pandas as pd

PANELS_CSV = "data/panels.csv"
LLM_DIR = "outputs/llm/gemini_v2"
CDS_DIR = "outputs/cds"
SCORING_DIR = "outputs/scoring"
OUTPUT_DIR = "outputs/dataset"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "merged_dataset.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_text_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def load_json_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    panels = pd.read_csv(PANELS_CSV)

    merged_rows = []

    for _, row in panels.iterrows():
        panel_id = row["panel_id"]

        llm_path = os.path.join(LLM_DIR, f"{panel_id}_llm.txt")
        cds_path = os.path.join(CDS_DIR, f"{panel_id}_cds.txt")
        print(cds_path)
        score_path = os.path.join(SCORING_DIR, f"{panel_id}_score.json")

        llm_output = load_text_file(llm_path)
        cds_output = load_text_file(cds_path)
        
        scoring = load_json_file(score_path)

        merged = dict(row)
        merged["llm_output"] = llm_output
        merged["cds_output"] = cds_output

        if scoring:
            for key, value in scoring.items():
                merged[key] = value
        else:
            merged["scoring_missing"] = True

        merged_rows.append(merged)

    df = pd.DataFrame(merged_rows)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Merged dataset saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
