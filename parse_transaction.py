import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2322/output.txt", "r", encoding="utf-8") as f:
    line = f.readline().strip()
    data = json.loads(line)

tid = data.get("transaction_id")
print("Transaction ID:", tid)

pages = data.get("pages", [])
print(f"Total pages: {len(pages)}")

for p_idx, page in enumerate(pages):
    pid = page.get("page_id")
    elements = page.get("elements", [])
    found = []
    for el in elements:
        t = el.get("text", "")
        eid = el.get("element_id")
        etype = el.get("type")
        if any(k in t for k in ["4.52", "4.48", "4.56", "ผลการประเมิน", "แผนภาพการไหล", "ดีมาก"]):
            found.append((eid, etype, t))
    if found:
        print(f"\nPage {p_idx+1} (ID: {pid}):")
        for eid, etype, t in found:
            print(f"  [{eid}] ({etype}): {t}")
