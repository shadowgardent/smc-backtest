import win32com.client
import os

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

in_path = os.path.abspath(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx")
out_path = os.path.abspath(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Checked.pdf")

doc = word.Documents.Open(in_path)
doc.SaveAs(out_path, FileFormat=17) # 17 = wdFormatPDF
doc.Close()
word.Quit()

print("Successfully converted to PDF:", out_path)
