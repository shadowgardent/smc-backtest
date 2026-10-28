import docx, re, sys, subprocess, pymupdf
from docx.oxml import parse_xml

sys.stdout.reconfigure(encoding='utf-8')

backup_file = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx'
doc = docx.Document(backup_file)

# Let's inspect P40 XML around '∀'
p40 = doc.paragraphs[40]
xml = p40._element.xml
pos = xml.find('∀')
print("XML segment around forall:")
print(xml[pos-500:pos+800])
