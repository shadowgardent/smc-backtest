import requests
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

sheet_id = "15_QNMleInWe0B3X4Xx-YMA-rEVA69Gu4iWgFCUtNDLY"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

resp = requests.get(url, timeout=10)
with open("google_sheet_latest.csv", "w", encoding="utf-8") as f:
    f.write(resp.text)

with open("google_sheet_latest.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Total raw rows in sheet: {len(rows)}")
for i, r in enumerate(rows):
    if any(cell.strip() for cell in r):
        print(f"Row {i:02d} (len={len(r)}): Timestamp='{r[0]}' | Name='{r[1]}' | Gender='{r[2]}' | Age='{r[3]}' | Occ='{r[4]}' | Exp='{r[5]}'")
