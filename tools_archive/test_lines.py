import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("google_sheet_eval.csv", "r", encoding="utf-8") as f:
    lines = [l for l in f.readlines() if l.strip()]

print(f"Total non-empty lines: {len(lines)}")
for idx, l in enumerate(lines):
    parts = l.split(",")
    ts = parts[0].strip().replace('"', '')
    name = parts[1].strip().replace('"', '') if len(parts) > 1 else ""
    print(f"Index {idx} (Line {idx+1}): Timestamp={ts} | Name={name}")
