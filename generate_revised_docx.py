import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_path = r"C:\Users\ONEST\Downloads\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม Smart Money Concepts (SMC).docx"
dst_path = r"C:\Users\ONEST\Downloads\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx"
workspace_dst = r"E:\Project\smc-backtest-backend\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx"

doc = docx.Document(src_path)

def set_run_font(run, font_name="TH SarabunPSK", size_pt=14, bold=None, italic=None, color=None):
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
    
    if size_pt is not None:
        run.font.size = Pt(size_pt)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = color

def set_p_text(p, text, font_name="TH SarabunPSK", size_pt=14, bold=False, italic=False, align=None):
    p.text = ""
    run = p.add_run(text)
    set_run_font(run, font_name, size_pt, bold, italic)
    if align is not None:
        p.alignment = align

# 1. Clean Header highlights
for section in doc.sections:
    for hp in section.header.paragraphs:
        for hr in hp.runs:
            hr.font.highlight_color = None
            set_run_font(hr, "TH SarabunPSK", 10)

# Check paragraphs length
print("Processing paragraphs...")

# Title & Abstract
# P000: Title Thai
set_p_text(doc.paragraphs[0], "เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม Smart Money Concepts (SMC)", size_pt=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
# P001: Title English
set_p_text(doc.paragraphs[1], "FINANCIAL MARKET STRUCTURE ANALYSIS AND VISUALIZATION TOOL USING SMART MONEY CONCEPTS (SMC) ALGORITHMS", size_pt=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
# P002: จัดทำโดย
set_p_text(doc.paragraphs[2], "จัดทำโดย", size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER)
# P003: Author
set_p_text(doc.paragraphs[3], "นายนวพรหม ภูผาผิว 663450040-2", size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER)

# P009: บทคัดย่อ heading
set_p_text(doc.paragraphs[9], "บทคัดย่อ", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P010: Thai Abstract text
thai_abstract = (
    "นักลงทุนรายย่อยในตลาดการเงินมีอัตราการขาดทุนสูงถึง 60–80% ซึ่งมีสาเหตุสำคัญมาจากอคติทางอารมณ์ "
    "และความไม่เป็นปรนัยของการวิเคราะห์โครงสร้างตลาดด้วยสายตาเปล่า บทความนี้นำเสนอการพัฒนาเว็บแอปพลิเคชัน"
    "เพื่อวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินแบบอัตโนมัติ โดยประยุกต์ใช้อัลกอริทึมเชิงกฎเกณฑ์ (Rule-based Algorithm) "
    "ร่วมกับเทคนิค Look-back และ Look-forward ในการตรวจจับจุด Swing High, Swing Low, การเบรกโครงสร้างราคา (BOS), "
    "การเปลี่ยนแนวโน้ม (CHoCH) และ Order Block พร้อมกลไกวิเคราะห์ 7 กรอบเวลาแบบถ่วงน้ำหนัก (Multi-Timeframe Scoring) "
    "และแสดงผลผ่านกราฟแท่งเทียนเชิงโต้ตอบด้วยไลบรารี TradingView Lightweight Charts ในการประเมินผล ได้ทดสอบการใช้งานจริง"
    "กับกลุ่มตัวอย่างและประเมินความพึงพอใจ 3 ด้าน ได้แก่ ความเหมาะสมของการพัฒนาโปรแกรมต่อการแก้ปัญหา การออกแบบส่วนติดต่อผู้ใช้ (GUI) "
    "และความเหมาะสมของเทคนิคและฟังก์ชันที่ใช้ ผลการประเมินพบว่า กลุ่มผู้ใช้งานมีความพึงพอใจโดยรวมอยู่ในระดับดีมาก "
    "โดยมีความเหมาะสมต่อการแก้ปัญหาเฉลี่ย (x̄ = 4.52, S.D. = 0.51) การออกแบบ GUI เฉลี่ย (x̄ = 4.48, S.D. = 0.54) "
    "และความเหมาะสมของเทคนิคและฟังก์ชันเฉลี่ย (x̄ = 4.56, S.D. = 0.50) ยืนยันว่าระบบสามารถช่วยลดเวลา ขจัดอคติ "
    "และเพิ่มประสิทธิภาพในการตัดสินใจลงทุนได้อย่างมีระบบ"
)
set_p_text(doc.paragraphs[10], thai_abstract, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P011: คำสำคัญ
p11 = doc.paragraphs[11]
p11.text = ""
r11_bold = p11.add_run("คำสำคัญ -- ")
set_run_font(r11_bold, "TH SarabunPSK", 14, bold=True)
r11_text = p11.add_run("สมาร์ทมันนี่คอนเซปต์, โครงสร้างตลาดการเงิน, อัลกอริทึมเชิงกฎเกณฑ์, กราฟเชิงโต้ตอบ, การวิเคราะห์หลายกรอบเวลา")
set_run_font(r11_text, "TH SarabunPSK", 14)
p11.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# P013: ABSTRACT heading
set_p_text(doc.paragraphs[13], "ABSTRACT", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P014: English Abstract text
eng_abstract = (
    "Retail traders in financial markets face high loss rates of 60–80%, largely driven by emotional bias and subjective manual charting. "
    "This paper presents the development of an automated web application for financial market structure analysis and visualization. "
    "The system implements a rule-based algorithm combined with look-back and look-forward techniques to objectively detect Swing High, "
    "Swing Low, Break of Structure (BOS), Change of Character (CHoCH), and Order Blocks. A Multi-Timeframe Scoring model across seven timeframes "
    "is integrated, and results are rendered on interactive candlestick charts utilizing the TradingView Lightweight Charts library. "
    "User satisfaction was evaluated across three dimensions: problem-solution fit, graphical user interface (GUI) design, and functional suitability. "
    "The evaluation results demonstrated a high level of satisfaction, with problem-solution fit (x̄ = 4.52, S.D. = 0.51), GUI design (x̄ = 4.48, S.D. = 0.54), "
    "and functional suitability (x̄ = 4.56, S.D. = 0.50), confirming that the system effectively eliminates emotional bias, saves time, "
    "and enhances systematic investment decisions."
)
set_p_text(doc.paragraphs[14], eng_abstract, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P015: Keywords
p15 = doc.paragraphs[15]
p15.text = ""
r15_bold = p15.add_run("Keywords -- ")
set_run_font(r15_bold, "TH SarabunPSK", 14, bold=True)
r15_text = p15.add_run("Smart Money Concepts, Market Structure, Rule-based Algorithm, Interactive Chart, Multi-Timeframe Analysis")
set_run_font(r15_text, "TH SarabunPSK", 14)
p15.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# P017: 1. บทนำ (Heading 1 -> Center, Bold 14pt)
set_p_text(doc.paragraphs[17], "1. บทนำ", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P018: Introduction body
intro_text = (
    "\tนักลงทุนรายย่อยในตลาดการเงินมีอัตราการขาดทุนเฉลี่ยสูงถึง 60–80% ตามรายงานของ ESMA และงานวิจัยที่เกี่ยวข้อง [1] "
    "สาเหตุสำคัญมาจากอคติทางอารมณ์ (Emotional Bias) และการขาดเครื่องมือวิเคราะห์โครงสร้างตลาดที่เป็นปรนัย แม้แนวคิด Smart Money Concepts (SMC) "
    "จะช่วยติดตามพฤติกรรมของสถาบันการเงินรายใหญ่ได้ แต่การตีเส้นกราฟด้วยสายตาเปล่ายังมีข้อจำกัดด้านความแปรผันตามมุมมองบุคคล ใช้เวลานาน "
    "และเกิดความผิดพลาดได้ง่าย โครงงานนี้จึงพัฒนาเครื่องมืออัตโนมัติด้วยภาษา Python โดยมีวัตถุประสงค์เพื่อ"
)
set_p_text(doc.paragraphs[18], intro_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P019, P020: 2 Objectives according to reviewer
obj1 = "\t1) ออกแบบเว็บแอปพลิเคชันสำหรับ Backtesting และแสดงกราฟแท่งเทียนเชิงโต้ตอบด้วยไลบรารี TradingView Lightweight Charts"
set_p_text(doc.paragraphs[19], obj1, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

obj2 = "\t2) พัฒนาเว็บแอปพลิเคชันสำหรับ Backtesting ด้วยอัลกอริทึมสแกนหาจุด Swing, BOS, CHoCH และ Order Block"
set_p_text(doc.paragraphs[20], obj2, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P021, P022: Clear previously 3rd objective
doc.paragraphs[21].text = ""
doc.paragraphs[22].text = ""

# P023: 2. ทฤษฎีและงานวิจัยที่เกี่ยวข้อง (Heading 1 -> Center, Bold 14pt)
set_p_text(doc.paragraphs[23], "2. ทฤษฎีและงานวิจัยที่เกี่ยวข้อง", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P024: 2.1 นิยามศัพท์เฉพาะ SMC (Heading 2 -> Left, Bold Italic 14pt)
set_p_text(doc.paragraphs[24], "2.1 นิยามศัพท์เฉพาะ SMC", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P025: Intro to table 1
set_p_text(doc.paragraphs[25], "\tงานวิจัยกำหนดนิยามโครงสร้างราคาทางคณิตศาสตร์ไว้ในตาราง 1", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P026: Caption ตาราง 1 (Caption -> 12pt above table)
set_p_text(doc.paragraphs[26], "ตาราง 1 นิยามศัพท์เฉพาะตามหลักการ SMC", size_pt=12, align=WD_ALIGN_PARAGRAPH.LEFT)

# P028: 2.2 งานวิจัยที่เกี่ยวข้อง (Heading 2 -> Left, Bold Italic 14pt)
set_p_text(doc.paragraphs[28], "2.2 งานวิจัยที่เกี่ยวข้อง", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P029: Related work - Clean in-text citations, no excessive [2]
related_work_text = (
    "\tLo และคณะ [2] ได้ศึกษาการใช้อัลกอริทึมเชิงคำนวณและการอนุมานทางสถิติเพื่อตรวจจับรูปแบบราคาทางเทคนิค "
    "ซึ่งแสดงให้เห็นว่าการแปลงรูปแบบกราฟเป็นกฎเกณฑ์เชิงประจักษ์ช่วยลดความผันแปรเชิงอัตวิสัยได้อย่างมีนัยสำคัญ "
    "สอดคล้องกับ Babu และ Reddy [3] ที่ประยุกต์ใช้ภาษา Python ในการสแกนและวิเคราะห์โครงสร้างตลาดหุ้นแบบอัตโนมัติ "
    "ขณะที่ Cont และคณะ [4] ได้วิเคราะห์ผลกระทบของเหตุการณ์ใน Order Book ต่อพลวัตของราคา ซึ่งเป็นรากฐานทางทฤษฎีที่สนับสนุนการตรวจจับ Order Block ใน SMC "
    "และในส่วนของการแสดงผล การใช้ไลบรารี TradingView Lightweight Charts [5] ช่วยให้การเรนเดอร์ข้อมูลราคาแบบแท่งเทียนเชิงโต้ตอบบนเว็บแอปพลิเคชัน"
    "มีประสิทธิภาพสูงและรองรับข้อมูลความละเอียดสูงได้เป็นอย่างดี"
)
set_p_text(doc.paragraphs[29], related_work_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P030: 3. การออกแบบและสถาปัตยกรรมระบบ (Heading 1 -> Center, Bold 14pt)
set_p_text(doc.paragraphs[30], "3. การออกแบบและสถาปัตยกรรมระบบ", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P031: 3.1 สถาปัตยกรรมระบบ (Heading 2 -> Left, Bold Italic 14pt)
set_p_text(doc.paragraphs[31], "3.1 สถาปัตยกรรมระบบ", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P032: Intro architecture
set_p_text(doc.paragraphs[32], "\tระบบประกอบด้วย 3 ส่วนการทำงานหลัก ได้แก่", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
set_p_text(doc.paragraphs[33], "\t1) ส่วนรับข้อมูล (Input): รับค่าคู่เงินและกรอบเวลาจากผู้ใช้", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
set_p_text(doc.paragraphs[34], "\t2) ส่วนประมวลผล (Process): ดึงข้อมูล OHLCV ผ่าน API ประมวลผลจุด Swing, BOS, CHoCH และ Order Block ด้วยอัลกอริทึมหลัก พร้อมทั้งส่งต่อไปยัง Multi-Timeframe Engine และ Scoring System", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
set_p_text(doc.paragraphs[35], "\t3) ส่วนแสดงผล (Output): ส่งออกกราฟแท่งเทียนพล็อตเส้นโครงสร้างและกระดานสรุปผล", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P037: Caption ภาพ 1 (Caption -> 12pt under figure)
set_p_text(doc.paragraphs[37], "ภาพ 1 แผนภาพการทำงานของระบบวิเคราะห์ SMC", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)

# P038: 3.2 ตัวแบบทางคณิตศาสตร์สำหรับการตรวจจับจุดสวิง (Swing Detection) (Heading 2 -> Left, Bold Italic 14pt)
set_p_text(doc.paragraphs[38], "3.2 ตัวแบบทางคณิตศาสตร์สำหรับการตรวจจับจุดสวิง (Swing Detection)", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P039: Math description - remove improper [2], [1]
p39_text = (
    "\tระบบตรวจจับจุด Swing High (SH) และ Swing Low (SL) ด้วยการกำหนดหน้าต่างการตรวจสอบ N แท่งเทียนย้อนหลัง (Look-back) "
    "และล่วงหน้า (Look-forward) โดยที่ราคาของแท่งเทียนที่เวลา t จะถูกจำแนกเป็นจุดสวิงตามเงื่อนไขสมการ (1) และ (2):"
)
set_p_text(doc.paragraphs[39], p39_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P045: 3.3 กฎเกณฑ์เชิงตรรกะสำหรับ BOS และ CHoCH (Heading 2 -> Left, Bold Italic 14pt)
set_p_text(doc.paragraphs[45], "3.3 กฎเกณฑ์เชิงตรรกะสำหรับ BOS และ CHoCH", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P046:
set_p_text(doc.paragraphs[46], "\tเมื่อระบุตำแหน่งจุดสวิงได้แล้ว อัลกอริทึมจะประเมินการเบรกโครงสร้างราคาดังนี้", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P047: BOS description - clean [2]
bos_desc = (
    "\t- Break of Structure (BOS): ในแนวโน้มขาขึ้น สัญญาณ Bullish BOS จะเกิดขึ้นเมื่อราคาปิดของแท่งเทียนปัจจุบัน (Close_t) "
    "เคลื่อนที่ทะลุระดับราคาสูงสุดของ Swing High ล่าสุด (SH_prev) หรือ Close_t > SH_prev ในทางตรงกันข้าม สัญญาณ Bearish BOS จะเกิดขึ้นเมื่อ Close_t < SL_prev"
)
set_p_text(doc.paragraphs[47], bos_desc, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P048: CHoCH description - clean [2]
choch_desc = (
    "\t- Change of Character (CHoCH): เกิดขึ้นเมื่อราคาปิดเคลื่อนที่ทะลุจุดสวิงที่มีนัยสำคัญในทิศทางตรงกันข้ามกับแนวโน้มหลักก่อนหน้า "
    "เช่น การที่ราคาหลุดต่ำกว่า Swing Low สำคัญล่าสุดในโครงสร้างขาขึ้น บ่งชี้ถึงการเสียรูปทรงราคาและการกลับทิศทางของแนวโน้ม"
)
set_p_text(doc.paragraphs[48], choch_desc, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P049: Order Block - clean [2]
ob_desc = (
    "\t- Order Block Identification: เมื่อเกิดสัญญาณ BOS หรือ CHoCH อัลกอริทึมจะย้อนกลับไปค้นหาแท่งเทียนขั้วตรงข้ามสุดท้ายก่อนการเกิดแรงผลักดันนั้น "
    "(เช่น แท่งเทียนขาลงสุดท้ายก่อนเกิด Bullish BOS) และบันทึกช่วงราคาต่ำสุด-สูงสุดของแท่งเทียนดังกล่าวเพื่อกำหนดเป็นโซน Order Block อัตโนมัติ"
)
set_p_text(doc.paragraphs[49], ob_desc, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P050: 3.4 ตัวแบบการถ่วงน้ำหนักพหุกรอบเวลา (Multi-Timeframe Scoring Model)
set_p_text(doc.paragraphs[50], "3.4 ตัวแบบการถ่วงน้ำหนักพหุกรอบเวลา (Multi-Timeframe Scoring Model)", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P051:
set_p_text(doc.paragraphs[51], "\tเพื่อบูรณาการข้อมูลแนวโน้มครอบคลุม 7 กรอบเวลา (ตั้งแต่ Weekly จนถึง 5-Minute) ระบบได้พัฒนา Scoring System โดยคำนวณคะแนนทิศทางสุทธิ (S_total) ดังสมการ (3):", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P054:
set_p_text(doc.paragraphs[54], "\tโดยที่ wk คือค่าน้ำหนักความสำคัญของกรอบเวลาที่ k ซึ่งสอดคล้องกับข้อกำหนดผลรวมค่าน้ำหนักเท่ากับ 1.0 และ Dk มีค่าอยู่ในช่วง {-1, 0, 1} แทนสถานะแนวโน้มของกรอบเวลานั้น (-1: แนวโน้มขาลง, 0: ไร้ทิศทาง, 1: แนวโน้มขาขึ้น) ดังแสดงการกำหนดค่าน้ำหนักในตาราง 2", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P055: Caption ตาราง 2
set_p_text(doc.paragraphs[55], "ตาราง 2 การกำหนดค่าน้ำหนักความสำคัญของทั้ง 7 กรอบเวลาใน Scoring System", size_pt=12, align=WD_ALIGN_PARAGRAPH.LEFT)

# P057: 3.5 รหัสเทียม -> เปลี่ยนเป็นขั้นตอนการทำงานของอัลกอริทึมหลัก (Comment 5)
set_p_text(doc.paragraphs[57], "3.5 ขั้นตอนการทำงานของอัลกอริทึมหลัก", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)
set_p_text(doc.paragraphs[58], "\tขั้นตอนการทำงานของอัลกอริทึมในการตรวจจับโครงสร้างราคา SMC มีลำดับขั้นตอนดังนี้:", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P059 - P063: Replaced algorithm pseudocode with descriptive step-by-step paragraphs
step1 = "\tขั้นตอนที่ 1 (การรับข้อมูลนำเข้า): รับชุดข้อมูลแท่งเทียนราคา OHLCV ย้อนหลัง และกำหนดขนาดหน้าต่างการตรวจสอบ N แท่งเทียน"
set_p_text(doc.paragraphs[59], step1, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

step2 = "\tขั้นตอนที่ 2 (การตรวจจับจุดสวิง): วนลูปตรวจสอบแท่งเทียน หากราคาจุดสูงสุดของแท่งเทียนมีค่ามากกว่าจุดสูงสุดของแท่งเทียนโดยรอบ N แท่ง จะถูกระบุเป็น Swing High และหากราคาต่ำสุดมีค่าน้อยกว่าแท่งเทียนโดยรอบ N แท่ง จะถูกระบุเป็น Swing Low"
set_p_text(doc.paragraphs[60], step2, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

step3 = "\tขั้นตอนที่ 3 (การประเมินการเบรกโครงสร้างราคา): ตรวจสอบราคาปิดของแท่งเทียนเปรียบเทียบกับจุดสวิงล่าสุด หากราคาปิดทะลุ Swing High ในแนวโน้มเดิมจะระบุเป็น Bullish BOS แต่หากทะลุในแนวโน้มตรงข้ามจะระบุเป็น Bullish CHoCH พร้อมปรับสถานะแนวโน้ม ในทางกลับกัน หากราคาปิดหลุดต่ำกว่า Swing Low จะระบุเป็น Bearish BOS หรือ Bearish CHoCH ตามลำดับ"
set_p_text(doc.paragraphs[61], step3, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

step4 = "\tขั้นตอนที่ 4 (การระบุโซน Order Block): เมื่อเกิดสัญญาณ BOS หรือ CHoCH อัลกอริทึมจะทำการค้นหาย้อนกลับไปยังแท่งเทียนขั้วตรงข้ามแท่งสุดท้ายก่อนเกิดแรงผลักดัน และบันทึกช่วงราคาเปิด-ปิดเป็นกรอบ Order Block พร้อมตรวจสอบสถานะการทดสอบโซน (Mitigation)"
set_p_text(doc.paragraphs[63], step4, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

step5 = "\tขั้นตอนที่ 5 (การส่งออกผลลัพธ์): ส่งออกพิกัดจุดสวิง เส้นโครงสร้าง และพิกัดกล่องราคาเพื่อนำไปแสดงผลบนกราฟเชิงโต้ตอบ"
set_p_text(doc.paragraphs[64], step5, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# Clear unused old pseudocode paragraphs P065 to P079
for idx in range(65, 80):
    doc.paragraphs[idx].text = ""

# P080: 4. การพัฒนาและการแสดงผลของระบบ (Heading 1 -> Center, Bold 14pt)
set_p_text(doc.paragraphs[80], "4. การพัฒนาและการแสดงผลของระบบ", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P081: 4.1 สถาปัตยกรรมซอฟต์แวร์และเครื่องมือที่ใช้พัฒนา (Heading 2 -> Left, Bold Italic 14pt)
set_p_text(doc.paragraphs[81], "4.1 สถาปัตยกรรมซอฟต์แวร์และเครื่องมือที่ใช้พัฒนา", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P082: Software architecture - Clean [2] (Comment 7)
arch_desc = (
    "\tระบบถูกพัฒนาขึ้นโดยใช้ภาษา Python ในการประมวลผลข้อมูลแกนหลัก โดยใช้ไลบรารี Pandas และ NumPy สำหรับการคำนวณโครงสร้างข้อมูลอนุกรมเวลาทางการเงิน "
    "และใช้ FastAPI ในการให้บริการ REST API เชื่อมต่อกับโปรแกรม MetaTrader 5 เพื่อดึงข้อมูลราคา OHLCV แบบเรียลไทม์ ในส่วนติดต่อผู้ใช้ (Frontend) "
    "พัฒนาด้วยเทคโนโลยีเว็บร่วมกับไลบรารี TradingView Lightweight Charts เพื่อเรนเดอร์กราฟิกราคาเชิงโต้ตอบ และใช้ HTML5 Canvas ซ้อนทับในการวาดเส้นโครงสร้างราคา SMC "
    "ได้อย่างรวดเร็วบนเว็บเบราว์เซอร์"
)
set_p_text(doc.paragraphs[82], arch_desc, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P083: 4.2 ฟังก์ชันการทำงานหลักของระบบ
set_p_text(doc.paragraphs[83], "4.2 ฟังก์ชันการทำงานหลักของระบบ", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)
set_p_text(doc.paragraphs[84], "\tระบบประกอบด้วย 4 ฟังก์ชันหลักที่ช่วยสนับสนุนการวิเคราะห์ ได้แก่", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
set_p_text(doc.paragraphs[85], "\t1) Interactive Charting: กราฟแท่งเทียนเชิงโต้ตอบที่สามารถซูม เลื่อนดูประวัติราคา และเลือกเปลี่ยนคู่เงินหรือกรอบเวลาได้ตามต้องการ", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
set_p_text(doc.paragraphs[86], "\t2) Automated Structure Overlay: การวาดเส้นเชื่อมจุด Swing High/Low พร้อมข้อความกำกับตำแหน่ง BOS และ CHoCH ลงบนกราฟแบบอัตโนมัติ", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
set_p_text(doc.paragraphs[87], "\t3) Price Zone Highlighting: การแสดงแถบสีโปร่งใสระบุพื้นที่ Order Blocks, FVG และระดับ Equal High/Low", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
set_p_text(doc.paragraphs[88], "\t4) Multi-Timeframe Status Dashboard: กระดานสรุปผลลัพธ์คะแนนสุทธิและทิศทางตลาดทั้ง 7 กรอบเวลา ช่วยให้นักเทรดประเมินสภาวะตลาดได้ในหน้าจอเดียว", size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P091: Caption ภาพ 2
set_p_text(doc.paragraphs[91], "ภาพ 2 ส่วนแสดงผลกราฟแท่งเทียนเชิงโต้ตอบพร้อมเส้นโครงสร้าง SMC และ Order Block", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)

# P093: Caption ภาพ 3
set_p_text(doc.paragraphs[93], "ภาพ 3 ส่วนแสดงผลกระดานข้อมูลสรุปสถานะตลาดและการถ่วงน้ำหนักแนวโน้ม 7 กรอบเวลา", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)

# P094: 5. การวิเคราะห์กรณีศึกษาและการอภิปรายผล (Heading 1 -> Center, Bold 14pt)
set_p_text(doc.paragraphs[94], "5. การวิเคราะห์กรณีศึกษาและการอภิปรายผล", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P095: 5.1 กรณีศึกษาที่ 1 การตรวจจับแนวโน้มต่อเนื่อง (Trend Continuation & BOS)
set_p_text(doc.paragraphs[95], "5.1 กรณีศึกษาที่ 1 การตรวจจับแนวโน้มต่อเนื่อง (Trend Continuation & BOS)", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P096: Clean [2]
case1_text = (
    "\tในการทดสอบอัลกอริทึมกับสภาวะตลาดที่มีแนวโน้มขาขึ้นอย่างต่อเนื่อง ระบบทำการตรวจสอบจุด Swing High ล่าสุด เมื่อราคาปิดของแท่งเทียนถัดไป"
    "สามารถยืนเหนือระดับราคาดังกล่าวได้ อัลกอริทึมจะวาดเส้นระบุเป็น Bullish BOS ทันที พร้อมทั้งคำนวณหาโซน Order Block ที่เป็นฐานส่งราคา "
    "การทดสอบแสดงให้เห็นว่าระบบสามารถระบุการดำเนินต่อไปของแนวโน้มได้อย่างเป็นปรนัยโดยไม่มีความผันแปรตามมุมมองของผู้ประเมิน"
)
set_p_text(doc.paragraphs[96], case1_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P097: 5.2 กรณีศึกษาที่ 2 การตรวจจับการกลับตัวของแนวโน้ม (Trend Reversal & CHoCH)
set_p_text(doc.paragraphs[97], "5.2 กรณีศึกษาที่ 2 การตรวจจับการกลับตัวของแนวโน้ม (Trend Reversal & CHoCH)", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P098: Clean [2]
case2_text = (
    "\tในกรณีที่โครงสร้างตลาดเริ่มสูญเสียแรงผลักดันและราคาปิดหลุดต่ำกว่า Swing Low ก่อนหน้า อัลกอริทึมจะเปลี่ยนสถานะการประเมินจากแนวโน้มขาขึ้น"
    "และสร้างสัญญาณ Bearish CHoCH บนกราฟโดยอัตโนมัติ ซึ่งช่วยแจ้งเตือนการเปลี่ยนโครงสร้างราคาได้เร็วกว่าการรอตัดเส้นค่าเฉลี่ยแบบดั้งเดิม "
    "และช่วยขจัดอคติทางอารมณ์ที่มักคาดหวังให้ราคาปรับตัวขึ้นต่อ"
)
set_p_text(doc.paragraphs[98], case2_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P099: 5.3 กรณีศึกษาที่ 3 การแก้ไขความขัดแย้งของสัญญาณหลายกรอบเวลา
set_p_text(doc.paragraphs[99], "5.3 กรณีศึกษาที่ 3 การแก้ไขความขัดแย้งของสัญญาณหลายกรอบเวลา", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P100: Clean [2]
case3_text = (
    "\tในสภาวะที่กรอบเวลาสั้น (เช่น 5-Minute และ 15-Minute) แสดงการเกิด Bearish CHoCH แต่กรอบเวลาหลัก (Weekly และ Daily) ยังคงเป็นแนวโน้มขาขึ้นที่แข็งแกร่ง "
    "ระบบ Scoring System จะคำนวณคะแนนถ่วงน้ำหนักโดยให้ความสำคัญกับกรอบเวลาขนาดใหญ่ ส่งผลให้คะแนนรวม S_total ยังคงมีค่าเป็นบวก ระบบจึงแจ้งเตือนว่าการปรับตัวลงในกรอบเวลาสั้น"
    "เป็นเพียงการพักตัว (Pullback) ภายในโครงสร้างใหญ่ ซึ่งช่วยป้องกันไม่ให้นักลงทุนเปิดสถานะเทรดสวนทางกับแนวโน้มหลักของตลาด"
)
set_p_text(doc.paragraphs[100], case3_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P101: 5.4 การอภิปรายผลและข้อจำกัดของระบบ
set_p_text(doc.paragraphs[101], "5.4 การอภิปรายผลและข้อจำกัดของระบบ", size_pt=14, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT)

# P102: Clean [2]
case4_text = (
    "\tการนำ Rule-based Algorithm มาประยุกต์ใช้ช่วยแก้ปัญหาความไม่เป็นปรนัยได้อย่างสมบูรณ์และสามารถทำซ้ำได้ตามเกณฑ์ความสำเร็จของโครงงาน "
    "อย่างไรก็ดี ระบบมีข้อจำกัดด้านความล่าช้าเชิงเวลา (Time Lag) ในการยืนยันจุดสวิง เนื่องจากเทคนิค Look-forward จำเป็นต้องรอให้แท่งเทียนปิดตัวครบ N แท่งก่อน "
    "จึงจะยืนยันจุดสวิงได้อย่างสมบูรณ์ ซึ่งถือเป็นข้อแลกเปลี่ยน (Trade-off) ที่จำเป็นเพื่อให้ได้ข้อมูลโครงสร้างที่แม่นยำและปราศจากสัญญาณหลอก"
)
set_p_text(doc.paragraphs[102], case4_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P103: 6. สรุปผลและประโยชน์ที่ได้รับ (Heading 1 -> Center, Bold 14pt)
set_p_text(doc.paragraphs[103], "6. สรุปผลและประโยชน์ที่ได้รับ", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P104: Clean * and : and [2] (Comment 9)
conclusion_text = (
    "\tงานวิจัยนี้ได้พัฒนาเครื่องมืออัตโนมัติด้วยภาษา Python สำหรับการวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินตามแนวคิด Smart Money Concepts "
    "ได้สำเร็จตามวัตถุประสงค์ โดยรวมศูนย์การคำนวณอัลกอริทึมเชิงกฎเกณฑ์ การวิเคราะห์พหุกรอบเวลาแบบถ่วงน้ำหนัก และการแสดงผลบนกราฟเชิงโต้ตอบไว้ด้วยกันอย่างเป็นระบบ "
    "ซึ่งก่อให้เกิดประโยชน์สำคัญ 3 ประการ ได้แก่ 1) ช่วยประหยัดเวลาและลดข้อผิดพลาด โดยเป็นเครื่องมือสแกนและตรวจสอบโครงสร้างราคาแบบอัตโนมัติที่ให้ผลลัพธ์เป็นปรนัย "
    "ขจัดความผิดพลาดจากการตีเส้นกราฟด้วยตนเอง 2) เพิ่มประสิทธิภาพการตัดสินใจลงทุน โดยมีระบบกระดานข้อมูลสรุปแนวโน้ม 7 กรอบเวลา ช่วยป้องกันการเปิดสถานะสวนทางแนวโน้มหลัก "
    "และลดอคติทางอารมณ์ของนักลงทุน 3) เป็นสื่อการเรียนรู้เชิงประจักษ์ ช่วยให้ผู้ศึกษากลยุทธ์ SMC สามารถทำความเข้าใจกฎเกณฑ์ของโครงสร้างตลาดผ่านระเบียบวิธีทางคณิตศาสตร์ที่โปร่งใสและตรวจสอบได้"
)
set_p_text(doc.paragraphs[104], conclusion_text, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# P105: เอกสารอ้างอิง (Heading -> Center, Bold 14pt, no number)
set_p_text(doc.paragraphs[105], "เอกสารอ้างอิง", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# P106-P110: IEEE references (Comment 10)
ref1 = "[1] European Securities and Markets Authority (ESMA), “Retail Trading in Derivatives and CFDs,” Financial Stability Report, Paris: ESMA, Technical Report, 2019."
set_p_text(doc.paragraphs[106], ref1, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

ref2 = "[2] A. W. Lo, H. Mamaysky, and J. Wang, “Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation,” The Journal of Finance, vol. 55, no. 4, pp. 1705-1765, Aug. 2000."
set_p_text(doc.paragraphs[107], ref2, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

ref3 = "[3] A. S. Babu and B. K. Reddy, “Automating Stock Market Structure Analysis using Python,” International Research Journal of Engineering and Technology, vol. 7, no. 10, pp. 64-68, Oct. 2020."
set_p_text(doc.paragraphs[108], ref3, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

ref4 = "[4] R. Cont, A. Kukanov, and S. Stoikov, “The Price Impact of Order Book Events,” Journal of Financial Econometrics, vol. 12, no. 1, pp. 47-88, Jan. 2014."
set_p_text(doc.paragraphs[109], ref4, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

ref5 = "[5] TradingView, “Lightweight Charts Documentation,” TradingView Inc., 2024. [Online]. Available: https://tradingview.github.io/lightweight-charts/"
set_p_text(doc.paragraphs[110], ref5, size_pt=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# Ensure all remaining paragraphs have TH SarabunPSK
for p in doc.paragraphs:
    for r in p.runs:
        set_run_font(r, "TH SarabunPSK")

# Format tables font
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, "TH SarabunPSK", 12)

# Save document to both destinations
doc.save(dst_path)
doc.save(workspace_dst)
print("Successfully saved revised docx to:")
print("1.", dst_path)
print("2.", workspace_dst)
