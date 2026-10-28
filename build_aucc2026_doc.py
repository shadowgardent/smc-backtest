# -*- coding: utf-8 -*-
import sys
import os
import re
import copy
import shutil
import zipfile
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.stdout.reconfigure(encoding='utf-8')

BACKUP_DOCX = r'e:\Project\smc-backtest-backend\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx'
WORK_DOCX = r'e:\Project\smc-backtest-backend\SMC_AUCC2026_Final.docx'
NEW_FIG1 = r'e:\Project\smc-backtest-backend\new_figure_1.png'

doc = docx.Document(BACKUP_DOCX)

def set_run_font(run, size_pt=14, bold=False, italic=False, superscript=False, subscript=False):
    run.font.name = 'TH SarabunPSK'
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.superscript = superscript
    run.font.subscript = subscript
    run.font.color.rgb = RGBColor(0, 0, 0)
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), 'TH SarabunPSK')
    rFonts.set(qn('w:hAnsi'), 'TH SarabunPSK')
    rFonts.set(qn('w:cs'), 'TH SarabunPSK')
    rFonts.set(qn('w:eastAsia'), 'TH SarabunPSK')
    sz_val = str(int(size_pt * 2))
    for tag in ['w:sz', 'w:szCs']:
        el = rPr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            rPr.append(el)
        el.set(qn('w:val'), sz_val)

def clear_paragraph_runs(p):
    for child in list(p._p):
        if child.tag != qn('w:pPr'):
            p._p.remove(child)

def set_paragraph_runs(p, runs_spec, align=None, first_line_indent=None, left_indent=None, space_before=None, space_after=None, keep_with_next=None):
    clear_paragraph_runs(p)
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    if first_line_indent is not None:
        pf.first_line_indent = first_line_indent
    if left_indent is not None:
        pf.left_indent = left_indent
    if space_before is not None:
        pf.space_before = space_before
    if space_after is not None:
        pf.space_after = space_after
    if keep_with_next is not None:
        pf.keep_with_next = keep_with_next

    for spec in runs_spec:
        text = spec[0]
        bold = spec[1] if len(spec) > 1 else False
        italic = spec[2] if len(spec) > 2 else False
        size_pt = spec[3] if len(spec) > 3 else 14
        sup = spec[4] if len(spec) > 4 else False
        sub = spec[5] if len(spec) > 5 else False
        r = p.add_run(text)
        set_run_font(r, size_pt=size_pt, bold=bold, italic=italic, superscript=sup, subscript=sub)

# ---------------------------------------------------------
# 1. HEADER: The 14th Asia Undergraduate Conference on Computing (AUCC) 2026
# ---------------------------------------------------------
for sec in doc.sections:
    hp = sec.header.paragraphs[0]
    set_paragraph_runs(
        hp,
        [
            ('The 14', True, False, 14, False),
            ('th', True, False, 14, True),
            (' Asia Undergraduate Conference on Computing (AUCC) 2026', True, False, 14, False),
        ],
        align=WD_ALIGN_PARAGRAPH.CENTER
    )

# ---------------------------------------------------------
# 2. TITLE & AUTHOR BLOCK (Section 0: P00 - P08)
# ---------------------------------------------------------
set_paragraph_runs(
    doc.paragraphs[0],
    [('เครื่องมือ\u200bวิเคราะห์\u200bและ\u200bแสดงผล\u200bโครงสร้าง\u200bตลาด\u200bการเงิน\u200bด้วย\u200bอัลกอริทึม Smart Money Concepts (SMC)', True, False, 18)],
    align=WD_ALIGN_PARAGRAPH.CENTER
)
set_paragraph_runs(
    doc.paragraphs[1],
    [('Financial Market Structure Analysis and Visualization Tool Using Smart Money Concepts (SMC) Algorithms', True, False, 16)],
    align=WD_ALIGN_PARAGRAPH.CENTER,
    space_after=Pt(6)
)
# P03: Author Name ONLY (no "จัดทำโดย", no "นาย", no student ID)
set_paragraph_runs(
    doc.paragraphs[3],
    [('นวพรหม ภูผาผิว', True, False, 14)],
    align=WD_ALIGN_PARAGRAPH.CENTER
)
# Remove P02 ("จัดทำโดย") and extra blank lines P05, P06, P07 in reverse order (keeping P04 blank and P08 sectPr intact)
for idx in [7, 6, 5, 2]:
    p_el = doc.paragraphs[idx]._p
    p_el.getparent().remove(p_el)

def find_p_by_prefix(prefix):
    clean_pre = prefix.replace('\u200b', '')
    for i, p in enumerate(doc.paragraphs):
        if p.text.replace('\u200b', '').strip().startswith(clean_pre):
            return i, p
    raise ValueError(f"Paragraph starting with {prefix!r} not found")

# ---------------------------------------------------------
# 3. ABSTRACT & KEYWORDS (Thai & English)
# ---------------------------------------------------------
_, p_th_abs_hdr = find_p_by_prefix('บทคัดย่อ')
set_paragraph_runs(p_th_abs_hdr, [('บทคัดย่อ', True, False, 14)], align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Inches(0))

_, p_th_abs = find_p_by_prefix('นักลงทุน')
th_abs_text = (
    'นักลงทุน\u200bรายย่อย\u200bที่\u200bไม่มี\u200bความรู้\u200bเพียงพอ\u200bใน\u200bการลงทุน\u200bใน\u200bตลาด\u200bการเงิน\u200bมี\u200bอัตรา\u200bการขาดทุน\u200bสูง\u200bถึง 60\u200b–80% [1] '
    'ซึ่ง\u200bมี\u200bสาเหตุ\u200bสำคัญ\u200bมาจาก\u200bอคติ\u200bทาง\u200bอารมณ์ และ\u200bความคลาดเคลื่อน\u200bจาก\u200bการ\u200bตีความ\u200bโครงสร้าง\u200bกราฟ\u200bด้วย\u200bสายตา\u200bที่\u200bแตกต่าง\u200bกัน\u200bใน\u200bแต่ละ\u200bบุคคล '
    'บทความ\u200bนี้\u200bนำเสนอ\u200bการพัฒนา\u200bเว็บ\u200bแอปพลิเคชัน\u200bเพื่อ\u200bวิเคราะห์\u200bและ\u200bแสดงผล\u200bโครงสร้าง\u200bตลาด\u200bการเงิน\u200bแบบ\u200bอัตโนมัติ '
    'โดย\u200bประยุกต์ใช้\u200bอัลกอริทึม\u200bเชิง\u200bกฎเกณฑ์ (Rule-based Algorithm) ร่วมกับ\u200bเทคนิค Look-back และ Look-forward '
    'ใน\u200bการตรวจจับ\u200bจุด Swing High, Swing Low, การ\u200bเบรก\u200bโครงสร้าง\u200bราคา (BOS), การ\u200bเปลี่ยน\u200bแนวโน้ม (CHoCH) และ Order Block '
    'พร้อม\u200bกลไก\u200bวิเคราะห์ 7 กรอบ\u200bเวลา\u200bแบบ\u200bถ่วง\u200bน้ำหนัก (Multi-Timeframe Scoring) และ\u200bแสดงผล\u200bผ่าน\u200bกราฟ\u200bแท่ง\u200bเทียน\u200bเชิง\u200bโต้ตอบ\u200bด้วย\u200bไลบรารี TradingView Lightweight Charts '
    'ใน\u200bการประเมินผล ได้\u200bทดสอบ\u200bการใช้งาน\u200bกับ\u200bผู้ใช้งาน\u200bจริง\u200bจำนวน 5 คน โดย\u200bประเมิน\u200bความพึงพอใจ 3 ด้าน ได้แก่ '
    'ความเหมาะสม\u200bของ\u200bการพัฒนา\u200bโปรแกรม\u200bต่อ\u200bการแก้ปัญหา การ\u200bออกแบบ\u200bส่วน\u200bติดต่อ\u200bผู้ใช้ (GUI) และ\u200bความเหมาะสม\u200bของ\u200bเทคนิค\u200bและ\u200bฟังก์ชัน\u200bที่\u200bใช้ '
    'ผล\u200bการประเมิน\u200bพบ\u200bว่า ผู้ใช้งาน\u200bมี\u200bความพึงพอใจ\u200bโดยรวม\u200bอยู่\u200bใน\u200bระดับ\u200bดีมาก โดย\u200bมี\u200bค่าเฉลี่ย\u200bรวม\u200bเท่ากับ 4.52 จาก 5 '
    'ยืนยัน\u200bว่า\u200bระบบ\u200bสามารถ\u200bช่วย\u200bลด\u200bเวลา ขจัด\u200bอคติ และ\u200bเพิ่มประสิทธิภาพ\u200bใน\u200bการตัดสินใจ\u200bลงทุน\u200bได้\u200bอย่าง\u200bเป็นระบบ'
)
set_paragraph_runs(
    p_th_abs,
    [(th_abs_text, False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY,
    first_line_indent=Inches(0.25)
)

_, p_th_kw = find_p_by_prefix('คำสำคัญ')
set_paragraph_runs(
    p_th_kw,
    [
        ('คำสำคัญ', True, True, 14),
        (' – สมาร์ท\u200bมัน\u200bนี่\u200bคอนเซปต์, การ\u200bวิเคราะห์\u200bทางการเงิน, การ\u200bแสดงผล\u200bข้อมูล\u200bด้วย\u200bภาพ', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0)
)

_, p_en_abs_hdr = find_p_by_prefix('ABSTRACT')
set_paragraph_runs(p_en_abs_hdr, [('ABSTRACT', True, False, 14)], align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Inches(0))

_, p_en_abs = find_p_by_prefix('Retail traders')
en_abs_text = (
    'Retail investors lacking sufficient investment knowledge in financial markets face high loss rates of 60–80% [1], '
    'largely driven by emotional bias and inconsistent visual interpretation of price charts across individuals. This paper presents the development of an automated '
    'web application for financial market structure analysis and visualization. The system implements a rule-based algorithm '
    'combined with look-back and look-forward techniques to systematically detect Swing High, Swing Low, Break of Structure (BOS), '
    'Change of Character (CHoCH), and Order Blocks. A Multi-Timeframe Scoring model across seven timeframes is integrated, '
    'and results are rendered on interactive candlestick charts utilizing the TradingView Lightweight Charts library. '
    'System evaluation was conducted with five real users across three dimensions: problem-solution fit, graphical user interface (GUI) design, '
    'and functional suitability. The evaluation results demonstrated a very high level of overall user satisfaction with an overall average score of 4.52 out of 5, '
    'confirming that the system effectively eliminates emotional bias, saves time, and enhances systematic investment decisions.'
)
set_paragraph_runs(
    p_en_abs,
    [(en_abs_text, False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    first_line_indent=Inches(0.25)
)

_, p_en_kw = find_p_by_prefix('Keywords')
set_paragraph_runs(
    p_en_kw,
    [
        ('Keywords', True, True, 14),
        (' -- Smart Money Concepts (SMC), Financial Analysis, Visualization', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0)
)

# ---------------------------------------------------------
# 4. SECTION 1: INTRODUCTION (1. บทนำ)
# ---------------------------------------------------------
idx_s1, p_s1 = find_p_by_prefix('1. บทนำ')
p_intro = doc.paragraphs[idx_s1 + 1]
intro_text = (
    '\tนักลงทุน\u200bรายย่อย\u200bที่\u200bไม่มี\u200bความรู้\u200bเพียงพอ\u200bใน\u200bการลงทุน\u200bใน\u200bตลาด\u200bการเงิน\u200bมี\u200bอัตรา\u200bการขาดทุน\u200bเฉลี่ย\u200bสูง\u200bถึง 60\u200b–80% '
    'ตาม\u200bรายงาน\u200bของ ESMA และ\u200bงานวิจัย\u200bที่\u200bเกี่ยวข้อง [1] สาเหตุ\u200bสำคัญ\u200bมาจาก\u200bอคติ\u200bทาง\u200bอารมณ์ (Emotional Bias) '
    'และ\u200bการ\u200bขาด\u200bเครื่องมือ\u200bวิเคราะห์\u200bโครงสร้าง\u200bตลาด\u200bที่\u200bมี\u200bเกณฑ์\u200bมาตรฐาน\u200bชัดเจน แม้\u200bแนวคิด Smart Money Concepts (SMC) '
    'จะ\u200bช่วย\u200bติดตาม\u200bพฤติกรรม\u200bของ\u200bสถาบันการเงิน\u200bรายใหญ่\u200bได้ แต่\u200bการ\u200bตีเส้น\u200bกราฟ\u200bด้วย\u200bสาย\u200bตาเปล่า\u200bยังมี\u200bข้อจำกัด\u200bด้าน\u200bความคลาดเคลื่อน\u200bตาม\u200bมุมมอง\u200bของ\u200bแต่ละ\u200bบุคคล '
    'ใช้เวลานาน และ\u200bเกิด\u200bความผิดพลาด\u200bได้\u200bง่าย โครงงาน\u200bนี้\u200bจึง\u200bพัฒนา\u200bเครื่องมือ\u200bอัตโนมัติ\u200bด้วย\u200bภาษา Python โดย\u200bมี\u200bวัตถุประสงค์\u200bเพื่อ'
)
set_paragraph_runs(p_intro, [(intro_text, False, False, 14)], align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY)

p_obj1 = doc.paragraphs[idx_s1 + 2]
set_paragraph_runs(
    p_obj1,
    [('\t1) พัฒนา\u200bอัลกอริทึม\u200bเชิง\u200bกฎเกณฑ์\u200bสำหรับ\u200bการ\u200bระบุ\u200bโครงสร้าง\u200bราคา\u200bตาม\u200bหลักการ SMC อย่าง\u200bมี\u200bมาตรฐาน\u200bเดียวกัน', False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)
p_obj2 = doc.paragraphs[idx_s1 + 3]
set_paragraph_runs(
    p_obj2,
    [('\t2) พัฒนา\u200bเว็บ\u200bแอปพลิเคชัน\u200bที่\u200bแสดงผล\u200bโครงสร้าง\u200bราคา\u200bและ\u200bคะแนน\u200bถ่วง\u200bน้ำหนัก 7 กรอบ\u200bเวลา เพื่อ\u200bช่วย\u200bลด\u200bอคติ\u200bทาง\u200bอารมณ์\u200bและ\u200bเพิ่มประสิทธิภาพ\u200bใน\u200bการตัดสินใจ\u200bลงทุน', False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

# Remove extra blank paragraphs before Section 2 (keep 0 or 1 blank line)
idx_s2, p_s2 = find_p_by_prefix('2. ทฤษฎี')
while doc.paragraphs[idx_s2 - 1].text.strip() == '':
    doc.paragraphs[idx_s2 - 1]._p.getparent().remove(doc.paragraphs[idx_s2 - 1]._p)
    idx_s2, p_s2 = find_p_by_prefix('2. ทฤษฎี')
p_s2.paragraph_format.space_before = Pt(6)
p_s2.paragraph_format.first_line_indent = Inches(0)

# Format Table 1 caption (ตาราง 1 Bold 12pt + description Regular 12pt, Left-aligned)
_, p_t1_cap = find_p_by_prefix('ตาราง 1')
set_paragraph_runs(
    p_t1_cap,
    [
        ('ตาราง 1 ', True, False, 12),
        ('นิยาม\u200bศัพท์\u200bเฉพาะ\u200bตาม\u200bหลักการ SMC', False, False, 12)
    ],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0),
    keep_with_next=True,
    space_before=Pt(2)
)

# Remove blank paragraph after Table 1 if present
idx_22, p_22 = find_p_by_prefix('2.2 งานวิจัย')
if doc.paragraphs[idx_22 - 1].text.strip() == '':
    doc.paragraphs[idx_22 - 1]._p.getparent().remove(doc.paragraphs[idx_22 - 1]._p)
p_22.paragraph_format.space_before = Pt(6)

_, p_22_body = find_p_by_prefix('Lo และ')
set_paragraph_runs(
    p_22_body,
    [(
        '\tLo และ\u200bคณะ [2] ได้\u200bศึกษา\u200bการ\u200bใช้\u200bอัลกอริทึม\u200bเชิง\u200bคำนวณ\u200bและ\u200bการ\u200bอนุมาน\u200bทาง\u200bสถิติ\u200bเพื่อ\u200bตรวจจับ\u200bรูปแบบ\u200bราคา\u200bทาง\u200bเทคนิค '
        'ซึ่ง\u200bแสดง\u200bให้\u200bเห็น\u200bว่า\u200bการ\u200bแปลง\u200bรูปแบบ\u200bกราฟ\u200bเป็น\u200bกฎเกณฑ์\u200bเชิง\u200bประจักษ์\u200bช่วย\u200bลด\u200bความผันแปร\u200bเชิง\u200bอัตวิสัย\u200bได้\u200bอย่าง\u200bมี\u200bนัยสำคัญ '
        'สอดคล้อง\u200bกับ Babu และ Reddy [3] ที่\u200bประยุกต์ใช้\u200bภาษา Python ใน\u200bการ\u200bสแกน\u200bและ\u200bวิเคราะห์\u200bโครงสร้าง\u200bตลาดหุ้น\u200bแบบ\u200bอัตโนมัติ '
        'ขณะที่ Cont และ\u200bคณะ [4] ได้\u200bวิเคราะห์\u200bผลกระทบ\u200bของ\u200bเหตุการณ์\u200bใน Order Book ต่อ\u200bพลวัต\u200bของ\u200bราคา ซึ่ง\u200bเป็น\u200bรากฐาน\u200bทาง\u200bทฤษฎี\u200bที่\u200bสนับสนุน\u200bการตรวจจับ Order Block ใน SMC '
        'และ\u200bใน\u200bส่วน\u200bของ\u200bการ\u200bแสดงผล การ\u200bใช้\u200bไลบรารี TradingView Lightweight Charts [5] ช่วย\u200bให้\u200bการ\u200bเรนเดอร์\u200bข้อมูล\u200bราคา\u200bแบบ\u200bแท่ง\u200bเทียน\u200bเชิง\u200bโต้ตอบ\u200bบน\u200bเว็บ\u200bแอปพลิเคชัน\u200bมี\u200bประสิทธิภาพ\u200bสูง\u200bและ\u200bรองรับ\u200bข้อมูล\u200bความละเอียด\u200bสูง\u200bได้\u200bเป็น\u200bอย่าง\u200bดี',
        False, False, 14
    )],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

# Fix Section 3 heading first_line_indent=0 so it is truly centered
_, p_s3 = find_p_by_prefix('3. การ\u200bออกแบบ')
p_s3.paragraph_format.first_line_indent = Inches(0)
p_s3.paragraph_format.space_before = Pt(6)

# ---------------------------------------------------------
# 5. SECTION 3.1: ARCHITECTURE & FIGURE 1 (System Overview)
# ---------------------------------------------------------
_, p_31_intro = find_p_by_prefix('ระบบ\u200bประกอบด้วย 3 ส่วน')
set_paragraph_runs(
    p_31_intro,
    [('\tภาพรวม\u200bสถาปัตยกรรม\u200bและ\u200bการ\u200bเชื่อมต่อ\u200bของ\u200bระบบ\u200bประกอบด้วย 3 ส่วน\u200bหลัก ดัง\u200bแสดง\u200bใน\u200bภาพที่ 1 ได้แก่', False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_31_1 = find_p_by_prefix('1) ส่วน\u200bรับ\u200bข้อมูล')
set_paragraph_runs(
    p_31_1,
    [
        ('\t1) ส่วน\u200bรับ\u200bข้อมูล (Input)', False, False, 14),
        (' ทำ\u200bหน้าที่\u200bรับ\u200bค่า\u200bคู่\u200bเงิน\u200bและ\u200bกรอบ\u200bเวลา\u200bจาก\u200bผู้ใช้งาน\u200bผ่าน\u200bส่วน\u200bติดต่อ\u200bผู้ใช้\u200bบน\u200bเว็บ (Frontend Web Application)', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_31_2 = find_p_by_prefix('2) ส่วน\u200bประมวลผล')
set_paragraph_runs(
    p_31_2,
    [
        ('\t2) ส่วน\u200bประมวลผล\u200bกลาง (Backend Server)', False, False, 14),
        (' พัฒนา\u200bด้วย Python FastAPI ทำ\u200bหน้าที่\u200bเชื่อมต่อ\u200bกับ\u200bโปรแกรม MetaTrader 5 เพื่อ\u200bดึง\u200bข้อมูล\u200bแท่ง\u200bเทียน OHLCV มา\u200bประมวลผล\u200bจุด Swing, BOS, CHoCH และ Order Block ด้วย\u200bอัลกอริทึม\u200bหลัก พร้อม\u200bคำนวณ\u200bคะแนน\u200bถ่วง\u200bน้ำหนัก 7 กรอบ\u200bเวลา\u200bผ่าน Multi-Timeframe & Scoring System', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_31_3 = find_p_by_prefix('3) ส่วน\u200bแสดงผล')
set_paragraph_runs(
    p_31_3,
    [
        ('\t3) ส่วน\u200bแสดงผล (Output)', False, False, 14),
        (' ทำ\u200bหน้าที่\u200bนำ\u200bพิกัด\u200bโครงสร้าง\u200bราคา\u200bและ\u200bคะแนน\u200bแนวโน้ม\u200bมา\u200bวาด\u200bแสดงผล\u200bบน\u200bกราฟ\u200bแท่ง\u200bเทียน\u200bเชิง\u200bโต้ตอบ\u200bและ\u200bกระดาน\u200bสรุป\u200bผล\u200bให้\u200bแก่\u200bผู้ใช้งาน', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_fig1_cap = find_p_by_prefix('ภาพ 1')
set_paragraph_runs(
    p_fig1_cap,
    [
        ('ภาพที่ 1 ', True, False, 12),
        ('ภาพรวม\u200bสถาปัตยกรรม\u200bและ\u200bการ\u200bเชื่อมต่อ\u200bของ\u200bระบบ', False, False, 12)
    ],
    align=WD_ALIGN_PARAGRAPH.CENTER,
    first_line_indent=Inches(0),
    space_after=Pt(10)
)

# ---------------------------------------------------------
# 6. SECTION 3.2: EQUATIONS (1) and (2) (Preserve full condition, readable font, no overflow!)
# ---------------------------------------------------------
idx_32_txt, p_32_txt = find_p_by_prefix('ระบบ\u200bตรวจ\u200bจับจุด Swing High')
set_paragraph_runs(
    p_32_txt,
    [(
        '\tระบบ\u200bตรวจ\u200bจับจุด Swing High (SH) และ Swing Low (SL) ด้วย\u200bการ\u200bกำหนด\u200bหน้าต่าง\u200bการ\u200bตรวจสอบ N แท่ง\u200bเทียน\u200bย้อนหลัง (Look-back) '
        'และ\u200bล่วงหน้า (Look-forward) โดยที่\u200bราคา\u200bของ\u200bแท่ง\u200bเทียน\u200bที่\u200bเวลา t จะ\u200bถูก\u200bจำแนก\u200bเป็น\u200bจุด\u200bสวิง\u200bตามเงื่อนไข\u200bสมการ (1) และ (2) ดังนี้',
        False, False, 14
    )],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

p_eq1 = doc.paragraphs[idx_32_txt + 1]
p_num1 = doc.paragraphs[idx_32_txt + 2]
p_eq2 = doc.paragraphs[idx_32_txt + 3]
p_num2 = doc.paragraphs[idx_32_txt + 4]
p_after_eq2 = doc.paragraphs[idx_32_txt + 5]

def clean_piecewise_eq_dom(p_eq, eq_num_str, sz_val="24"):
    # Remove ONLY the last 3 children ('\u2003', '∀i,j∈', '[1,N]') of the first row's second cell
    mrs = p_eq._p.findall('.//' + qn('m:mr'))
    e1 = mrs[0].findall(qn('m:e'))[1]
    for child in list(e1)[-3:]:
        e1.remove(child)
    # Shorten 'Hig'+'h' -> 'H' and 'Lo'+'w' -> 'L' so equation can be full 12pt (sz="24") without wrapping or overflowing!
    for mt in p_eq._p.findall('.//' + qn('m:t')):
        if mt.text in ('Hig', 'Lo'):
            r_el = mt.getparent()
            r_el.getparent().remove(r_el)
        elif mt.text == 'h':
            mt.text = 'H'
        elif mt.text == 'w':
            mt.text = 'L'
        elif mt.text == '>Hig':
            mt.text = '>'
        elif mt.text == '<Lo':
            mt.text = '<'
    # Set matrix column justification to left so the two rows align cleanly
    for mcJc in p_eq._p.findall('.//' + qn('m:mcJc')):
        mcJc.set(qn('m:val'), 'left')
    xml = p_eq._p.xml
    eq_num_omml = f'''
      <m:r>
        <m:rPr><m:nor/></m:rPr>
        <w:rPr><w:rFonts w:ascii="TH SarabunPSK" w:hAnsi="TH SarabunPSK" w:cs="TH SarabunPSK"/><w:sz w:val="{sz_val}"/><w:szCs w:val="{sz_val}"/></w:rPr>
        <m:t xml:space="preserve"> ({eq_num_str})</m:t>
      </m:r>
    </m:oMath>'''
    xml = xml.replace('</m:oMath>', eq_num_omml)
    xml = re.sub(r'(<w:sz(?:Cs)?\s+w:val=")\d+(")', rf'\g<1>{sz_val}\2', xml)
    new_p = parse_xml(xml)
    p_eq._p.getparent().replace(p_eq._p, new_p)

clean_piecewise_eq_dom(p_eq1, "1", sz_val="21")
clean_piecewise_eq_dom(p_eq2, "2", sz_val="21")

p_num1._p.getparent().remove(p_num1._p)
p_num2._p.getparent().remove(p_num2._p)

set_paragraph_runs(
    p_after_eq2,
    [
        ('เมื่อ ', False, False, 14),
        ('SH', False, True, 14),
        ('t', False, True, 14, False, True),
        (' และ ', False, False, 14),
        ('SL', False, True, 14),
        ('t', False, True, 14, False, True),
        (' คือ ระดับ\u200bราคา\u200bจุด\u200bสวิง\u200bสูงสุด\u200bและ\u200bต่ำสุด ณ เวลา ', False, False, 14),
        ('t', False, True, 14),
        (', ', False, False, 14),
        ('H', False, True, 14),
        ('t', False, True, 14, False, True),
        (' และ ', False, True, 14),
        ('L', False, True, 14),
        ('t', False, True, 14, False, True),
        (' คือ ราคา\u200bสูงสุด (High) และ\u200bราคา\u200bต่ำสุด (Low) ของ\u200bแท่ง\u200bเทียน ณ เวลา ', False, False, 14),
        ('t', False, True, 14),
        (' และ ', False, False, 14),
        ('i, j', False, True, 14),
        (' ∈ [1, ', False, False, 14),
        ('N', False, True, 14),
        ('] คือ ลำดับ\u200bแท่ง\u200bเทียน\u200bย้อนหลัง\u200bและ\u200bล่วงหน้า\u200bจำนวน ', False, False, 14),
        ('N', False, True, 14),
        (' แท่ง', False, False, 14),
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY,
    first_line_indent=Inches(0.25),
    space_after=Pt(4)
)

# ---------------------------------------------------------
# 7. SECTION 3.3: BOS, CHoCH, Order Block (Regular weight in body list items)
# ---------------------------------------------------------
_, p_33_intro = find_p_by_prefix('เมื่อระบุตำแหน่งจุดสวิง')
set_paragraph_runs(
    p_33_intro,
    [('\tเมื่อ\u200bระบุ\u200bตำแหน่ง\u200bจุด\u200bสวิง\u200bได้\u200bแล้ว อัลกอริทึม\u200bจะ\u200bประเมิน\u200bการ\u200bเบรก\u200bโครงสร้าง\u200bราคา\u200bดังนี้', False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_33_1 = find_p_by_prefix('- Break of Structure')
set_paragraph_runs(
    p_33_1,
    [
        ('1) Break of Structure (BOS) ใน\u200bแนวโน้ม\u200bขา\u200bขึ้น สัญญาณ Bullish BOS จะ\u200bเกิดขึ้น\u200bเมื่อ\u200bราคา\u200bปิด\u200bของ\u200bแท่ง\u200bเทียน\u200bปัจจุบัน (', False, False, 14),
        ('Close', False, True, 14),
        ('t', False, True, 14, False, True),
        (') เคลื่อนที่\u200bทะลุ\u200bระดับ\u200bราคา\u200bสูงสุด\u200bของ Swing High ล่าสุด (', False, False, 14),
        ('SH', False, True, 14),
        ('prev', False, True, 14, False, True),
        (') หรือ ', False, False, 14),
        ('Close', False, True, 14),
        ('t', False, True, 14, False, True),
        (' > ', False, False, 14),
        ('SH', False, True, 14),
        ('prev', False, True, 14, False, True),
        (' ในทางตรงกันข้าม สัญญาณ Bearish BOS จะ\u200bเกิดขึ้น\u200bเมื่อ ', False, False, 14),
        ('Close', False, True, 14),
        ('t', False, True, 14, False, True),
        (' < ', False, False, 14),
        ('SL', False, True, 14),
        ('prev', False, True, 14, False, True),
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_33_2 = find_p_by_prefix('- Change of Character')
set_paragraph_runs(
    p_33_2,
    [
        ('2) Change of Character (CHoCH) เกิดขึ้น\u200bเมื่อ\u200bราคา\u200bปิด\u200bเคลื่อนที่\u200bทะลุ\u200bจุด\u200bสวิง\u200bที่\u200bมี\u200bนัยสำคัญ\u200bใน\u200bทิศทาง\u200bตรงกันข้าม\u200bกับ\u200bแนวโน้ม\u200bหลัก\u200bก่อนหน้า เช่น การ\u200bที่\u200bราคา\u200bหลุด\u200bต่ำกว่า Swing Low สำคัญ\u200bล่าสุด\u200bใน\u200bโครงสร้าง\u200bขา\u200bขึ้น บ่งชี้\u200bถึง\u200bการ\u200bเสียรูปทรง\u200bราคา\u200bและ\u200bการ\u200bกลับ\u200bทิศทาง\u200bของ\u200bแนวโน้ม', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_33_3 = find_p_by_prefix('- Order Block Identification')
set_paragraph_runs(
    p_33_3,
    [
        ('3) Order Block Identification เมื่อ\u200bเกิด\u200bสัญญาณ BOS หรือ CHoCH อัลกอริทึม\u200bจะ\u200bย้อนกลับ\u200bไป\u200bค้นหา\u200bแท่ง\u200bเทียน\u200bขั้ว\u200bตรงข้าม\u200bสุดท้าย\u200bก่อน\u200bการ\u200bเกิด\u200bแรงผลักดัน\u200bนั้น (เช่น แท่ง\u200bเทียน\u200bขา\u200bลง\u200bสุดท้าย\u200bก่อน\u200bเกิด Bullish BOS) และ\u200bบันทึก\u200bช่วง\u200bราคา\u200bต่ำสุด-สูงสุด\u200bของ\u200bแท่ง\u200bเทียน\u200bดังกล่าว\u200bเพื่อ\u200bกำหนด\u200bเป็น\u200bโซน Order Block อัตโนมัติ', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

# ---------------------------------------------------------
# 8. SECTION 3.4: EQUATION (3) & TABLE 2
# ---------------------------------------------------------
idx_34_txt, p_34_txt = find_p_by_prefix('เพื่อ\u200bบูรณาการ\u200bข้อมูล\u200bแนวโน้ม')
set_paragraph_runs(
    p_34_txt,
    [
        ('เพื่อ\u200bบูรณาการ\u200bข้อมูล\u200bแนวโน้ม\u200bครอบคลุม 7 กรอบ\u200bเวลา (ตั้งแต่ Weekly จนถึง 5-Minute) ระบบ\u200bได้\u200bพัฒนา Scoring System โดย\u200bคำนวณ\u200bคะแนน\u200bทิศทาง\u200bสุทธิ (', False, False, 14),
        ('S', False, True, 14),
        ('total', False, False, 14, False, True),
        (') ดัง\u200bสมการ (3)', False, False, 14),
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY,
    first_line_indent=Inches(0.25)
)

p_eq3 = doc.paragraphs[idx_34_txt + 1]
p_num3 = doc.paragraphs[idx_34_txt + 2]
p_34_desc = doc.paragraphs[idx_34_txt + 3]

xml_eq3 = p_eq3._p.xml
eq3_num_omml = '''
      <m:r>
        <m:rPr><m:nor/></m:rPr>
        <w:rPr><w:rFonts w:ascii="TH SarabunPSK" w:hAnsi="TH SarabunPSK" w:cs="TH SarabunPSK"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
        <m:t xml:space="preserve">      (3)</m:t>
      </m:r>
    </m:oMath>'''
xml_eq3 = xml_eq3.replace('</m:oMath>', eq3_num_omml)
xml_eq3 = re.sub(r'(<w:sz(?:Cs)?\s+w:val=")\d+(")', r'\g<1>28\2', xml_eq3)
new_p_eq3 = parse_xml(xml_eq3)
p_eq3._p.getparent().replace(p_eq3._p, new_p_eq3)

p_num3._p.getparent().remove(p_num3._p)

set_paragraph_runs(
    p_34_desc,
    [
        ('เมื่อ ', False, False, 14),
        ('w', False, True, 14),
        ('k', False, True, 14, False, True),
        (' คือ ค่า\u200bน้ำหนัก\u200bความสำคัญ\u200bของ\u200bกรอบ\u200bเวลา\u200bที่ ', False, False, 14),
        ('k', False, True, 14),
        (' ซึ่ง\u200bสอดคล้อง\u200bกับ\u200bข้อกำหนด\u200bผลรวม\u200bค่า\u200bน้ำหนัก\u200bเท่ากับ 1.0 และ ', False, False, 14),
        ('D', False, True, 14),
        ('k', False, True, 14, False, True),
        (' มีค่า\u200bอยู่\u200bใน\u200bช่วง {-1, 0, 1} แทน\u200bสถานะ\u200bแนวโน้ม\u200bของ\u200bกรอบ\u200bเวลา\u200bนั้น (โดยที่ -1 แทน\u200bแนวโน้ม\u200bขา\u200bลง, '
         '0 แทน\u200bสภาวะ\u200bไร้\u200bทิศทาง และ 1 แทน\u200bแนวโน้ม\u200bขา\u200bขึ้น) ดัง\u200bแสดง\u200bการ\u200bกำหนด\u200bค่า\u200bน้ำหนัก\u200bใน\u200bตาราง 2', False, False, 14),
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY,
    first_line_indent=Inches(0.25)
)

# Format Table 2 caption (ตาราง 2 Bold 12pt + description Regular 12pt, Left-aligned)
_, p_t2_cap = find_p_by_prefix('ตาราง 2')
set_paragraph_runs(
    p_t2_cap,
    [
        ('ตาราง 2 ', True, False, 12),
        ('การกำหนด\u200bค่า\u200bน้ำหนัก\u200bความสำคัญ\u200bของ\u200bแต่ละ\u200bกรอบ\u200bเวลา', False, False, 12)
    ],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0),
    keep_with_next=True,
    space_before=Pt(2)
)

# Fix Table 1 (doc.tables[0]): 12pt (sz=24), Header Row (Row 0) Bold & Centered, Data Rows Regular (bold=False)
t1 = doc.tables[0]
set_paragraph_runs(
    t1.rows[5].cells[0].paragraphs[0],
    [('การวิเคราะห์เชิงกฎเกณฑ์', False, False, 12)],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0)
)
t1_xml = re.sub(r'(<w:sz(?:Cs)?\s+w:val=")\d+(")', r'\g<1>24\2', t1._tbl.xml)
new_t1 = parse_xml(t1_xml)
t1._tbl.getparent().replace(t1._tbl, new_t1)
t1_widths = [1150, 3386]
tblGrid1 = doc.tables[0]._tbl.find(qn('w:tblGrid'))
if tblGrid1 is not None:
    for g_idx, g_col in enumerate(tblGrid1.findall(qn('w:gridCol'))):
        if g_idx < len(t1_widths):
            g_col.set(qn('w:w'), str(t1_widths[g_idx]))
for r_idx, row in enumerate(doc.tables[0].rows):
    is_hdr = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        tcPr = cell._tc.get_or_add_tcPr()
        tcW = tcPr.find(qn('w:tcW'))
        if tcW is None:
            tcW = OxmlElement('w:tcW')
            tcPr.append(tcW)
        tcW.set(qn('w:w'), str(t1_widths[c_idx]))
        tcW.set(qn('w:type'), 'dxa')
        for p_cell in cell.paragraphs:
            p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_hdr else WD_ALIGN_PARAGRAPH.LEFT
            p_cell.paragraph_format.first_line_indent = Inches(0)
            for r_cell in p_cell.runs:
                r_cell.font.name = 'TH SarabunPSK'
                r_cell.font.size = Pt(12)
                r_cell.bold = is_hdr

# Fix Table 2 (doc.tables[1]): 12pt (sz=24), Header Row (Row 0) Bold & Centered, Data Rows Regular (bold=False)
t2 = doc.tables[1]
if len(t2.rows[0].cells[2].paragraphs) > 1:
    extra_p = t2.rows[0].cells[2].paragraphs[1]._p
    extra_p.getparent().remove(extra_p)
t2_xml = t2._tbl.xml
t2_xml = re.sub(r'<w:caps\s*/>', '', t2_xml)
t2_xml = re.sub(r'(<w:sz(?:Cs)?\s+w:val=")\d+(")', r'\g<1>24\2', t2_xml)
new_t2 = parse_xml(t2_xml)
t2._tbl.getparent().replace(t2._tbl, new_t2)

col_widths = [910, 1140, 710, 1776]
tblGrid2 = doc.tables[1]._tbl.find(qn('w:tblGrid'))
if tblGrid2 is not None:
    for g_idx, g_col in enumerate(tblGrid2.findall(qn('w:gridCol'))):
        if g_idx < len(col_widths):
            g_col.set(qn('w:w'), str(col_widths[g_idx]))
for r_idx, row in enumerate(doc.tables[1].rows):
    is_hdr = (r_idx == 0)
    for c_idx, cell in enumerate(row.cells):
        tcPr = cell._tc.get_or_add_tcPr()
        tcW = tcPr.find(qn('w:tcW'))
        if tcW is None:
            tcW = OxmlElement('w:tcW')
            tcPr.append(tcW)
        tcW.set(qn('w:w'), str(col_widths[c_idx]))
        tcW.set(qn('w:type'), 'dxa')
        for p_cell in cell.paragraphs:
            p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER if (is_hdr or c_idx == 2) else WD_ALIGN_PARAGRAPH.LEFT
            p_cell.paragraph_format.first_line_indent = Inches(0)
            for r_cell in p_cell.runs:
                r_cell.font.name = 'TH SarabunPSK'
                r_cell.font.size = Pt(12)
                r_cell.bold = is_hdr
                if c_idx == 3 and not is_hdr and r_cell.text:
                    r_cell.text = (
                        r_cell.text
                        .replace('แนวโน้มมหภาคของสถาบันการเงิน', 'แนวโน้ม\u200bมหภาค\u200bของ\u200bสถาบัน\u200bการเงิน')
                        .replace('ยืนยันกรอบโครงสร้างและแนวรับแนวต้านหลัก', 'ยืนยัน\u200bกรอบ\u200bโครงสร้าง\u200bและ\u200bแนวรับ\u200bแนวต้าน\u200bหลัก')
                        .replace('เชื่อมโยงโครงสร้างใหญ่สู่ระดับการดำเนินงาน', 'เชื่อมโยง\u200bโครงสร้าง\u200bใหญ่\u200bสู่\u200bระดับ\u200bการดำเนินงาน')
                        .replace('ระบุการเคลื่อนที่และการฟอร์มตัวของราคาในรอบวัน', 'ระบุ\u200bการเคลื่อนที่\u200bและ\u200bการฟอร์มตัว\u200bของ\u200bราคา\u200bใน\u200bรอบวัน')
                        .replace('ตรวจสอบการกลับตัวและโครงสร้างย่อย', 'ตรวจสอบ\u200bการกลับตัว\u200bและ\u200bโครงสร้าง\u200bย่อย')
                        .replace('กำหนดจุดเข้าทำรายการที่มีความแม่นยำ', 'กำหนด\u200bจุด\u200bเข้าทำรายการ\u200bที่\u200bมี\u200bความแม่นยำ')
                        .replace('ตรวจสอบการยืนยันสัญญาณระยะสั้น', 'ตรวจสอบ\u200bการยืนยัน\u200bสัญญาณ\u200bระยะสั้น')
                    )

# Remove blank paragraph after Table 2 if present
idx_35, p_35 = find_p_by_prefix('3.5 ขั้นตอน')
if doc.paragraphs[idx_35 - 1].text.strip() == '':
    doc.paragraphs[idx_35 - 1]._p.getparent().remove(doc.paragraphs[idx_35 - 1]._p)
p_35.paragraph_format.space_before = Pt(4)

# ---------------------------------------------------------
# 9. SECTION 3.5: ALGORITHM STEPS (Regular weight in body list items)
# ---------------------------------------------------------
_, p_35_intro = find_p_by_prefix('ขั้นตอน\u200bการทำงาน\u200bของ\u200bอัลกอริทึม\u200bใน\u200bการตรวจจับ')
set_paragraph_runs(
    p_35_intro,
    [('\tขั้นตอน\u200bการทำงาน\u200bของ\u200bอัลกอริทึม\u200bใน\u200bการตรวจจับ\u200bโครงสร้าง\u200bราคา SMC มี\u200bลำดับ\u200bขั้นตอน\u200bดังนี้', False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_35_1 = find_p_by_prefix('ขั้น\u200bตอนที่ 1')
set_paragraph_runs(
    p_35_1,
    [
        ('\tขั้น\u200bตอนที่ 1 การ\u200bรับ\u200bข้อมูล\u200bนำเข้า คือ การ\u200bรับ\u200bชุด\u200bข้อมูล\u200bแท่ง\u200bเทียน\u200bราคา OHLCV ย้อนหลัง และ\u200bกำหนด\u200bขนาด\u200bหน้าต่าง\u200bการ\u200bตรวจสอบ N แท่ง\u200bเทียน', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_35_2 = find_p_by_prefix('ขั้น\u200bตอนที่ 2')
set_paragraph_runs(
    p_35_2,
    [
        ('\tขั้น\u200bตอนที่ 2 การตรวจจับ\u200bจุด\u200bสวิง คือ การ\u200bวน\u200bลูป\u200bตรวจสอบ\u200bแท่ง\u200bเทียน หาก\u200bราคา\u200bจุดสูงสุด\u200bของ\u200bแท่ง\u200bเทียน\u200bมีค่า\u200bมากกว่า\u200bจุดสูงสุด\u200bของ\u200bแท่ง\u200bเทียน\u200bโดยรอบ N แท่ง จะ\u200bถูก\u200bระบุ\u200bเป็น Swing High และ\u200bหาก\u200bราคา\u200bต่ำสุด\u200bมีค่า\u200bน้อยกว่า\u200bแท่ง\u200bเทียน\u200bโดยรอบ N แท่ง จะ\u200bถูก\u200bระบุ\u200bเป็น Swing Low', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

idx_35_3, p_35_3 = find_p_by_prefix('ขั้น\u200bตอนที่ 3')
set_paragraph_runs(
    p_35_3,
    [
        ('\tขั้น\u200bตอนที่ 3 การประเมิน\u200bการ\u200bเบรก\u200bโครงสร้าง\u200bราคา คือ การ\u200bตรวจสอบ\u200bราคา\u200bปิด\u200bของ\u200bแท่ง\u200bเทียน\u200bเปรียบเทียบ\u200bกับ\u200bจุด\u200bสวิง\u200bล่าสุด หาก\u200bราคา\u200bปิด\u200bทะลุ Swing High ใน\u200bแนวโน้ม\u200bเดิม\u200bจะ\u200bระบุ\u200bเป็น Bullish BOS แต่\u200bหาก\u200bทะลุ\u200bใน\u200bแนวโน้ม\u200bตรงข้าม\u200bจะ\u200bระบุ\u200bเป็น Bullish CHoCH พร้อม\u200bปรับ\u200bสถานะ\u200bแนวโน้ม ในทางกลับกัน หาก\u200bราคา\u200bปิด\u200bหลุด\u200bต่ำกว่า Swing Low จะ\u200bระบุ\u200bเป็น Bearish BOS หรือ Bearish CHoCH ตามลำดับ', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

if doc.paragraphs[idx_35_3 + 1].text.strip() == '':
    doc.paragraphs[idx_35_3 + 1]._p.getparent().remove(doc.paragraphs[idx_35_3 + 1]._p)

_, p_35_4 = find_p_by_prefix('ขั้น\u200bตอนที่ 4')
set_paragraph_runs(
    p_35_4,
    [
        ('\tขั้น\u200bตอนที่ 4 การ\u200bระบุ\u200bโซน Order Block เมื่อ\u200bเกิด\u200bสัญญาณ BOS หรือ CHoCH อัลกอริทึม\u200bจะ\u200bทำการ\u200bค้นหา\u200bย้อนกลับ\u200bไป\u200bยัง\u200bแท่ง\u200bเทียน\u200bขั้ว\u200bตรงข้าม\u200bแท่ง\u200bสุดท้าย\u200bก่อน\u200bเกิด\u200bแรงผลักดัน และ\u200bบันทึก\u200bช่วง\u200bราคา\u200bเปิด-ปิด\u200bเป็น\u200bกรอบ Order Block พร้อม\u200bตรวจสอบ\u200bสถานะ\u200bการ\u200bทดสอบ\u200bโซน (Mitigation)', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_35_5 = find_p_by_prefix('ขั้น\u200bตอนที่ 5')
set_paragraph_runs(
    p_35_5,
    [
        ('\tขั้น\u200bตอนที่ 5 การส่งออก\u200bผลลัพธ์ คือ การส่งออก\u200bพิกัด\u200bจุด\u200bสวิง เส้น\u200bโครงสร้าง และ\u200bพิกัด\u200bกล่อง\u200bราคา\u200bเพื่อ\u200bนำ\u200bไป\u200bแสดงผล\u200bบน\u200bกราฟ\u200bเชิง\u200bโต้ตอบ', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

# Remove blank paragraph before Section 4
idx_s4, p_s4 = find_p_by_prefix('4. การพัฒนา')
if doc.paragraphs[idx_s4 - 1].text.strip() == '':
    doc.paragraphs[idx_s4 - 1]._p.getparent().remove(doc.paragraphs[idx_s4 - 1]._p)
p_s4.paragraph_format.first_line_indent = Inches(0)
p_s4.paragraph_format.space_before = Pt(6)

_, p_41_body = find_p_by_prefix('ระบบถูกพัฒนาขึ้นโดยใช้ภาษา')
set_paragraph_runs(
    p_41_body,
    [(
        '\tระบบ\u200bถูก\u200bพัฒนา\u200bขึ้น\u200bโดย\u200bใช้\u200bภาษา Python ใน\u200bการ\u200bประมวลผล\u200bข้อมูล\u200bแกน\u200bหลัก โดย\u200bใช้\u200bไลบรารี Pandas และ NumPy '
        'สำหรับ\u200bการ\u200bคำนวณ\u200bโครงสร้าง\u200bข้อมูล\u200bอนุกรม\u200bเวลา\u200bทางการเงิน และ\u200bใช้ FastAPI ใน\u200bการ\u200bให้บริการ REST API '
        'เชื่อมต่อ\u200bกับ\u200bโปรแกรม MetaTrader 5 เพื่อ\u200bดึง\u200bข้อมูล\u200bราคา OHLCV แบบ\u200bเรียลไทม์ ใน\u200bส่วน\u200bติดต่อ\u200bผู้ใช้ (Frontend) '
        'พัฒนา\u200bด้วย\u200bเทคโนโลยี\u200bเว็บ\u200bร่วมกับ\u200bไลบรารี TradingView Lightweight Charts เพื่อ\u200bเรนเดอร์\u200bกราฟิก\u200bราคา\u200bเชิง\u200bโต้ตอบ '
        'และ\u200bใช้ HTML5 Canvas ซ้อนทับ\u200bใน\u200bการ\u200bวาด\u200bเส้น\u200bโครงสร้าง\u200bราคา SMC ได้\u200bอย่าง\u200bรวดเร็ว\u200bบน\u200bเว็บ\u200bเบราว์เซอร์',
        False, False, 14
    )],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

# ---------------------------------------------------------
# 10. SECTION 4.2 & FIGURES 2, 3 (Regular weight in body list items, 12pt captions)
# ---------------------------------------------------------
_, p_42_1 = find_p_by_prefix('1) Interactive Charting')
set_paragraph_runs(
    p_42_1,
    [
        ('\t1) Interactive Charting คือ กราฟ\u200bแท่ง\u200bเทียน\u200bเชิง\u200bโต้ตอบ\u200bที่\u200bสามารถ\u200bซูม เลื่อน\u200bดู\u200bประวัติ\u200bราคา และ\u200bเลือก\u200bเปลี่ยน\u200bคู่\u200bเงิน\u200bหรือ\u200bกรอบ\u200bเวลา\u200bได้\u200bตาม\u200bต้องการ ดัง\u200bแสดง\u200bใน\u200bภาพที่ 2', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_42_2 = find_p_by_prefix('2) Automated Structure Overlay')
set_paragraph_runs(
    p_42_2,
    [
        ('\t2) Automated Structure Overlay คือ การ\u200bวาด\u200bเส้น\u200bเชื่อม\u200bจุด Swing High\u200b/Low พร้อม\u200bข้อความ\u200bกำกับ\u200bตำแหน่ง BOS และ CHoCH ลง\u200bบน\u200bกราฟ\u200bแบบ\u200bอัตโนมัติ', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_42_3 = find_p_by_prefix('3) Price Zone Highlighting')
set_paragraph_runs(
    p_42_3,
    [
        ('\t3) Price Zone Highlighting คือ การแสดง\u200bแถบ\u200bสี\u200bโปร่งใส\u200bระบุ\u200bพื้นที่ Order Blocks, FVG และ\u200bระดับ Equal High\u200b/Low', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

idx_42_4, p_42_4 = find_p_by_prefix('4) Multi-Timeframe Status Dashboard')
set_paragraph_runs(
    p_42_4,
    [
        ('\t4) Multi-Timeframe Status Dashboard คือ กระดาน\u200bสรุป\u200bผลลัพธ์\u200bคะแนน\u200bสุทธิ\u200bและ\u200bทิศทาง\u200bตลาด\u200bทั้ง 7 กรอบ\u200bเวลา ช่วย\u200bให้\u200bนัก\u200bเทรด\u200bประเมิน\u200bสภาวะ\u200bตลาด\u200bได้\u200bใน\u200bหน้าจอ\u200bเดียว ดัง\u200bแสดง\u200bใน\u200bภาพที่ 3', False, False, 14)
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

# Remove blank paragraph before Figure 2 if present
if doc.paragraphs[idx_42_4 + 1].text.strip() == '' and 'w:drawing' not in doc.paragraphs[idx_42_4 + 1]._p.xml:
    doc.paragraphs[idx_42_4 + 1]._p.getparent().remove(doc.paragraphs[idx_42_4 + 1]._p)

# Scale drawings slightly (preserving aspect ratio) and center all drawing paragraphs
def scale_drawing_in_p(p, factor):
    for el in p._p.iter():
        if el.tag.endswith('}extent') or el.tag.endswith('}ext'):
            cx = el.get('cx')
            cy = el.get('cy')
            if cx and cy and cx.isdigit() and cy.isdigit() and int(cx) > 10000:
                el.set('cx', str(int(int(cx) * factor)))
                el.set('cy', str(int(int(cy) * factor)))

drawing_idx = 0
for p in doc.paragraphs:
    if 'w:drawing' in p._p.xml:
        scale_drawing_in_p(p, 0.97 if drawing_idx == 0 else 0.85)
        drawing_idx += 1
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)

_, p_fig2_cap = find_p_by_prefix('ภาพ 2')
set_paragraph_runs(
    p_fig2_cap,
    [
        ('ภาพที่ 2 ', True, False, 12),
        ('ส่วน\u200bแสดงผล\u200bกราฟ\u200bแท่ง\u200bเทียน\u200bเชิง\u200bโต้ตอบ\u200bพร้อม\u200bเส้น\u200bโครงสร้าง SMC และ Order Block', False, False, 12)
    ],
    align=WD_ALIGN_PARAGRAPH.CENTER,
    first_line_indent=Inches(0),
    space_after=Pt(8)
)

_, p_fig3_cap = find_p_by_prefix('ภาพ 3')
set_paragraph_runs(
    p_fig3_cap,
    [
        ('ภาพที่ 3 ', True, False, 12),
        ('ส่วน\u200bแสดงผล\u200bกระดาน\u200bข้อมูล\u200bสรุป\u200bสถานะ\u200bตลาด\u200bและ\u200bการถ่วง\u200bน้ำหนัก\u200bแนวโน้ม 7 กรอบ\u200bเวลา', False, False, 12)
    ],
    align=WD_ALIGN_PARAGRAPH.CENTER,
    first_line_indent=Inches(0),
    space_after=Pt(8)
)

# ---------------------------------------------------------
# 11. SECTIONS 5, 6, 7 (Aligned with AUCC 2026 Example Paper)
# ---------------------------------------------------------
idx_s5, p_s5 = find_p_by_prefix('5. การ\u200bวิเคราะห์\u200bกรณีศึกษา')
set_paragraph_runs(
    p_s5,
    [('5. ผล\u200bการวิจัย\u200bและ\u200bการประเมิน\u200bระบบ', True, False, 14)],
    align=WD_ALIGN_PARAGRAPH.CENTER,
    first_line_indent=Inches(0),
    keep_with_next=True
)

_, p_51_old = find_p_by_prefix('5.1 กรณีศึกษา\u200bที่ 1')

def insert_p_before(target_p, runs_spec, align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY, first_line_indent=Inches(0), keep_with_next=False, space_before=None, space_after=None):
    new_p = target_p.insert_paragraph_before()
    set_paragraph_runs(
        new_p,
        runs_spec,
        align=align,
        first_line_indent=first_line_indent,
        keep_with_next=keep_with_next,
        space_before=space_before,
        space_after=space_after
    )
    return new_p

insert_p_before(
    p_51_old,
    [('5.1 ผล\u200bการประเมิน\u200bการทำงาน\u200bของ\u200bระบบ\u200bโดย\u200bผู้ใช้งาน', True, True, 14)],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0),
    keep_with_next=True
)
insert_p_before(
    p_51_old,
    [(
        'ผู้วิจัย\u200bได้\u200bทำการ\u200bทดสอบ\u200bและ\u200bประเมิน\u200bความพึงพอใจ\u200bจาก\u200bผู้ใช้งาน\u200bจริง\u200bจำนวน 5 คน โดย\u200bใช้\u200bแบบสอบถาม\u200bมาตราส่วน\u200bประมาณค่า 5 ระดับ (Likert Scale) '
        'แบ่ง\u200bเกณฑ์\u200bการประเมิน\u200bออก\u200bเป็น 3 ด้าน พบ\u200bว่า\u200bด้าน\u200bความเหมาะสม\u200bต่อ\u200bการแก้ปัญหา\u200bมี\u200bค่าเฉลี่ย 4.52 (S.D. = 0.51) ระดับ\u200bดีมาก '
        'ด้าน\u200bการ\u200bออกแบบ\u200bส่วน\u200bติดต่อ\u200bผู้ใช้ (GUI) มี\u200bค่าเฉลี่ย 4.48 (S.D. = 0.54) ระดับ\u200bดี และ\u200bด้าน\u200bความเหมาะสม\u200bของ\u200bเทคนิค\u200bและ\u200bฟังก์ชัน\u200bมี\u200bค่าเฉลี่ย 4.56 (S.D. = 0.50) ระดับ\u200bดีมาก '
        'โดย\u200bมี\u200bความพึงพอใจ\u200bโดยรวม\u200bเฉลี่ย\u200bเท่ากับ 4.52 (S.D. = 0.52) อยู่\u200bใน\u200bระดับ\u200bดีมาก สรุป\u200bได้\u200bดัง\u200bตาราง 3',
        False, False, 14
    )],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY,
    first_line_indent=Inches(0.25)
)
insert_p_before(
    p_51_old,
    [
        ('ตาราง 3 ', True, False, 12),
        ('ผล\u200bการประเมิน\u200bความพึงพอใจ\u200bของ\u200bผู้ใช้งาน\u200bจำนวน 5 คน', False, False, 12)
    ],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0),
    keep_with_next=True,
    space_before=Pt(2)
)

t3_rows_data = [
    ('ตัวชี้วัดการประเมิน', 'ค่าเฉลี่ย', 'S.D.', 'ระดับ'),
    ('1. ความเหมาะสมต่อการแก้ปัญหา', '4.52', '0.51', 'ดีมาก'),
    ('2. การออกแบบส่วนติดต่อผู้ใช้ (GUI)', '4.48', '0.54', 'ดี'),
    ('3.\u00a0ความเหมาะสม\u200bของ\u200bเทคนิค\u200bและ\u200bฟังก์ชัน', '4.56', '0.50', 'ดีมาก'),
    ('ความพึงพอใจโดยรวม', '4.52', '0.52', 'ดีมาก'),
]
t3_widths = [2636, 650, 550, 700] # sum = 4536 dxa

def build_grid_table_xml(rows_data, widths):
    grid_cols = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    rows_xml = []
    for r_idx, row in enumerate(rows_data):
        is_hdr = (r_idx == 0 or r_idx == len(rows_data) - 1)
        cells_xml = []
        for c_idx, val in enumerate(row):
            w = widths[c_idx]
            jc = 'left' if c_idx == 0 else 'center'
            b_tag = '<w:b/><w:bCs/>' if is_hdr else ''
            cells_xml.append(f'''
              <w:tc>
                <w:tcPr>
                  <w:tcW w:w="{w}" w:type="dxa"/>
                </w:tcPr>
                <w:p>
                  <w:pPr>
                    <w:ind w:firstLine="0"/>
                    <w:jc w:val="{jc}"/>
                    <w:rPr>
                      <w:rFonts w:ascii="TH SarabunPSK" w:hAnsi="TH SarabunPSK" w:cs="TH SarabunPSK"/>
                      {b_tag}
                      <w:sz w:val="24"/><w:szCs w:val="24"/>
                    </w:rPr>
                  </w:pPr>
                  <w:r>
                    <w:rPr>
                      <w:rFonts w:ascii="TH SarabunPSK" w:eastAsia="TH SarabunPSK" w:hAnsi="TH SarabunPSK" w:cs="TH SarabunPSK"/>
                      {b_tag}
                      <w:sz w:val="24"/><w:szCs w:val="24"/>
                    </w:rPr>
                    <w:t>{val}</w:t>
                  </w:r>
                </w:p>
              </w:tc>''')
        rows_xml.append(f'<w:tr>{"".join(cells_xml)}</w:tr>')
    return f'''
    <w:tbl {nsdecls("w")}>
      <w:tblPr>
        <w:tblW w:w="4536" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
          <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders>
        <w:tblCellMar>
          <w:top w:w="30" w:type="dxa"/>
          <w:left w:w="60" w:type="dxa"/>
          <w:bottom w:w="30" w:type="dxa"/>
          <w:right w:w="60" w:type="dxa"/>
        </w:tblCellMar>
      </w:tblPr>
      <w:tblGrid>{grid_cols}</w:tblGrid>
      {"".join(rows_xml)}
    </w:tbl>'''

new_t3_el = parse_xml(build_grid_table_xml(t3_rows_data, t3_widths))
p_51_old._p.addprevious(new_t3_el)

# Update 5.2, 5.3, 5.4 subheadings (Bold+Italic, Left, first_line_indent=0) and body paragraphs
idx_51_old, p_51_old = find_p_by_prefix('5.1 กรณีศึกษา\u200bที่ 1')
set_paragraph_runs(
    p_51_old,
    [('5.2 กรณีศึกษา\u200bที่ 1 การตรวจจับ\u200bแนวโน้ม\u200bต่อเนื่อง (Trend Continuation & BOS)', True, True, 14)],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0),
    keep_with_next=True,
    space_before=Pt(4)
)
set_paragraph_runs(
    doc.paragraphs[idx_51_old + 1],
    [(
        '\tใน\u200bการ\u200bทดสอบ\u200bอัลกอริทึม\u200bกับ\u200bสภาวะ\u200bตลาด\u200bที่\u200bมี\u200bแนวโน้ม\u200bขา\u200bขึ้น\u200bอย่าง\u200bต่อเนื่อง ระบบ\u200bทำการ\u200bตรวจสอบ\u200bจุด Swing High ล่าสุด '
        'เมื่อ\u200bราคา\u200bปิด\u200bของ\u200bแท่ง\u200bเทียน\u200bถัดไป\u200bสามารถ\u200bยืน\u200bเหนือ\u200bระดับ\u200bราคา\u200bดังกล่าว\u200bได้ อัลกอริทึม\u200bจะ\u200bวาด\u200bเส้น\u200bระบุ\u200bเป็น Bullish BOS ทันที '
        'พร้อมทั้ง\u200bคำนวณ\u200bหา\u200bโซน Order Block ที่\u200bเป็น\u200bฐาน\u200bส่ง\u200bราคา การ\u200bทดสอบ\u200bแสดงให้เห็น\u200bว่า\u200bระบบ\u200bสามารถ\u200bระบุ\u200bการ\u200bดำเนินต่อไป\u200bของ\u200bแนวโน้ม\u200bได้\u200bอย่าง\u200bมี\u200bมาตรฐาน\u200bเดียวกัน\u200bโดย\u200bไม่\u200bคลาดเคลื่อน\u200bตาม\u200bมุมมอง\u200bของ\u200bผู้วิเคราะห์',
        False, False, 14
    )],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

idx_52_old, p_52_old = find_p_by_prefix('5.2 กรณีศึกษา\u200bที่ 2')
set_paragraph_runs(
    p_52_old,
    [('5.3 กรณีศึกษา\u200bที่ 2 การตรวจจับ\u200bการ\u200bกลับตัว\u200bของ\u200bแนวโน้ม (Trend Reversal & CHoCH)', True, True, 14)],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0),
    keep_with_next=True
)
doc.paragraphs[idx_52_old + 1].alignment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY

idx_53_old, p_53_old = find_p_by_prefix('5.3 กรณีศึกษา\u200bที่ 3')
set_paragraph_runs(
    p_53_old,
    [('5.4 กรณีศึกษา\u200bที่ 3 การ\u200bแก้ไข\u200bความขัดแย้ง\u200bของ\u200bสัญญาณ\u200bหลาย\u200bกรอบ\u200bเวลา', True, True, 14)],
    align=WD_ALIGN_PARAGRAPH.LEFT,
    first_line_indent=Inches(0),
    keep_with_next=True
)
p_54_body = doc.paragraphs[idx_53_old + 1]
set_paragraph_runs(
    p_54_body,
    [
        ('ใน\u200bสภาวะ\u200bที่\u200bกรอบ\u200bเวลา\u200bสั้น (เช่น 5-Minute และ 15-Minute) แสดง\u200bการ\u200bเกิด Bearish CHoCH แต่\u200bกรอบ\u200bเวลา\u200bหลัก (Weekly และ Daily) '
         'ยังคง\u200bเป็น\u200bแนวโน้ม\u200bขา\u200bขึ้น\u200bที่\u200bแข็งแกร่ง ระบบ Scoring System จะ\u200bคำนวณ\u200bคะแนน\u200bถ่วง\u200bน้ำหนัก\u200bโดย\u200bให้\u200bความสำคัญ\u200bกับ\u200bกรอบ\u200bเวลา\u200bขนาด\u200bใหญ่ '
         'ส่งผล\u200bให้\u200bคะแนน\u200bรวม ', False, False, 14),
        ('S', False, True, 14),
        ('total', False, False, 14, False, True),
        (' ยังคง\u200bมีค่า\u200bเป็น\u200bบวก ระบบ\u200bจึง\u200bแจ้งเตือน\u200bว่า\u200bการ\u200bปรับตัว\u200bลง\u200bใน\u200bกรอบ\u200bเวลา\u200bสั้น\u200bเป็น\u200bเพียง\u200bการ\u200bพักตัว (Pullback) ภายใน\u200bโครงสร้าง\u200bใหญ่ '
         'ซึ่ง\u200bช่วย\u200bป้องกัน\u200bไม่ให้\u200bนักลงทุน\u200bเปิด\u200bสถานะ\u200bเทรด\u200bสวนทาง\u200bกับ\u200bแนวโน้ม\u200bหลัก\u200bของ\u200bตลาด', False, False, 14),
    ],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY,
    first_line_indent=Inches(0.25)
)

idx_54_old, p_54_old = find_p_by_prefix('5.4 การ\u200bอภิปราย\u200bผล')
set_paragraph_runs(
    p_54_old,
    [('6. อภิปราย\u200bผล\u200bและ\u200bข้อจำกัด\u200bของ\u200bงานวิจัย', True, False, 14)],
    align=WD_ALIGN_PARAGRAPH.CENTER,
    first_line_indent=Inches(0),
    keep_with_next=True,
    space_before=Pt(4)
)
p_s6_disc = doc.paragraphs[idx_54_old + 1]
set_paragraph_runs(
    p_s6_disc,
    [(
        '\tระบบ\u200bที่\u200bพัฒนา\u200bขึ้น\u200bช่วย\u200bเปลี่ยน\u200bกระบวนการ\u200bวิเคราะห์\u200bจาก\u200bการ\u200bตีความ\u200bตาม\u200bความรู้สึก\u200bส่วนบุคคล '
        'ให้\u200bเป็น\u200bการ\u200bวิเคราะห์\u200bเชิง\u200bระบบ\u200bที่\u200bมี\u200bความ\u200bสม่ำเสมอ\u200bและ\u200bมี\u200bมาตรฐาน\u200bเดียวกัน อย่างไรก็ตาม ระบบ\u200bยังมี\u200bข้อจำกัด\u200bด้าน\u200bความล่าช้า (Lagging) '
        'ใน\u200bการ\u200bยืนยัน\u200bจุด\u200bสวิง\u200bซึ่ง\u200bต้อง\u200bรอ\u200bแท่ง\u200bเทียน\u200bล่วงหน้า N แท่ง\u200bปิด\u200bสมบูรณ์ และ\u200bอัลกอริทึม\u200bพึ่งพา\u200bข้อมูล\u200bราคา\u200bใน\u200bอดีต\u200bเป็น\u200bหลัก '
        'จึง\u200bอาจ\u200bเกิด\u200bสัญญาณ\u200bหลอก (False Breakout) ได้\u200bใน\u200bช่วง\u200bที่\u200bมี\u200bข่าวสาร\u200bเศรษฐกิจ\u200bสำคัญ\u200bที่\u200bสร้าง\u200bความผันผวน\u200bรุนแรง\u200bแบบ\u200bฉับพลัน',
        False, False, 14
    )],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
)

_, p_s6_old = find_p_by_prefix('6. สรุป\u200bผล')
set_paragraph_runs(
    p_s6_old,
    [('7. สรุป\u200bผล\u200bการทดลอง', True, False, 14)],
    align=WD_ALIGN_PARAGRAPH.CENTER,
    first_line_indent=Inches(0),
    keep_with_next=True,
    space_before=Pt(4)
)

_, p_s6_body = find_p_by_prefix('งานวิจัย\u200bนี้\u200bได้\u200bพัฒนา\u200bเครื่องมือ\u200bอัตโนมัติ')
conclusion_text = (
    'งานวิจัย\u200bนี้\u200bได้\u200bพัฒนา\u200bเครื่องมือ\u200bอัตโนมัติ\u200bด้วย\u200bภาษา Python สำหรับ\u200bการ\u200bวิเคราะห์\u200bและ\u200bแสดงผล\u200bโครงสร้าง\u200bตลาด\u200bการเงิน\u200bตาม\u200bแนวคิด Smart Money Concepts '
    'ได้\u200bสำเร็จ\u200bตาม\u200bวัตถุประสงค์ โดย\u200bบูรณาการ\u200bอัลกอริทึม\u200bเชิง\u200bกฎเกณฑ์ การ\u200bวิเคราะห์\u200bพหุ\u200bกรอบ\u200bเวลา\u200bแบบ\u200bถ่วง\u200bน้ำหนัก '
    'และ\u200bการ\u200bแสดงผล\u200bบน\u200bกราฟ\u200bเชิง\u200bโต้ตอบ\u200bไว้\u200bด้วยกัน\u200bอย่าง\u200bเป็นระบบ ช่วย\u200bประหยัดเวลา ขจัด\u200bความผิดพลาด\u200bจาก\u200bการ\u200bตีเส้น\u200bกราฟ\u200bด้วย\u200bตนเอง '
    'และ\u200bลด\u200bอคติ\u200bทาง\u200bอารมณ์\u200bของ\u200bนักลงทุน จากการ\u200bทดสอบ\u200bและ\u200bประเมิน\u200bความพึงพอใจ\u200bกับ\u200bผู้ใช้งาน\u200bจริง\u200bจำนวน 5 คน พบ\u200bว่า\u200bผู้ใช้งาน\u200bมี\u200bความพึงพอใจ\u200bโดยรวม\u200bอยู่\u200bใน\u200bระดับ\u200bดีมาก '
    'โดย\u200bมี\u200bค่าเฉลี่ย\u200bรวม\u200bเท่ากับ 4.52 จาก 5 ยืนยัน\u200bว่า\u200bระบบ\u200bสามารถ\u200bสนับสนุน\u200bการตัดสินใจ\u200bลงทุน\u200bและ\u200bเป็น\u200bสื่อ\u200bการเรียนรู้\u200bเชิงประจักษ์\u200bได้\u200bอย่าง\u200bมีประสิทธิภาพ'
)
set_paragraph_runs(
    p_s6_body,
    [(conclusion_text, False, False, 14)],
    align=WD_ALIGN_PARAGRAPH.THAI_JUSTIFY,
    first_line_indent=Inches(0.25)
)

_, p_ref_hdr = find_p_by_prefix('เอกสารอ้างอิง')
p_ref_hdr.paragraph_format.first_line_indent = Inches(0)
p_ref_hdr.paragraph_format.space_before = Pt(4)

# Normalize paragraph indentation, alignment, and explicit Bold/Regular/Italic/Size across the entire document:
for i_p, p in enumerate(doc.paragraphs):
    txt = p.text
    s_txt = txt.replace('\u200b', '').strip()
    if txt.startswith('\t'):
        for r in p.runs:
            if r.text.startswith('\t'):
                r.text = r.text.lstrip('\t')
                break
        p.paragraph_format.first_line_indent = Inches(0.25)
        p.paragraph_format.left_indent = Inches(0)
    elif re.match(r'^\[\d+\]', s_txt):
        p.paragraph_format.left_indent = Inches(0)
        p.paragraph_format.first_line_indent = Inches(0)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.name = 'TH SarabunPSK'
            r.font.size = Pt(14)
            r.bold = False
    elif re.match(r'^[1-7]\.\s', s_txt) or s_txt == 'เอกสารอ้างอิง':
        # Main Section Heading: 14pt, Bold, Regular (not italic), Centered, first_line_indent=0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.left_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            r.font.name = 'TH SarabunPSK'
            r.font.size = Pt(14)
            r.bold = True
            r.italic = False
    elif re.match(r'^[1-7]\.[1-9]\s', s_txt):
        # Sub-section Heading: 14pt, Bold + Italic, Left-aligned, first_line_indent=0
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.left_indent = Inches(0)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            r.font.name = 'TH SarabunPSK'
            r.font.size = Pt(14)
            r.bold = True
            r.italic = True
    elif re.match(r'^(1|2|3|4)\)\s', s_txt):
        p.paragraph_format.first_line_indent = Inches(0.25)
        p.paragraph_format.left_indent = Inches(0)
        p.alignment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
    elif i_p >= 14 and s_txt and not s_txt.startswith(('ตาราง ', 'ภาพที่ ')) and 'm:oMath' not in p._p.xml:
        # Remaining body paragraphs in Sections 1-7: 14pt, Regular (bold=False), THAI_JUSTIFY, first_line_indent=0.25
        p.alignment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
        p.paragraph_format.first_line_indent = Inches(0.25)
        p.paragraph_format.left_indent = Inches(0)
        for r in p.runs:
            r.font.name = 'TH SarabunPSK'
            if r.font.size is None:
                r.font.size = Pt(14)
            if r.bold is None:
                r.bold = False
            if r.italic is None:
                r.italic = False

while len(doc.paragraphs) > 0 and doc.paragraphs[-1].text.strip() == '' and 'w:drawing' not in doc.paragraphs[-1]._p.xml and 'w:sectPr' not in doc.paragraphs[-1]._p.xml:
    doc.paragraphs[-1]._p.getparent().remove(doc.paragraphs[-1]._p)

TMP_DOCX = r'e:\Project\smc-backtest-backend\tmp_aucc2026.docx'
doc.save(TMP_DOCX)

with zipfile.ZipFile(TMP_DOCX, 'r') as zin:
    with zipfile.ZipFile(WORK_DOCX, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/media/image1.png':
                with open(NEW_FIG1, 'rb') as f_img:
                    zout.writestr(item, f_img.read())
            else:
                zout.writestr(item, zin.read(item.filename))

os.remove(TMP_DOCX)
print("Successfully generated:", WORK_DOCX)
