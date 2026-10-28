import csv
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("google_sheet_eval.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    raw_rows = list(reader)

# Filter out empty rows
headers = raw_rows[0]
data_rows = [r for r in raw_rows[1:] if len(r) >= 21 and r[1].strip()]

print(f"Total valid respondents: {len(data_rows)}")

# Demographics
names = [r[1] for r in data_rows]
genders = [r[2] for r in data_rows]
ages = [int(r[3]) for r in data_rows if r[3].strip()]
occupations = [r[4] for r in data_rows]
experiences = [r[5] for r in data_rows]

print("\n--- DEMOGRAPHICS ---")
print(f"Genders: Male={genders.count('ชาย')}, Female={genders.count('หญิง')}")
print(f"Ages: Min={min(ages)}, Max={max(ages)}, Mean={np.mean(ages):.1f}")
print("Occupations:")
for occ in set(occupations):
    print(f"  - {occ}: {occupations.count(occ)} คน")
print("Experiences:")
for exp in set(experiences):
    print(f"  - {exp}: {experiences.count(exp)} คน")

# Score columns: 6 to 20 (15 questions)
scores = []
for r in data_rows:
    row_scores = [float(x) for x in r[6:21]]
    scores.append(row_scores)

scores_mat = np.array(scores) # shape: (10, 15)

q_titles = headers[6:21]

print("\n--- QUESTIONS STATISTICS (Mean & S.D.) ---")
def interpret(score):
    if score >= 4.51: return "มากที่สุด (ดีมาก)"
    elif score >= 3.51: return "มาก (ดี)"
    elif score >= 2.51: return "ปานกลาง"
    elif score >= 1.51: return "น้อย"
    else: return "น้อยที่สุด"

for q_idx in range(15):
    q_scores = scores_mat[:, q_idx]
    mean_val = np.mean(q_scores)
    sd_val = np.std(q_scores, ddof=1) # sample SD
    print(f"Q{q_idx+1:02d} ({q_titles[q_idx][:40]}...): Mean={mean_val:.2f}, SD={sd_val:.2f} -> {interpret(mean_val)}")

# Category Statistics
# Cat 1: Q1-Q5 (indices 0..4)
cat1 = scores_mat[:, 0:5]
cat1_mean = np.mean(cat1)
cat1_sd = np.std(np.mean(cat1, axis=1), ddof=1)
# or pool SD
print(f"\nด้านที่ 1 ประโยชน์และฟังก์ชันการทำงาน (1.1-1.5): Mean={cat1_mean:.2f}, SD={np.std(cat1, ddof=1):.2f} -> {interpret(cat1_mean)}")

# Cat 2: Q6-Q10 (indices 5..9)
cat2 = scores_mat[:, 5:10]
cat2_mean = np.mean(cat2)
print(f"ด้านที่ 2 ส่วนติดต่อผู้ใช้และ UI/UX (2.1-2.5): Mean={cat2_mean:.2f}, SD={np.std(cat2, ddof=1):.2f} -> {interpret(cat2_mean)}")

# Cat 3: Q11-Q15 (indices 10..14)
cat3 = scores_mat[:, 10:15]
cat3_mean = np.mean(cat3)
print(f"ด้านที่ 3 ความถูกต้องและประสิทธิภาพอัลกอริทึม (3.1-3.5): Mean={cat3_mean:.2f}, SD={np.std(cat3, ddof=1):.2f} -> {interpret(cat3_mean)}")

# Overall
total_mean = np.mean(scores_mat)
total_sd = np.std(scores_mat, ddof=1)
print(f"\nภาพรวมทั้งหมด 15 ข้อ: Mean={total_mean:.2f}, SD={total_sd:.2f} -> {interpret(total_mean)}")

# Qualitative feedback
print("\n--- ข้อเสนอแนะเพิ่มเติม ---")
for r in data_rows:
    fb = r[21].strip()
    if fb and fb != "-":
        print(f"- {r[1]} ({r[4]}): \"{fb}\"")
