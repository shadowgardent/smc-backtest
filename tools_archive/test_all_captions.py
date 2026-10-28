import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

pdf = fitz.open(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Checked.pdf")
print("=== CHECKING ALL CAPTIONS & HEADINGS IN PDF ===")
for p_no, page in enumerate(pdf):
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                line_text = "".join(s["text"] for s in l["spans"]).strip()
                if any(k in line_text for k in ["ภาพที่", "ตาราง", "1. บทนำ", "2. ทฤษฎี", "3. การออกแบบ", "4. การพัฒนา", "5. ผลการวิจัย", "6. อภิปราย", "7. สรุป", "เอกสารอ้างอิง"]):
                    span_details = " | ".join(f"{s['font']} ({s['size']:.1f}pt)" for s in l["spans"])
                    print(f"[Page {p_no+1}] '{line_text[:50]}' -> {span_details}")
