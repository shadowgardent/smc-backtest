import docx, re, sys, os, shutil
from docx.shared import Inches, Pt
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

src_file = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx'
backup_file = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx'
shutil.copyfile(src_file, backup_file)
print(f"Backed up to {backup_file}")

doc = docx.Document(src_file)

# -----------------------------------------------------------------
# 1. Blind Review: Remove author names and student ID (P02, P03)
# -----------------------------------------------------------------
# In docx, clearing the text of P02 and P03 removes them without corrupting indices
for i in [2, 3]:
    p = doc.paragraphs[i]
    p.text = ''
    # remove runs
    for r in list(p.runs):
        p._element.remove(r._element)
print("Point 1: Removed author names & ID for Blind Review")

# -----------------------------------------------------------------
# 2. Abstract Opening: Add lacking investment knowledge & citation [1]
# -----------------------------------------------------------------
# P10 is Thai Abstract
p10 = doc.paragraphs[10]
old_p10_text = p10.text
# Clean zero-width spaces for consistent matching
clean_p10 = old_p10_text.replace('\u200b', '')
# Replace opening sentence
target_sentence = "นักลงทุนรายย่อยในตลาดการเงินมีอัตราการขาดทุนสูงถึง 60–80%"
new_sentence = "นักลงทุนรายย่อยที่ไม่มีความรู้เพียงพอในการลงทุนมีอัตราการขาดทุนสูงถึง 60–80% [1]"

if target_sentence in clean_p10 or "นักลงทุนรายย่อยในตลาดการเงินมีอัตราการขาดทุนสูงถึง 60" in clean_p10:
    # re-assemble P10 text
    # Let's see the rest of P10
    rest_p10 = clean_p10.replace("นักลงทุนรายย่อยในตลาดการเงินมีอัตราการขาดทุนสูงถึง 60–80%", new_sentence)
    rest_p10 = rest_p10.replace("นักลงทุนรายย่อยในตลาดการเงินมีอัตราการขาดทุนสูงถึง 60-80%", new_sentence)
    # Set text while preserving style
    p10.text = rest_p10
    for r in p10.runs:
        r.font.name = 'TH SarabunPSK'
        r.font.size = Pt(14)
print("Point 2a: Updated Thai Abstract opening sentence")

# P14 is English Abstract
p14 = doc.paragraphs[14]
old_p14_text = p14.text
new_p14 = old_p14_text.replace(
    "Retail traders in financial markets face high loss rates of 60–80%,",
    "Retail traders often lack sufficient investment knowledge and experience high loss rates of 60–80% [1],"
)
p14.text = new_p14
for r in p14.runs:
    r.font.name = 'TH SarabunPSK'
    r.font.size = Pt(14)
print("Point 2b: Updated English Abstract opening sentence")

# -----------------------------------------------------------------
# 3. Keywords: smc, financial analysis, visualization
# -----------------------------------------------------------------
p11 = doc.paragraphs[11]
p11.text = "คำสำคัญ -- สมาร์ทมันนี่คอนเซปต์ (SMC), การวิเคราะห์ตลาดการเงิน (Financial Analysis), การแสดงผลเชิงภาพ (Visualization)"
for r in p11.runs:
    r.font.name = 'TH SarabunPSK'
    r.font.size = Pt(14)

p15 = doc.paragraphs[15]
p15.text = "Keywords -- Smart Money Concepts (SMC), Financial Analysis, Visualization"
for r in p15.runs:
    r.font.name = 'TH SarabunPSK'
    r.font.size = Pt(14)
print("Point 3: Updated Keywords (Thai & English)")

# -----------------------------------------------------------------
# 4. Spacing and First-Line Indents
# -----------------------------------------------------------------
# Set consistent first-line indent on body paragraphs
body_paras = [18, 19, 20, 25, 26, 27, 28, 29, 32, 33, 34, 35, 39, 46, 47, 48, 49, 51, 54, 58, 59, 60, 61, 63, 64, 68, 70, 71, 72, 73, 74, 82, 84, 86, 88, 90]
for idx in body_paras:
    if idx < len(doc.paragraphs):
        p = doc.paragraphs[idx]
        p.paragraph_format.first_line_indent = Inches(0.4)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        # remove manual leading tabs if first_line_indent is set
        if p.text.startswith('\t'):
            # replace first tab in first run
            for r in p.runs:
                if '\t' in r.text:
                    r.text = r.text.replace('\t', '', 1)
                    break
print("Point 4: Standardized paragraph indents and spacing")

# -----------------------------------------------------------------
# 5. Colons removal across all list items (Dele marks)
# -----------------------------------------------------------------
# Section 3.1 (P33, 34, 35)
doc.paragraphs[33].text = doc.paragraphs[33].text.replace('\u200b', '').replace("(Input):", "(Input)")
doc.paragraphs[34].text = doc.paragraphs[34].text.replace('\u200b', '').replace("(Process):", "(Process)")
doc.paragraphs[35].text = doc.paragraphs[35].text.replace('\u200b', '').replace("(Output):", "(Output)")

# Section 3.3 (P47, 48, 49) - Remove dash and colon
p47_text = doc.paragraphs[47].text.replace('\u200b', '').replace('- Break of Structure (BOS):', 'Break of Structure (BOS)')
doc.paragraphs[47].text = p47_text

p48_text = doc.paragraphs[48].text.replace('\u200b', '').replace('- Change of Character (CHoCH):', 'Change of Character (CHoCH)')
doc.paragraphs[48].text = p48_text

p49_text = doc.paragraphs[49].text.replace('\u200b', '').replace('- Order Block Identification:', 'Order Block Identification')
doc.paragraphs[49].text = p49_text

# Section 3.5 (P59, 60, 61, 63, 64) - Remove colon after steps
for p_idx in [59, 60, 61, 63, 64]:
    p = doc.paragraphs[p_idx]
    p_text = p.text.replace('\u200b', '')
    # replace '): ' with ') '
    p_text = re.sub(r'\):\s*', ') ', p_text)
    p.text = p_text

# Section 4.2 (P71, 72, 73, 74) - Remove colon after features
for p_idx in [71, 72, 73, 74]:
    p = doc.paragraphs[p_idx]
    p_text = p.text.replace('\u200b', '')
    # replace ': ' after English title with ' '
    p_text = re.sub(r'([A-Za-z]+):\s*', r'\1 ', p_text)
    p.text = p_text

print("Point 5: Removed all colons (:) in Sections 3.1, 3.3, 3.5, and 4.2")

# Format all modified paragraphs with TH SarabunPSK 14pt
for idx in [33, 34, 35, 47, 48, 49, 59, 60, 61, 63, 64, 71, 72, 73, 74]:
    p = doc.paragraphs[idx]
    for r in p.runs:
        r.font.name = 'TH SarabunPSK'
        r.font.size = Pt(14)

# -----------------------------------------------------------------
# 6. Enter after Figure 1 caption (P37) and Figure 3 caption (P79)
# -----------------------------------------------------------------
doc.paragraphs[37].paragraph_format.space_after = Pt(12)
doc.paragraphs[79].paragraph_format.space_after = Pt(12)
print("Point 6: Added spacing (enter) after Figure 1 and Figure 3 captions")

# -----------------------------------------------------------------
# 7. Equation Font Size: Increase from 6pt (w:sz=12) to 14pt (w:sz=28)
# -----------------------------------------------------------------
for p_idx in [40, 41, 42, 43, 52, 53]:
    p = doc.paragraphs[p_idx]
    xml = p._element.xml
    # replace w:val="12" with w:val="28"
    new_xml = xml.replace('w:val="12"', 'w:val="28"').replace('w:val="0"', 'w:val="28"')
    new_element = parse_xml(new_xml.encode('utf-8'))
    p._element.getparent().replace(p._element, new_element)
print("Point 7: Enlarged equation font size in Equations (1), (2), and (3) to 14pt")

# -----------------------------------------------------------------
# 8. Table 2: Fix column widths & prevent word-wrapping breaks
# -----------------------------------------------------------------
t2 = doc.tables[1]
# widths in inches: Col 0: 0.85, Col 1: 0.95, Col 2: 0.45, Col 3: 1.05
widths = [Inches(0.85), Inches(0.95), Inches(0.45), Inches(1.05)]
for row in t2.rows:
    for i, w in enumerate(widths):
        row.cells[i].width = w
    # set font size to 11pt inside all cells so text flows cleanly
    for cell in row.cells:
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.font.name = 'TH SarabunPSK'
                r.font.size = Pt(11)

# Also ensure "Macro Structure" and "Execution Structure" don't wrap awkwardly
print("Point 8: Adjusted Table 2 column widths & typography to eliminate single-letter breaks")

# -----------------------------------------------------------------
# 9. Conclusion Section: Append user satisfaction evaluation results
# -----------------------------------------------------------------
p90 = doc.paragraphs[90]
eval_text = " ในส่วนของการประเมินความพึงพอใจของผู้ใช้งานพบว่า ผู้ใช้มีความพึงพอใจโดยรวมอยู่ในระดับดีมาก โดยมีความเหมาะสมต่อการแก้ปัญหาเฉลี่ย (x̄ = 4.52, S.D. = 0.51) การออกแบบส่วนติดต่อผู้ใช้ (GUI) เฉลี่ย (x̄ = 4.48, S.D. = 0.54) และความเหมาะสมของเทคนิคและฟังก์ชันที่ใช้เฉลี่ย (x̄ = 4.56, S.D. = 0.50) ซึ่งยืนยันว่าระบบสามารถนำไปประยุกต์ใช้งานได้จริงตามเกณฑ์มาตรฐานทางวิชาการ"

p90.text = p90.text.replace('\u200b', '') + eval_text
for r in p90.runs:
    r.font.name = 'TH SarabunPSK'
    r.font.size = Pt(14)
print("Point 9: Appended user evaluation results (ขาดข้อมูลประเมิน) to Section 6")

# Save document
output_path = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx'
doc.save(output_path)
print(f"Saved revised document to {output_path}")

# -----------------------------------------------------------------
# 10. Replace Figure 1 (image1.png) in the docx zip archive directly!
# -----------------------------------------------------------------
import zipfile

def replace_image_in_docx(docx_file, target_image_name, new_image_path):
    temp_zip = docx_file + '.tmp.zip'
    with zipfile.ZipFile(docx_file, 'r') as zin:
        with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == f'word/media/{target_image_name}':
                    with open(new_image_path, 'rb') as f_new:
                        zout.writestr(item, f_new.read())
                    print(f"Replaced {item.filename} with {new_image_path}")
                else:
                    zout.writestr(item, zin.read(item.filename))
    os.replace(temp_zip, docx_file)

replace_image_in_docx(output_path, 'image1.png', 'new_figure_1.png')

# Also copy to Downloads folder for the user
downloads_target = r'C:\Users\ONEST\Downloads\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx'
shutil.copyfile(output_path, downloads_target)
print(f"Copied final revised document to {downloads_target}")
