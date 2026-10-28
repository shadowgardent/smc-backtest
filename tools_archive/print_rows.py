import docx, re, sys
sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document('เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx')
xml = doc.paragraphs[40]._element.xml
mrs = re.findall(r'<m:mr>.*?</m:mr>', xml, re.DOTALL)
for idx, mr in enumerate(mrs):
    texts = re.findall(r'<[mw]:t[^>]*>(.*?)</[mw]:t>', mr, re.DOTALL)
    print(f'Row {idx}: {" ".join(texts)}')
