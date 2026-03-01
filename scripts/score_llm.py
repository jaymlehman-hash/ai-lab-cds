import os
import csv
import json
import time
import requests
from requests.exceptions import HTTPError

#API_KEY = os.environ["GEMINI_API_KEY"]
# Should I use a different model for the scoring?
MODEL_NAME = "gemini-2.5-flash"

LLM_OUTPUT_DIR = "outputs/llm/gemini_v2"
SCORING_OUTPUT_DIR = "outputs/scoring"

os.makedirs(SCORING_OUTPUT_DIR, exist_ok=True)

REQUEST_DELAY = 1.5
MAX_RETRIES = 5
BACKOFF_FACTOR = 2

SCORING_PROMPT = """
You are evaluating the quality of a clinical reasoning output generated from abnormal laboratory values.

Use the following scoring rubric. Return ONLY a JSON object with the fields listed below. Do not include commentary outside the JSON.

Rubric:

1. correctness_score (0–4): Accuracy of individual lab interpretations.
2. completeness_score (0–3): Whether all abnormal labs were addressed.
3. relationship_detection_score (0–4): Identification of direct, indirect, and research-supported relationships.
4. relationship_accuracy_score (0–3): Physiologic accuracy of identified relationships.
5. narrative_drift_score (0–3): Degree of unsupported assumptions (higher = less drift).
6. certainty_score (0–2): Appropriate use of conditional language.
7. mechanistic_score (0–4): Depth of physiologic/mechanistic reasoning.
8. structure_score (0–2): Adherence to required structure.

Return a JSON object with these fields:

{{
  "panel_id": "<string>",
  "correctness_score": <int>,
  "correctness_explanation": "<string>",
  "completeness_score": <int>,
  "completeness_explanation": "<string>",
  "relationship_detection_score": <int>,
  "relationship_detection_explanation": "<string>",
  "relationship_accuracy_score": <int>,
  "relationship_accuracy_explanation": "<string>",
  "narrative_drift_score": <int>,
  "narrative_drift_explanation": "<string>",
  "certainty_score": <int>,
  "certainty_explanation": "<string>",
  "mechanistic_score": <int>,
  "mechanistic_explanation": "<string>",
  "structure_score": <int>,
  "structure_explanation": "<string>",
  "total_score": <int>
}}

Now evaluate the following LLM output:

PANEL ID:
{panel_id}

LLM OUTPUT:
{llm_output}
"""

def strip_code_fences(text):
    text = text.strip()
    if text.startswith("```"):
        # Remove leading ```json or ```
        first_newline = text.find("\n")
        text = text[first_newline+1:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0}
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f"ERROR RESPONSE (attempt {attempt}): {response.text}")
                exit(0)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except HTTPError:
            status = response.status_code
            if status in (429, 500, 502, 503, 504):
                sleep_time = BACKOFF_FACTOR ** attempt
                print(f"Retryable error {status}. Sleeping {sleep_time}s before retry {attempt}/{MAX_RETRIES}...")
                time.sleep(sleep_time)
                continue
            print(f"Non-retryable error {status}: {response.text}")
            return None

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    return None

def score_panel(panel_id, llm_output):
    prompt = SCORING_PROMPT.format(panel_id=panel_id, llm_output=llm_output)
    result = call_gemini(prompt)

    if result is None:
        return None

    cleaned = strip_code_fences(result)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print(f"JSON decode error for panel {panel_id}. Cleaned output:")
        print(cleaned)
        return None

def main():
    for filename in os.listdir(LLM_OUTPUT_DIR):
        if not filename.endswith("_llm.txt"):
            continue

        panel_id = filename.replace("_llm.txt", "")
        llm_path = os.path.join(LLM_OUTPUT_DIR, filename)

        with open(llm_path, "r") as f:
            llm_output = f.read().strip()

        print(f"Scoring panel {panel_id}...")
        scoring = score_panel(panel_id, llm_output)

        if scoring:
            out_path = os.path.join(SCORING_OUTPUT_DIR, f"{panel_id}_score.json")
            with open(out_path, "w") as f:
                json.dump(scoring, f, indent=2)
            print(f"Saved: {out_path}")
        else:
            print(f"Failed to score panel {panel_id}")

        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    main()
