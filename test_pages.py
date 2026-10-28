import json
with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2322/output.txt", "r", encoding="utf-8") as f:
    data = json.loads(f.readline().strip())

pages = data.get("pages", [])
print(f"Pages count: {len(pages)}")
print("Sample page:", pages[0])
