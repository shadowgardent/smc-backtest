import docx, sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

backup_file = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx'
doc = docx.Document(backup_file)

# Parse P40 using ET
root = ET.fromstring(doc.paragraphs[40]._element.xml)
# namespaces
ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'
}

# Find all m:t
for t in root.findall('.//m:t', ns):
    print('m:t text:', repr(t.text))
