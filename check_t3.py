import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx")
print("Paragraph 66-70:")
for i in range(66, min(76, len(doc.paragraphs))):
    print(f"P{i}: {doc.paragraphs[i].text}")

table3 = doc.tables[2] # Table 3 is index 2
print("\nTable 3 Content:")
for row in table3.rows:
    row_text = [c.text.strip().replace("\n", " ") for c in row.cells]
    print(row_text)
