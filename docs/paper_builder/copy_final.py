import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

src_docx = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx'
src_pdf = 'เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.pdf'

fixed_docx = r'C:\Users\ONEST\Downloads\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Fixed.docx'
fixed_pdf = r'C:\Users\ONEST\Downloads\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2_Fixed.pdf'

shutil.copyfile(src_docx, fixed_docx)
shutil.copyfile(src_pdf, fixed_pdf)
print(f"Copied to: {fixed_docx}")
print(f"Copied to: {fixed_pdf}")

# Try copying to original name in case Word is closed
orig_docx = r'C:\Users\ONEST\Downloads\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.docx'
orig_pdf = r'C:\Users\ONEST\Downloads\เครื่องมือวิเคราะห์และแสดงผลโครงสร้างตลาดการเงินด้วยอัลกอริทึม_SMC_Revised_AUC2.pdf'
try:
    shutil.copyfile(src_docx, orig_docx)
    print(f"Overwrote: {orig_docx}")
except Exception as e:
    print(f"Note: Could not overwrite {orig_docx} (file is currently open in Word). Used _Fixed instead.")

try:
    shutil.copyfile(src_pdf, orig_pdf)
    print(f"Saved: {orig_pdf}")
except Exception as e:
    print(f"Note: Could not overwrite {orig_pdf}")
