import csv
import os
import json
import requests

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_NAME = "gemini-1.5-pro"
OUTPUT_DIR = "outputs/llm/gemini_v1"

os.makedirs(OUTPUT_DIR, exist_ok=True)

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

def build_lab_block(row):
    labs = []
    for i in range(1, 10):
        name = row.get(f"lab_name_{i}")
        if not name:
            break
        value = row[f"value_{i}"]
        units = row[f"units_{i}"]
        ref = row[f"ref_range_{i}"]
        labs.append(f"- {name}: {value} {units} (reference {ref})")
    return "\n".join(labs)

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.0
        }
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("ERROR RESPONSE:", response.text)
    response.raise_for_status()

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def run_panel(row):
    panel_id = row["panel_id"]
    lab_block = build_lab_block(row)
    prompt = PROMPT_TEMPLATE.format(lab_block=lab_block)

    output = call_gemini(prompt)

    out_path = os.path.join(OUTPUT_DIR, f"{panel_id}_llm.txt")
    with open(out_path, "w") as f:
        f.write(output)

    print(f"Saved: {out_path}")

def main():
    with open("data/panels.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_panel(row)

if __name__ == "__main__":
    main()
