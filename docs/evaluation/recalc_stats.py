import csv
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("google_sheet_latest.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    raw_rows = list(reader)

headers = raw_rows[0]
data_rows = [r for r in raw_rows[1:] if len(r) >= 21 and r[1].strip()]

print(f"Total respondents count: {len(data_rows)}")

# Print each respondent
for idx, r in enumerate(data_rows):
    print(f"\nPerson {idx+1}:")
    print(f"  Name: {r[1]}")
    print(f"  Gender: {r[2]}, Age: {r[3]}, Occ: {r[4]}, Exp: {r[5]}")
    scores_1 = [int(x) for x in r[6:11]]
    scores_2 = [int(x) for x in r[11:16]]
    scores_3 = [int(x) for x in r[16:21]]
    print(f"  Cat 1 (1.1-1.5): {scores_1} -> Avg = {np.mean(scores_1):.2f}")
    print(f"  Cat 2 (2.1-2.5): {scores_2} -> Avg = {np.mean(scores_2):.2f}")
    print(f"  Cat 3 (3.1-3.5): {scores_3} -> Avg = {np.mean(scores_3):.2f}")
    print(f"  Total Avg = {np.mean(scores_1 + scores_2 + scores_3):.2f}")
    fb = r[21].strip()
    if fb: print(f"  Feedback: '{fb}'")

# Scores matrix: (5, 15)
scores = []
for r in data_rows:
    row_scores = [float(x) for x in r[6:21]]
    scores.append(row_scores)

scores_mat = np.array(scores)

q_titles = headers[6:21]

print("\n================== DETAILED STATISTICAL AUDIT ==================")
def interpret(val):
    if val >= 4.51: return "มากที่สุด (ดีมาก)"
    elif val >= 3.51: return "มาก (ดี)"
    elif val >= 2.51: return "ปานกลาง"
    elif val >= 1.51: return "น้อย"
    else: return "น้อยที่สุด"

# Question-by-Question
print("\n--- 15 QUESTIONS (Mean & SD) ---")
for q_idx in range(15):
    q_vals = scores_mat[:, q_idx]
    m = np.mean(q_vals)
    s = np.std(q_vals, ddof=1) # sample standard deviation
    print(f"Q{q_idx+1:02d} ({q_titles[q_idx]}): Scores={list(q_vals.astype(int))} | Mean={m:.2f}, SD={s:.2f} -> {interpret(m)}")

# Categories
cat1 = scores_mat[:, 0:5]
cat2 = scores_mat[:, 5:10]
cat3 = scores_mat[:, 10:15]

cat1_mean = np.mean(cat1)
cat1_sd_all = np.std(cat1, ddof=1)
cat1_person_avgs = np.mean(cat1, axis=1)
cat1_sd_person = np.std(cat1_person_avgs, ddof=1)

cat2_mean = np.mean(cat2)
cat2_sd_all = np.std(cat2, ddof=1)
cat2_person_avgs = np.mean(cat2, axis=1)
cat2_sd_person = np.std(cat2_person_avgs, ddof=1)

cat3_mean = np.mean(cat3)
cat3_sd_all = np.std(cat3, ddof=1)
cat3_person_avgs = np.mean(cat3, axis=1)
cat3_sd_person = np.std(cat3_person_avgs, ddof=1)

overall_mean = np.mean(scores_mat)
overall_sd_all = np.std(scores_mat, ddof=1)
overall_person_avgs = np.mean(scores_mat, axis=1)
overall_sd_person = np.std(overall_person_avgs, ddof=1)

print("\n--- CATEGORY SUMMARY ---")
print(f"ด้านที่ 1 ฟังก์ชันและประโยชน์ (1.1-1.5): Mean={cat1_mean:.2f}, SD={cat1_sd_person:.2f} (item SD={cat1_sd_all:.2f}) -> {interpret(cat1_mean)}")
print(f"ด้านที่ 2 ส่วนติดต่อผู้ใช้ UI/UX (2.1-2.5): Mean={cat2_mean:.2f}, SD={cat2_sd_person:.2f} (item SD={cat2_sd_all:.2f}) -> {interpret(cat2_mean)}")
print(f"ด้านที่ 3 ความถูกต้องอัลกอริทึม (3.1-3.5): Mean={cat3_mean:.2f}, SD={cat3_sd_person:.2f} (item SD={cat3_sd_all:.2f}) -> {interpret(cat3_mean)}")
print(f"\nภาพรวมทั้งหมด: Mean={overall_mean:.2f}, SD={overall_sd_person:.2f} (item SD={overall_sd_all:.2f}) -> {interpret(overall_mean)}")
