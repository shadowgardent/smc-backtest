import docx, sys
sys.stdout.reconfigure(encoding='utf-8')

backup_file = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Backup.docx'
doc = docx.Document(backup_file)

# Let's check P48 in backup
p48 = doc.paragraphs[48]
print("P48 runs count:", len(p48.runs))
for r_idx, r in enumerate(p48.runs):
    print(f"  Run {r_idx}: {repr(r.text)}")
