import fitz
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.pdf")

# Page 4 check (Table 3 and Section 5.1)
print("=== PAGE 4 TEXT PREVIEW ===")
p4_text = doc[3].get_text()
for line in p4_text.split("\n"):
    if any(k in line for k in ["4.08", "0.41", "5.1", "ตาราง 3", "ความพึงพอใจ"]):
        print(" ", line.strip())

# Page 5 check (Conclusion)
print("\n=== PAGE 5 TEXT PREVIEW ===")
p5_text = doc[4].get_text()
for line in p5_text.split("\n"):
    if any(k in line for k in ["4.08", "สรุปผล", "ความพึงพอใจ"]):
        print(" ", line.strip())
