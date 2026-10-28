import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2322/output.txt", "r", encoding="utf-8") as f:
    line0 = f.readline().strip()
    data = json.loads(line0)

richtexts = data.get("richtexts", [])
print("First richtext object keys:", richtexts[0].keys() if richtexts else "None")
print("First richtext sample:", richtexts[0] if richtexts else "None")

# Print all elements on the last 30 richtexts
for rt in richtexts[160:]:
    print(f"Page ID: {rt.get('page_id')} | Box ID: {rt.get('box_id')} | Content: {rt}")
