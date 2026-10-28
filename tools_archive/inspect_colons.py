import sys, os, pymupdf
from PIL import Image
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect each crop in detail
crops = [
    # Page 3
    ('p3_0_(2)', 'หน้า 3: ท้ายประโยค สมการ (1) และ (2):'),
    ('p3_1_(BOS)', 'หน้า 3: - Break of Structure (BOS):'),
    ('p3_2_(CHoCH)', 'หน้า 3: - Change of Character (CHoCH):'),
    ('p3_3_Identification', 'หน้า 3: - Order Block Identification:'),
    ('p3_4_(3)', 'หน้า 3: ท้ายประโยค สมการ (3):'),
    # Page 4
    ('p4_0_(1', 'หน้า 4: (-1:'),
    ('p4_1_0', 'หน้า 4: 0:'),
    ('p4_2_1', 'หน้า 4: 1: แนวโน้มขาขึ้น)'),
    ('p4_3_', 'หน้า 4: มีลำดับขั้นตอนดังนี้:'),
    ('p4_4_', 'หน้า 4: ขั้นตอนที่ 1 (การรับข้อมูลนำเข้า):'),
    ('p4_5_', 'หน้า 4: ขั้นตอนที่ 2 (การตรวจจับจุดสวิง):'),
    ('p4_6_', 'หน้า 4: ขั้นตอนที่ 3 (การประเมินการเบรกโครงสร้างราคา):'),
    ('p4_7_Block', 'หน้า 4: ขั้นตอนที่ 4 (การระบุโซน Order Block):'),
    ('p4_8_', 'หน้า 4: ขั้นตอนที่ 5 (การส่งออกผลลัพธ์):'),
    ('p4_9_Charting', 'หน้า 4: 1) Interactive Charting:'),
    # Page 5
    ('p5_0_Overlay', 'หน้า 5: 2) Automated Structure Overlay:'),
    ('p5_1_Highlighting', 'หน้า 5: 3) Price Zone Highlighting:'),
    ('p5_2_Dashboard', 'หน้า 5: 4) Multi-Timeframe Status Dashboard:'),
]

for prefix, desc in crops:
    # find file matching prefix
    matches = [f for f in os.listdir('colon_crops') if f.startswith(prefix.split('_')[0] + '_' + prefix.split('_')[1])]
    if matches:
        f = matches[0]
        img = Image.open(os.path.join('colon_crops', f))
        arr = np.array(img)
        blue_mask = (arr[:, :, 2] > 120) & (arr[:, :, 2] > arr[:, :, 0] + 30)
        cnt = np.sum(blue_mask)
        print(f"{desc:<50} | Blue px: {cnt} | File: {f}")
