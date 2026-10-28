import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("google_sheet_eval.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
for i, r in enumerate(rows):
    print(f"Row {i:02d} ({len(r)} cols): {r}")
