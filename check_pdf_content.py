import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Checked.pdf")
for i, page in enumerate(doc):
    text = page.get_text()
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first_3 = lines[:3] if lines else []
    last_3 = lines[-3:] if lines else []
    img_list = page.get_images()
    print(f"=== PAGE {i+1} ({len(lines)} lines, {len(img_list)} images) ===")
    print("  Top:", " | ".join(first_3))
    print("  Bottom:", " | ".join(last_3))
