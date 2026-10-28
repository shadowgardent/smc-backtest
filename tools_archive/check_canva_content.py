import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2314/output.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

for p_idx, page in enumerate(data.get("pages", [])):
    texts = []
    for rt in page.get("richtexts", []):
        t = rt.get("text", "").strip()
        if t: texts.append(t)
    combined = " | ".join(texts)
    print(f"--- PAGE {p_idx+1} ({len(texts)} texts) ---")
    if any(k in combined for k in ["ประเมิน", "ความพึงพอใจ", "4.52", "4.", "ดีมาก", "Evaluation", "สถาปัตยกรรม", "Flow", "Data Flow"]):
        print("  MATCH:", combined[:200])
    else:
        print("  Preview:", combined[:120])
