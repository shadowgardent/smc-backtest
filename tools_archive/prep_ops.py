import json

with open(r"C:/Users/ONEST/.gemini/antigravity/brain/a19985bc-fcd1-432f-9cb1-a7239ee1919d/.system_generated/steps/2322/output.txt", "r", encoding="utf-8") as f:
    data = json.loads(f.readline().strip())

tid = data["transaction"]["transaction_id"]
pages = data["pages"]

operations = [
    {
        "type": "replace_text",
        "element_id": "PBv0pM065QqstVmH-LB3ttGzkb9zGh0tb-LBg4Fmn05lRCz0Cv",
        "text": "4.08"
    },
    {
        "type": "replace_text",
        "element_id": "PBv0pM065QqstVmH-LB3ttGzkb9zGh0tb-LBnJgNlqrjTdw4C2",
        "text": "ค่าเฉลี่ยความพึงพอใจ (ระดับดี)"
    },
    {
        "type": "replace_text",
        "element_id": "PBv0pM065QqstVmH-LB3ttGzkb9zGh0tb-LB434P73fcD1SpF1",
        "text": "ประโยชน์ 4.08 • UI/UX 4.08 • ฟังก์ชัน 4.08"
    }
]

args = {
    "transaction_id": tid,
    "page_index": 16,
    "pages": pages,
    "operations": operations,
    "user_intent": "Update evaluation score from 4.52 to real score 4.08 on Slide 16"
}

with open("perform_ops_args.json", "w", encoding="utf-8") as f:
    json.dump(args, f, ensure_ascii=False, indent=2)

print("Saved perform_ops_args.json")
