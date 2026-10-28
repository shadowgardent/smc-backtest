import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx")

for i, p in enumerate(doc.paragraphs):
    if any(k in p.text for k in ["4.52", "0.52", "4.48", "4.56", "0.51", "0.50", "0.54"]):
        print(f"P{i:02d}: '{p.text}'")
