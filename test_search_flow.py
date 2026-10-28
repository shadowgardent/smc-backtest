import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:/Users/ONEST/Downloads/canva_tx_full.json", "w", encoding="utf-8") as out:
    pass

with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2322/output.txt", "r", encoding="utf-8") as f:
    line0 = f.readline().strip()
    data = json.loads(line0)

richtexts = data.get("richtexts", [])

for rt in richtexts:
    text = "".join(r.get("text", "") for r in rt.get("regions", []))
    pidx = rt.get("page_index")
    eid = rt.get("element_id")
    if any(k in text for k in ["แผนภาพ", "การไหล", "วิธีใช้งาน"]):
        print(f"Page {pidx} | EID: {eid} | Text: '{text}'")
