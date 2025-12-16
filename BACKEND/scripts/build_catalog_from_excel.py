import pandas as pd
import json

INPUT_FILE = "../data/Gen_AI Dataset.xlsx"
OUTPUT_FILE = "../data/assessments.json"

df = pd.read_excel(INPUT_FILE)

assessments = []

for _, row in df.iterrows():
    assessments.append({
        "name": str(row.get("Assessment Name", "")).strip(),
        "url": str(row.get("Assessment URL", "")).strip(),
        "description": str(row.get("Description", "")).strip(),
        "test_type": str(row.get("Test Type", "")).split(",")
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(assessments, f, indent=2, ensure_ascii=False)

print("Total assessments:", len(assessments))
