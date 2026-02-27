import csv
import os
from datetime import datetime
import google.generativeai as genai   # llm

#genai.configure(api_key=os.environ["GEMINI_API_KEY"])

genai.configure( api_key=os.environ["GEMINI_API_KEY"], transport="rest" )
MODEL_NAME = "gemini-1.0-pro"

PROMPT_TEMPLATE = """You are a clinical decision support system.
You are given multiple abnormal laboratory values from the same patient.

Provide a concise explanation of:
1) What each abnormal value may indicate, and
2) How these abnormalities may be related to each other, if at all.

Do not assume symptoms, history, or comorbidities beyond the labs provided.
Be explicit when a relationship is uncertain or speculative.
Temperature: 0.0

Abnormal labs:
{lab_block}
"""

# If you're curious about temperature 0.0, look it up.  0.0 means the model always picks the highest‑probability next token which I want

OUTPUT_DIR = "outputs/llm/gemini_v1"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_lab_block(row):
    labs = []
    for i in range(1, 10):  # supports up to 3 labs (lab_name_1, lab_name_2, lab_name_3)
        name = row.get(f"lab_name_{i}")
        if not name:
            break
        value = row[f"value_{i}"]
        units = row[f"units_{i}"]
        ref = row[f"ref_range_{i}"]
        labs.append(f"- {name}: {value} {units} (reference {ref})")
    return "\n".join(labs)

def run_panel(panel_row):
    panel_id = panel_row["panel_id"]
    lab_block = build_lab_block(panel_row)
    prompt = PROMPT_TEMPLATE.format(lab_block=lab_block)

    response = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)

    output_path = os.path.join(OUTPUT_DIR, f"{panel_id}_llm.txt")
    with open(output_path, "w") as f:
        f.write(response.text)

    print(f"Saved: {output_path}")

def main():
    with open("data/panels.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_panel(row)

if __name__ == "__main__":
    main()
