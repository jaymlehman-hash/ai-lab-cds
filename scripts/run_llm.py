import csv
import os
import time
import json
import requests
from requests.exceptions import HTTPError

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_NAME = "gemini-2.0-flash"
OUTPUT_DIR = "outputs/llm/gemini_v1"

# Rate limiting settings
REQUEST_DELAY = 1.5          # seconds between requests (prevents RPM throttling)
MAX_RETRIES = 5              # retry attempts for 429/500 errors
BACKOFF_FACTOR = 2           # exponential backoff multiplier

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
            status = response.status