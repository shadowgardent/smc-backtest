import docx, re, sys, subprocess
from docx.oxml import parse_xml

sys.stdout.reconfigure(encoding='utf-8')

backup_file = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx'
doc = docx.Document(backup_file)

# Let's inspect P40 XML to see how to remove the ∀i,j∈[1,N] part from the equation
p40 = doc.paragraphs[40]
xml = p40._element.xml

# In P40 XML:
# Find the part with ∀i,j∈[1,N]
# Let's search for '∀' or '1,N'
print("P40 contains ∀:", '∀' in xml)
print("P40 contains 1,N:", '1,N' in xml)
