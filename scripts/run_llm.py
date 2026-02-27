import csv
import os
import time
import json
import requests
from requests.exceptions import HTTPError

#API_KEY = os.environ["GEMINI_API_KEY"]
API_KEY = "AIzaSyD7Jj3wciNAB4rwL6SjE0q8Ze30fu8G1mA"
MODEL_NAME = "gemini-2.0-flash"
OUTPUT_DIR = "outputs/llm/gemini_v1"

# Rate limiting settings
REQUEST_DELAY = 1.5          # seconds between requests (prevents RPM throttling)
MAX_RETRIES = 5              # retry attempts for 429/500 errors
BACKOFF_FACTOR = 2           # exponential backoff multiplier

os.makedirs(OUTPUT_DIR, exist_ok=True)

PROMPT_TEMPLATE = """You are a clinical decision support system. You will be given multiple abnormal laboratory values from the same patient.

Your task is to produce a concise, structured explanation that includes:

1. **Individual Lab Interpretation**  
   For each abnormal lab value, explain what the abnormality may indicate.  
   Use physiologic mechanisms, common clinical associations, and well‑established patterns of interpretation.  
   Do not assume symptoms, diagnoses, or history that are not explicitly provided.

2. **Inter‑Lab Relationships**  
   Identify and explain any possible relationships between the abnormal labs.  
   Include:
   - Direct physiologic relationships  
   - Indirect or research‑supported associations  
   - Shared mechanisms (e.g., inflammation, metabolic dysfunction, oxidative stress)  
   - Patterns seen in population‑level studies  
   - Known associations involving iron overload, ferritin, and uric acid when relevant  
   - Situations where labs may be abnormal for unrelated reasons  

   When a relationship is uncertain, state that explicitly.  
   When a relationship is supported by research but not universally recognized in guidelines, state that clearly.

3. **Reasoning Transparency**  
   Keep reasoning grounded strictly in the provided lab values.  
   Do not infer symptoms, comorbidities, medications, or clinical context beyond what is given.  
   Avoid definitive diagnostic statements.  
   Use cautious, conditional language (“may suggest”, “can be associated with”, “is sometimes seen with”).

4. **Output Format**  
   Produce two sections:

   **A. Individual Lab Explanations**  
   - Lab 1: …  
   - Lab 2: …  
   - etc.

   **B. Possible Relationships Between Abnormal Labs**  
   - Relationship 1: …  
   - Relationship 2: …  
   - etc.  
   Include both direct and indirect associations when supported by physiology or research.

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
        value = row.get(f"value_{i}", "")
        units = row.get(f"units_{i}", "")
        ref = row.get(f"ref_range_{i}", "")
        labs.append(f"- {name}: {value} {units} (reference {ref})")
    return "\n".join(labs)

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {"temperature": 0.0}
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f"ERROR RESPONSE (attempt {attempt}): {response.text}")

            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except HTTPError as e:
            status = response.status_code

            # Retry only on quota or transient errors
            if status in (429, 500, 502, 503, 504):
                sleep_time = BACKOFF_FACTOR ** attempt
                print(f"Retryable error {status}. Sleeping {sleep_time}s before retry {attempt}/{MAX_RETRIES}...")
                time.sleep(sleep_time)
                continue

            # Non-retryable error
            print(f"Non-retryable error {status}: {response.text}")
            return f"ERROR: {response.text}"

        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"ERROR: {e}"

    return "ERROR: Max retries exceeded."

def run_panel(row):
    panel_id = row["panel_id"]
    lab_block = build_lab_block(row)
    prompt = PROMPT_TEMPLATE.format(lab_block=lab_block)

    print(f"Processing panel {panel_id}...")
    output = call_gemini(prompt)

    out_path = os.path.join(OUTPUT_DIR, f"{panel_id}_llm.txt")
    with open(out_path, "w") as f:
        f.write(output)

    print(f"Saved: {out_path}")
    time.sleep(REQUEST_DELAY)  # rate limiting

def main():
    with open("data/panels.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_panel(row)

if __name__ == "__main__":
    main()
