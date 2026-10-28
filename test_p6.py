import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2322/output.txt", "r", encoding="utf-8") as f:
    line0 = f.readline().strip()
    data = json.loads(line0)

richtexts = data.get("richtexts", [])
for rt in richtexts:
    if rt.get("page_index") == 6:
        text = "".join(r.get("text", "") for r in rt.get("regions", []))
        print("Page 6 Text:", text, "| Element:", rt.get("element_id"))

media = data.get("media", [])
print(f"\nTotal media elements in presentation: {len(media)}")
for m in media:
    if m.get("page_index") in [6, 16]:
        print(f"Media on Page {m.get('page_index')}: {m}")
