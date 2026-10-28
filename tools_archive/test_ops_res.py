import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2344/output.txt", "r", encoding="utf-8") as f:
    data = json.loads(f.readline().strip())

for rt in data.get("richtexts", []):
    if rt.get("page_index") == 16:
        text = "".join(r.get("text", "") for r in rt.get("regions", []))
        if any(k in text for k in ["4.08", "ความพึงพอใจ", "ผลการประเมิน"]):
            print(f"Verified Page 16 text: '{text}'")
