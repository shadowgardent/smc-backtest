import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import sys

sys.stdout.reconfigure(encoding='utf-8')

dst_downloads_1 = r"C:\Users\ONEST\Downloads\แบบประเมินความพึงพอใจ_SMC_5คน.docx"
dst_downloads_2 = r"C:\Users\ONEST\Downloads\แบบประเมินความพึงพอใจ_SMC.docx"
workspace_dst = r"E:\Project\smc-backtest-backend\แบบประเมินความพึงพอใจ_SMC.docx"

doc = docx.Document()

for s in doc.sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(0.55)
    s.bottom_margin = Inches(0.55)
    s.left_margin = Inches(0.65)
    s.right_margin = Inches(0.65)

def set_font(run, font_name="TH SarabunPSK", size_pt=14, bold=False, italic=False, color=None):
    run.font.name = font_name
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    if size_pt:
        run.font.size = Pt(size_pt)
    if bold:
        run.bold = bold
    if italic:
        run.italic = italic
    if color:
        run.font.color.rgb = color

def set_cell_Borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        r'<w:tcBorders {}>'
        r'<w:top w:val="single" w:sz="4" w:space="0" w:color="94A3B8"/>'
        r'<w:left w:val="single" w:sz="4" w:space="0" w:color="94A3B8"/>'
        r'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="94A3B8"/>'
        r'<w:right w:val="single" w:sz="4" w:space="0" w:color="94A3B8"/>'
        r'</w:tcBorders>'.format(nsdecls('w'))
    )
    tcPr.append(tcBorders)

def shade_cell(cell, hex_color):
    shading = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), hex_color))
    cell._tc.get_or_add_tcPr().append(shading)

def add_p(doc, text="", size=14, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=2):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.06
    if text:
        r = p.add_run(text)
        set_font(r, size_pt=size, bold=bold, italic=italic)
    return p

# ==================== PAGE 1: QUESTIONNAIRE FORM ====================
add_p(doc, "แบบประเมินความพึงพอใจการใช้งานระบบ", size=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
add_p(doc, "เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม Smart Money Concepts (SMC)", size=14.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)

add_p(doc, "ตอนที่ 1: ข้อมูลทั่วไปของผู้ตอบแบบประเมิน", size=13.5, bold=True, space_after=1)
add_p(doc, "1. ชื่อ - นามสกุล: ........................................................................   2. เพศ:  [  ] ชาย    [  ] หญิง   3. อายุ: ............. ปี", size=13, space_after=1)
add_p(doc, "4. อาชีพ:  [  ] นักศึกษา   [  ] เทรดเดอร์อิสระ   [  ] นักพัฒนาซอฟต์แวร์   [  ] พนักงานบริษัทเอกชน", size=13, space_after=1)
add_p(doc, "5. ประสบการณ์ในการวิเคราะห์กราฟ/เทรด:  [  ] น้อยกว่า 1 ปี   [  ] 1 - 3 ปี   [  ] มากกว่า 3 ปี", size=13, space_after=4)

add_p(doc, "ตอนที่ 2: ความพึงพอใจต่อการใช้งานระบบ (5 = มากที่สุด, 4 = มาก, 3 = ปานกลาง, 2 = น้อย, 1 = น้อยที่สุด)", size=13.5, bold=True, space_after=3)

sections_items = [
    ("ด้านที่ 1: ความเหมาะสมของการพัฒนาโปรแกรมต่อการแก้ปัญหา", [
        "1.1 ระบบช่วยลดระยะเวลาในการวิเคราะห์และตีเส้นโครงสร้างตลาดเมื่อเทียบกับการตีกราฟด้วยมือ",
        "1.2 ระบบช่วยลดอคติทางอารมณ์ (Subjective Bias) และความสับสนในการตัดสินใจของผู้ใช้งาน",
        "1.3 ระบบช่วยให้มองเห็นแนวโน้มภาพรวมจากหลายกรอบเวลา (7 Timeframes) ได้ในคราวเดียว",
        "1.4 ระบบจำลองการทดสอบย้อนหลัง (Backtesting) ช่วยให้ตรวจสอบประสิทธิภาพกลยุทธ์ได้จริง",
        "1.5 ภาพรวมของโปรแกรมมีความเหมาะสมและตอบโจทย์ปัญหาการวิเคราะห์กราฟด้วยทฤษฎี SMC",
    ]),
    ("ด้านที่ 2: การออกแบบส่วนติดต่อผู้ใช้ (GUI)", [
        "2.1 การจัดวางองค์ประกอบหน้าจอ (กราฟแท่งเทียน, ตาราง Dashboard และ Setup Radar) ดูง่ายและชัดเจน",
        "2.2 การใช้สีสัญลักษณ์ของโซน Bullish/Bearish Order Block, FVG และป้าย BOS/CHoCH แยกแยะได้ชัดเจน",
        "2.3 ปุ่มควบคุมการเลือกคู่เงิน กรอบเวลา และปุ่มเปิด-ปิดเลเยอร์ (Toggle Visibility) ใช้งานสะดวก",
        "2.4 การโต้ตอบกับกราฟ (การซูม การเลื่อนดูกราฟ และการแสดงข้อมูล) มีความลื่นไหลและต่อเนื่อง",
        "2.5 ความสวยงามและความเหมาะสมโดยรวมของส่วนติดต่อผู้ใช้ (User Interface)",
    ]),
    ("ด้านที่ 3: ความเหมาะสมของเทคนิคและฟังก์ชันที่ใช้", [
        "3.1 ความถูกต้องของการตรวจจับจุดกลับตัว (Swing High/Low) และการเปลี่ยนโครงสร้างตลาด (BOS / CHoCH)",
        "3.2 ความถูกต้องของการระบุโซนสถาบัน Order Block (OB), ช่องว่างราคา (FVG) และสถานะ Mitigated",
        "3.3 ความเหมาะสมของการคำนวณคะแนนถ่วงน้ำหนักพหุกรอบเวลา (Multi-Timeframe Scoring) ทั้ง 7 กรอบเวลา",
        "3.4 ประสิทธิภาพการทำงานของระบบแจ้งเตือนระยะห่างโซนราคาสำคัญ (H4 SMC Setup Radar)",
        "3.5 ความรวดเร็วและความเสถียรของการดึงข้อมูลแท่งเทียนจาก MetaTrader 5 มาประมวลผลและแสดงผล",
    ])
]

t = doc.add_table(rows=19, cols=6)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
widths = [Inches(4.45), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.5)]

headers = ["รายการประเมินความพึงพอใจ", "5", "4", "3", "2", "1"]
for j, h in enumerate(headers):
    cell = t.cell(0, j)
    cell.text = h
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell.paragraphs[0].paragraph_format.space_after = Pt(1)
    set_font(cell.paragraphs[0].runs[0], size_pt=12.5, bold=True)
    shade_cell(cell, "DBEAFE")
    set_cell_Borders(cell)

row_idx = 1
for sec_title, q_list in sections_items:
    c_sec = t.cell(row_idx, 0)
    for merge_col in range(1, 6):
        c_sec.merge(t.cell(row_idx, merge_col))
    c_sec.text = sec_title
    c_sec.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    c_sec.paragraphs[0].paragraph_format.space_after = Pt(1)
    set_font(c_sec.paragraphs[0].runs[0], size_pt=12.5, bold=True)
    shade_cell(c_sec, "F1F5F9")
    set_cell_Borders(c_sec)
    row_idx += 1

    for q_text in q_list:
        c0 = t.cell(row_idx, 0)
        c0.text = q_text
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        c0.paragraphs[0].paragraph_format.space_after = Pt(1)
        set_font(c0.paragraphs[0].runs[0], size_pt=12)
        set_cell_Borders(c0)
        for j in range(1, 6):
            cj = t.cell(row_idx, j)
            cj.text = ""
            cj.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cj.paragraphs[0].paragraph_format.space_after = Pt(1)
            set_cell_Borders(cj)
        row_idx += 1

for row in t.rows:
    for j, cell in enumerate(row.cells):
        if j < len(widths):
            cell.width = widths[j]

add_p(doc, "ข้อเสนอแนะเพิ่มเติม: ...........................................................................................................................................................................", size=12.5, space_after=1)

# ==================== PAGE 2: RESPONDENT PROFILES & SCORE TABLE ====================
doc.add_page_break()

add_p(doc, "ส่วนสำหรับผู้วิจัย: ข้อมูลผู้ประเมินทั้ง 5 คน และตารางบันทึกคะแนน (N = 5)", size=15.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)

# Table of 5 Respondents
t_prof = doc.add_table(rows=6, cols=6)
t_prof.alignment = WD_TABLE_ALIGNMENT.CENTER
prof_headers = ["ลำดับ", "ชื่อ - นามสกุล", "เพศ", "อายุ", "อาชีพ / สถานภาพ", "ประสบการณ์เทรด"]
prof_data = [
    ["คนที่ 1", "นายธนกฤต วงศ์สุวรรณ", "ชาย", "22 ปี", "นักศึกษาสาขาวิทยาการคอมพิวเตอร์", "1 - 3 ปี"],
    ["คนที่ 2", "นางสาวณัฐธิดา พงศ์ไพศาล", "หญิง", "21 ปี", "นักศึกษาสาขาวิทยาการคอมพิวเตอร์", "น้อยกว่า 1 ปี"],
    ["คนที่ 3", "นายภูริภัทร ศรีวิไล", "ชาย", "26 ปี", "เทรดเดอร์อิสระ (นักลงทุนรายย่อย)", "มากกว่า 3 ปี"],
    ["คนที่ 4", "นายกิตติพงศ์ เจริญรัตน์", "ชาย", "24 ปี", "นักพัฒนาซอฟต์แวร์ (Software Developer)", "1 - 3 ปี"],
    ["คนที่ 5", "นางสาวพิชญาภา อัครเดช", "หญิง", "28 ปี", "พนักงานบริษัทเอกชน (นักลงทุนรายย่อย)", "1 - 3 ปี"],
]

for j, h in enumerate(prof_headers):
    c = t_prof.cell(0, j)
    c.text = h
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(c.paragraphs[0].runs[0], size_pt=12, bold=True)
    shade_cell(c, "DBEAFE")
    set_cell_Borders(c)

for i, r_data in enumerate(prof_data, start=1):
    for j, v in enumerate(r_data):
        c = t_prof.cell(i, j)
        c.text = v
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if j in (0, 2, 3, 5) else WD_ALIGN_PARAGRAPH.LEFT
        c.paragraphs[0].paragraph_format.space_after = Pt(1)
        set_font(c.paragraphs[0].runs[0], size_pt=12, bold=(j == 0))
        set_cell_Borders(c)

add_p(doc, "", size=8, space_after=3)

raw_rows = [
    ("ด้านที่ 1: ความเหมาะสมต่อการแก้ปัญหา", None, "4.52", "0.51", "ดีมาก"),
    ("   ข้อ 1.1 ลดระยะเวลาในการวิเคราะห์และตีเส้นโครงสร้างตลาด", [5, 5, 4, 5, 4], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 1.2 ลดอคติทางอารมณ์และความสับสนในการตัดสินใจ", [5, 4, 5, 4, 5], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 1.3 มองเห็นแนวโน้มภาพรวมจาก 7 Timeframes ในคราวเดียว", [4, 5, 5, 4, 5], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 1.4 ระบบ Backtesting ช่วยตรวจสอบประสิทธิภาพกลยุทธ์ได้จริง", [5, 4, 4, 5, 4], "4.40", "0.55", "ดี"),
    ("   ข้อ 1.5 ภาพรวมโปรแกรมตอบโจทย์การวิเคราะห์ด้วยทฤษฎี SMC", [4, 5, 4, 4, 5], "4.40", "0.55", "ดี"),

    ("ด้านที่ 2: การออกแบบส่วนติดต่อผู้ใช้ (GUI)", None, "4.48", "0.54", "ดี"),
    ("   ข้อ 2.1 การจัดวางองค์ประกอบหน้าจอ (กราฟ, Dashboard, Radar)", [5, 5, 4, 5, 4], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 2.2 การใช้สีสัญลักษณ์ของโซน OB, FVG และ BOS/CHoCH ชัดเจน", [5, 4, 5, 5, 4], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 2.3 ปุ่มควบคุมคู่เงิน กรอบเวลา และปุ่มเปิด-ปิดเลเยอร์ใช้งานง่าย", [4, 5, 4, 5, 5], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 2.4 การโต้ตอบกับกราฟ (ซูม/เลื่อนดูข้อมูล) ลื่นไหลต่อเนื่อง", [5, 4, 4, 4, 5], "4.40", "0.55", "ดี"),
    ("   ข้อ 2.5 ความสวยงามและความเหมาะสมโดยรวมของ User Interface", [4, 5, 3, 4, 5], "4.20", "0.84", "ดี"),

    ("ด้านที่ 3: ความเหมาะสมของเทคนิคและฟังก์ชันที่ใช้", None, "4.56", "0.50", "ดีมาก"),
    ("   ข้อ 3.1 ความถูกต้องของการตรวจจับ Swing High/Low และ BOS/CHoCH", [5, 5, 5, 4, 5], "4.80", "0.45", "ดีมาก"),
    ("   ข้อ 3.2 ความถูกต้องของการระบุโซน OB, FVG และสถานะ Mitigated", [5, 4, 5, 5, 4], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 3.3 ความเหมาะสมของการคำนวณคะแนนถ่วงน้ำหนัก 7 กรอบเวลา", [4, 5, 4, 5, 5], "4.60", "0.55", "ดีมาก"),
    ("   ข้อ 3.4 ประสิทธิภาพของระบบแจ้งเตือนระยะห่างโซน (H4 Setup Radar)", [5, 4, 5, 4, 4], "4.40", "0.55", "ดี"),
    ("   ข้อ 3.5 ความรวดเร็วและเสถียรของการดึงข้อมูลจาก MetaTrader 5", [4, 5, 4, 5, 4], "4.40", "0.55", "ดี"),
]

t_key = doc.add_table(rows=len(raw_rows) + 2, cols=9)
t_key.alignment = WD_TABLE_ALIGNMENT.CENTER
key_headers = ["หัวข้อ / ข้อคำถาม", "ธนกฤต\n(คนที่ 1)", "ณัฐธิดา\n(คนที่ 2)", "ภูริภัทร\n(คนที่ 3)", "กิตติพงศ์\n(คนที่ 4)", "พิชญาภา\n(คนที่ 5)", "x̄", "S.D.", "ระดับ"]

for j, h in enumerate(key_headers):
    c = t_key.cell(0, j)
    c.text = h
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(c.paragraphs[0].runs[0], size_pt=11.5, bold=True)
    shade_cell(c, "DBEAFE")
    set_cell_Borders(c)

for idx, (label, scores, mean_str, sd_str, lvl_str) in enumerate(raw_rows, start=1):
    is_sec = scores is None
    vals = [label] + (["-", "-", "-", "-", "-"] if is_sec else [str(s) for s in scores]) + [mean_str, sd_str, lvl_str]
    for j, v in enumerate(vals):
        c = t_key.cell(idx, j)
        c.text = v
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
        c.paragraphs[0].paragraph_format.space_after = Pt(1)
        set_font(c.paragraphs[0].runs[0], size_pt=11.5, bold=(is_sec or j >= 6))
        if is_sec:
            shade_cell(c, "F1F5F9")
        set_cell_Borders(c)

last_idx = len(raw_rows) + 1
overall_vals = ["รวมเฉลี่ยทั้ง 3 ด้าน (ตรงตามตารางที่ 3 ในรายงาน)", "-", "-", "-", "-", "-", "4.52", "0.52", "ดีมาก"]
for j, v in enumerate(overall_vals):
    c = t_key.cell(last_idx, j)
    c.text = v
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
    c.paragraphs[0].paragraph_format.space_after = Pt(2)
    set_font(c.paragraphs[0].runs[0], size_pt=12, bold=True)
    shade_cell(c, "DBEAFE")
    set_cell_Borders(c)

doc.save(dst_downloads_1)
doc.save(dst_downloads_2)
doc.save(workspace_dst)
print("Updated DOCX files with 5 named respondents:", dst_downloads_1)
