import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

pdf = fitz.open(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Checked.pdf")
page2 = pdf[1]
blocks = page2.get_text("dict")["blocks"]
for b in blocks:
    if "lines" in b:
        for l in b["lines"]:
            for s in l["spans"]:
                if "ภาพที่ 1" in s["text"] or "สถาปัตยกรรม" in s["text"]:
                    print(f"PDF span text: '{s['text']}', font: {s['font']}, size: {s['size']:.2f} pt")
