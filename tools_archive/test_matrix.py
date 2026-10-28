import docx, re, sys, os, subprocess
from docx.oxml import parse_xml

sys.stdout.reconfigure(encoding='utf-8')

backup_file = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx'
doc = docx.Document(backup_file)

# Let's inspect the OMML of P40
p40_xml = doc.paragraphs[40]._element.xml

# In P40, the matrix has 2 rows (m:mr).
# Let's see how m:mr is structured.
print("P40 m:mr count:", p40_xml.count('<m:mr>'))
