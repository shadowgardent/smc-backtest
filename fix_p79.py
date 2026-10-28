import docx
from docx.shared import Pt
import sys
sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx"
doc = docx.Document(docx_path)

p79 = doc.paragraphs[79]
p79.text = p79.text.replace("อยู่ในระดับดีมาก โดยมีค่าเฉลี่ยรวมเท่ากับ 4.08", "อยู่ในระดับดี โดยมีค่าเฉลี่ยรวมเท่ากับ 4.08")
p79.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
for r in p79.runs:
    r.font.name = "TH SarabunPSK"
    r.font.size = Pt(14)

doc.save(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx")
doc.save(r"e:\Project\smc-backtest-backend\SMC_AUCC2026_Final.docx")

print("Fixed Section 7 word: ระดับดี")
