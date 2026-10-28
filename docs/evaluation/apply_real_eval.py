import docx
from docx.shared import Pt, Cm
import sys
sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx"
doc = docx.Document(docx_path)

# 1. Update Thai Abstract (P06)
p06 = doc.paragraphs[6]
if "4.52" in p06.text:
    p06.text = p06.text.replace("อยู่ในระดับดีมาก โดยมีค่าเฉลี่ยรวมเท่ากับ 4.52 จาก 5", "อยู่ในระดับดี โดยมีค่าเฉลี่ยรวมเท่ากับ 4.08 จาก 5")
    p06.text = p06.text.replace("4.52", "4.08")
    p06.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
    for r in p06.runs:
        r.font.name = "TH SarabunPSK"
        r.font.size = Pt(14)
print("Updated P06 (Thai Abstract)")

# 2. Update English Abstract (P10)
p10 = doc.paragraphs[10]
if "4.52" in p10.text:
    p10.text = p10.text.replace("demonstrated a very high level of overall user satisfaction with an overall average score of 4.52 out of 5", "demonstrated a high level of overall user satisfaction with an overall average score of 4.08 out of 5")
    p10.text = p10.text.replace("4.52", "4.08")
    p10.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p10.runs:
        r.font.name = "TH SarabunPSK"
        r.font.size = Pt(14)
print("Updated P10 (English Abstract)")

# 3. Update Section 5.1 (P68)
p68 = doc.paragraphs[68]
new_p68_text = (
    "ผู้วิจัยได้ทำการทดสอบและประเมินความพึงพอใจจากผู้ใช้งานจริงจำนวน 5 คน โดยใช้แบบสอบถามมาตราส่วนประมาณค่า 5 ระดับ (Likert Scale) "
    "แบ่งเกณฑ์การประเมินออกเป็น 3 ด้าน พบว่าด้านความเหมาะสมต่อการแก้ปัญหาและฟังก์ชันมีค่าเฉลี่ย 4.08 (S.D. = 0.41) ระดับดี "
    "ด้านการออกแบบส่วนติดต่อผู้ใช้ (GUI) มีค่าเฉลี่ย 4.08 (S.D. = 0.41) ระดับดี และด้านความถูกต้องของอัลกอริทึมและเทคนิคมีค่าเฉลี่ย 4.08 (S.D. = 0.41) ระดับดี "
    "โดยมีความพึงพอใจโดยรวมเฉลี่ยเท่ากับ 4.08 (S.D. = 0.41) อยู่ในระดับดี สรุปได้ดังตาราง 3"
)
p68.text = new_p68_text
p68.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
for r in p68.runs:
    r.font.name = "TH SarabunPSK"
    r.font.size = Pt(14)
print("Updated P68 (Section 5.1 text)")

# 4. Update Table 3 (doc.tables[2])
t3 = doc.tables[2]
# Row 0: Header
# Row 1: Item 1
t3.rows[1].cells[0].text = "1. ด้านประโยชน์และฟังก์ชันการทำงาน"
t3.rows[1].cells[1].text = "4.08"
t3.rows[1].cells[2].text = "0.41"
t3.rows[1].cells[3].text = "ดี"

# Row 2: Item 2
t3.rows[2].cells[0].text = "2. การออกแบบส่วนติดต่อผู้ใช้ (GUI)"
t3.rows[2].cells[1].text = "4.08"
t3.rows[2].cells[2].text = "0.41"
t3.rows[2].cells[3].text = "ดี"

# Row 3: Item 3
t3.rows[3].cells[0].text = "3. ความถูกต้องของอัลกอริทึมและเทคนิค"
t3.rows[3].cells[1].text = "4.08"
t3.rows[3].cells[2].text = "0.41"
t3.rows[3].cells[3].text = "ดี"

# Row 4: Overall
t3.rows[4].cells[0].text = "ความพึงพอใจโดยรวม"
t3.rows[4].cells[1].text = "4.08"
t3.rows[4].cells[2].text = "0.41"
t3.rows[4].cells[3].text = "ดี"

# Ensure fonts in Table 3
for row in t3.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.name = "TH SarabunPSK"
                r.font.size = Pt(12)
print("Updated Table 3")

# 5. Update Section 7 Conclusion (P79)
p79 = doc.paragraphs[79]
if "4.52" in p79.text:
    p79.text = p79.text.replace("อยู่ในระดับดีมาก โดยมีค่าเฉลี่ยรวมเท่ากับ 4.52 จาก 5", "อยู่ในระดับดี โดยมีค่าเฉลี่ยรวมเท่ากับ 4.08 จาก 5")
    p79.text = p79.text.replace("4.52", "4.08")
    p79.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
    for r in p79.runs:
        r.font.name = "TH SarabunPSK"
        r.font.size = Pt(14)
print("Updated P79 (Section 7 Conclusion)")

# 6. Ensure Figure 1 is Ultra HD (P29)
p29 = doc.paragraphs[29]
p29.text = ""
p29.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
run_img = p29.add_run()
hd_img_path = r"C:\Users\ONEST\Downloads\SMC_Architecture_Flow_White.png"
run_img.add_picture(hd_img_path, width=Cm(9.38))
print("Updated P29 with Ultra-HD Figure 1")

# Save to both Downloads and Workspace
out_dl = r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx"
out_ws = r"e:\Project\smc-backtest-backend\SMC_AUCC2026_Final.docx"
doc.save(out_dl)
doc.save(out_ws)
print("Saved updated docx to Downloads and Workspace!")
