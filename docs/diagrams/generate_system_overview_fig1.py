from PIL import Image, ImageDraw, ImageFont
import shutil

W, H = 2400, 1846
img = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

def get_font(size, bold=False):
    candidates = (
        ["C:/Windows/Fonts/leelawdb.ttf", "C:/Windows/Fonts/tahomabd.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold else
        ["C:/Windows/Fonts/leelawUI.ttf", "C:/Windows/Fonts/tahoma.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

f_title = get_font(48, bold=True)
f_box_hdr = get_font(38, bold=True)
f_box_sub = get_font(31, bold=True)
f_body = get_font(28, bold=False)
f_body_b = get_font(28, bold=True)
f_arrow = get_font(27, bold=True)
f_small = get_font(25, bold=False)

def draw_centered_text(box_x1, box_x2, y, text, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((box_x1 + box_x2 - tw) // 2, y), text, font=font, fill=fill)

# Outer subtle frame
draw.rounded_rectangle([20, 20, W - 20, H - 20], radius=28, outline=(203, 213, 225), width=4, fill=(250, 252, 255))

# Header banner
draw.rounded_rectangle([52, 46, W - 52, 144], radius=18, fill=(30, 58, 138), outline=(23, 37, 84), width=3)
draw_centered_text(52, W - 52, 70, "ภาพรวมสถาปัตยกรรมและการเชื่อมต่อของระบบ (System Overview)", f_title, (255, 255, 255))

def draw_arrow_h(x1, x2, y, color, label_top="", label_bot="", direction="right"):
    draw.line([(x1, y), (x2, y)], fill=color, width=7)
    ah = 17
    if direction in ("right", "both"):
        draw.polygon([(x2, y), (x2 - ah * 1.5, y - ah), (x2 - ah * 1.5, y + ah)], fill=color)
    if direction in ("left", "both"):
        draw.polygon([(x1, y), (x1 + ah * 1.5, y - ah), (x1 + ah * 1.5, y + ah)], fill=color)
    cx = (x1 + x2) // 2
    if label_top:
        bb = draw.textbbox((0, 0), label_top, font=f_arrow)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        draw.rounded_rectangle([cx - tw // 2 - 14, y - th - 26, cx + tw // 2 + 14, y - 10], radius=8, fill=(255, 255, 255), outline=color, width=2)
        draw.text((cx - tw // 2, y - th - 22), label_top, font=f_arrow, fill=color)
    if label_bot:
        bb = draw.textbbox((0, 0), label_bot, font=f_small)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        draw.text((cx - tw // 2, y + 12), label_bot, font=f_small, fill=(51, 65, 85))

def draw_arrow_v(x, y1, y2, color, label="", direction="down"):
    draw.line([(x, y1), (x2 := x, y2)], fill=color, width=7)
    ah = 17
    if direction in ("down", "both"):
        draw.polygon([(x, y2), (x - ah, y2 - ah * 1.5), (x + ah, y2 - ah * 1.5)], fill=color)
    if direction in ("up", "both"):
        draw.polygon([(x, y1), (x - ah, y1 + ah * 1.5), (x + ah, y1 + ah * 1.5)], fill=color)
    cy = (y1 + y2) // 2
    if label:
        bb = draw.textbbox((0, 0), label, font=f_arrow)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        draw.rounded_rectangle([x - tw // 2 - 16, cy - th // 2 - 10, x + tw // 2 + 16, cy + th // 2 + 10], radius=8, fill=(255, 255, 255), outline=color, width=2)
        draw.text((x - tw // 2, cy - th // 2 - 4), label, font=f_arrow, fill=color)

# ==============================================================================
# TOP TIER: (Left) ผู้ใช้งาน (User) <---> (Right) ส่วนติดต่อผู้ใช้บนเว็บ (Frontend)
# ==============================================================================

# 1. USER BOX (Left Top: x=52..620, y=195..735)
ux1, uy1, ux2, uy2 = 52, 195, 620, 735
draw.rounded_rectangle([ux1, uy1, ux2, uy2], radius=22, fill=(239, 246, 255), outline=(37, 99, 235), width=5)
draw.rounded_rectangle([ux1, uy1, ux2, uy1 + 82], radius=22, fill=(37, 99, 235))
draw.rectangle([ux1, uy1 + 48, ux2, uy1 + 82], fill=(37, 99, 235))
draw_centered_text(ux1, ux2, uy1 + 18, "ผู้ใช้งาน (User / Trader)", f_box_hdr, (255, 255, 255))

# Draw User + Monitor Icon inside User Box
ic_cx, ic_cy = (ux1 + ux2) // 2, uy1 + 185
draw.ellipse([ic_cx - 90, ic_cy - 60, ic_cx - 24, ic_cy + 6], fill=(59, 130, 246), outline=(29, 78, 216), width=4)
draw.chord([ic_cx - 118, ic_cy + 12, ic_cx + 4, ic_cy + 108], start=180, end=360, fill=(59, 130, 246), outline=(29, 78, 216), width=4)
draw.rounded_rectangle([ic_cx + 15, ic_cy - 42, ic_cx + 120, ic_cy + 38], radius=8, fill=(255, 255, 255), outline=(29, 78, 216), width=4)
draw.line([(ic_cx + 28, ic_cy + 14), (ic_cx + 52, ic_cy - 10), (ic_cx + 76, ic_cy + 4), (ic_cx + 106, ic_cy - 24)], fill=(22, 163, 74), width=5)
draw.polygon([(ic_cx + 5, ic_cy + 42), (ic_cx + 130, ic_cy + 42), (ic_cx + 140, ic_cy + 58), (ic_cx - 5, ic_cy + 58)], fill=(148, 163, 184), outline=(29, 78, 216), width=3)

user_lines = [
    "• เลือกคู่เงิน (Symbol เช่น EURUSD)",
    "• เลือกกรอบเวลา (Timeframe)",
    "• ตรวจสอบกราฟโครงสร้าง SMC",
    "  และตารางสรุปแนวโน้ม 7 กรอบเวลา",
    "• ใช้ประกอบการตัดสินใจลงทุน"
]
yy = uy1 + 282
for ln in user_lines:
    draw.text((ux1 + 28, yy), ln, font=f_body, fill=(15, 23, 42))
    yy += 44

# Arrows between User (x=620) and Frontend (x=1040) -> 420px wide gap!
draw_arrow_h(628, 1032, 375, (29, 78, 216), label_top="1) ส่วนรับข้อมูล (Input)", label_bot="เลือกคู่เงินและกรอบเวลา", direction="right")
draw_arrow_h(628, 1032, 565, (5, 150, 105), label_top="3) ส่วนแสดงผล (Output)", label_bot="กราฟโครงสร้าง & ตารางคะแนน", direction="left")

# 2. FRONTEND BOX (Right Top: x=1040..2348, y=195..735)
fx1, fy1, fx2, fy2 = 1040, 195, 2348, 735
draw.rounded_rectangle([fx1, fy1, fx2, fy2], radius=22, fill=(240, 253, 244), outline=(5, 150, 105), width=5)
draw.rounded_rectangle([fx1, fy1, fx2, fy1 + 82], radius=22, fill=(5, 150, 105))
draw.rectangle([fx1, fy1 + 48, fx2, fy1 + 82], fill=(5, 150, 105))
draw_centered_text(fx1, fx2, fy1 + 18, "ส่วนติดต่อผู้ใช้บนเว็บ (Frontend Web Application)", f_box_hdr, (255, 255, 255))

# Card A: Interactive Charting
c1x1, c1y1, c1x2, c1y2 = fx1 + 30, fy1 + 108, fx1 + 638, fy2 - 26
draw.rounded_rectangle([c1x1, c1y1, c1x2, c1y2], radius=16, fill=(255, 255, 255), outline=(16, 185, 129), width=3)
draw.rounded_rectangle([c1x1 + 16, c1y1 + 14, c1x2 - 16, c1y1 + 102], radius=10, fill=(209, 250, 229))
draw_centered_text(c1x1, c1x2, c1y1 + 20, "TradingView Lightweight Charts", f_box_sub, (6, 95, 70))
draw_centered_text(c1x1, c1x2, c1y1 + 58, "& HTML5 Canvas Overlay", f_body_b, (5, 150, 105))

fe_left_lines = [
    "• แสดงกราฟแท่งเทียนเชิงโต้ตอบ",
    "• วาดจุด Swing High / Swing Low",
    "• วาดเส้นโครงสร้าง BOS และ CHoCH",
    "• ไฮไลต์โซนราคา Order Block (OB)",
    "  และช่องว่างราคา (FVG) อัตโนมัติ"
]
yy = c1y1 + 122
for ln in fe_left_lines:
    draw.text((c1x1 + 22, yy), ln, font=f_body, fill=(15, 23, 42))
    yy += 44

# Card B: Multi-Timeframe Dashboard
c2x1, c2y1, c2x2, c2y2 = fx1 + 668, fy1 + 108, fx2 - 30, fy2 - 26
draw.rounded_rectangle([c2x1, c2y1, c2x2, c2y2], radius=16, fill=(255, 255, 255), outline=(16, 185, 129), width=3)
draw.rounded_rectangle([c2x1 + 16, c2y1 + 14, c2x2 - 16, c2y1 + 102], radius=10, fill=(209, 250, 229))
draw_centered_text(c2x1, c2x2, c2y1 + 20, "Multi-Timeframe Dashboard", f_box_sub, (6, 95, 70))
draw_centered_text(c2x1, c2x2, c2y1 + 58, "(Angular Web Interface)", f_body_b, (5, 150, 105))

fe_right_lines = [
    "• แสดงสถานะแนวโน้มทั้ง 7 กรอบเวลา",
    "  (W1, D1, H4, H1, M30, M15, M5)",
    "• แสดงคะแนนถ่วงน้ำหนักสุทธิ (Stotal)",
    "• สรุปทิศทางตลาดภาพรวมในหน้าจอเดียว",
    "• รับคำสั่งตั้งค่าจากผู้ใช้แบบเรียลไทม์"
]
yy = c2y1 + 122
for ln in fe_right_lines:
    draw.text((c2x1 + 22, yy), ln, font=f_body, fill=(15, 23, 42))
    yy += 44

# ==============================================================================
# VERTICAL ARROWS BETWEEN FRONTEND (TOP) AND BACKEND (BOTTOM RIGHT)
# ==============================================================================
draw_arrow_v(1345, 742, 952, (79, 70, 229), label="HTTP Request (คู่เงิน, กรอบเวลา)", direction="down")
draw_arrow_v(2040, 742, 952, (5, 150, 105), label="JSON Response (พิกัด SMC & คะแนน)", direction="up")

# ==============================================================================
# BOTTOM TIER: (Left) MetaTrader 5 Data Source <---> (Right) Backend SMC Engine
# ==============================================================================

# 3. MARKET DATA SOURCE BOX (Left Bottom: x=52..620, y=960..1775)
mx1, my1, mx2, my2 = 52, 960, 620, 1775
draw.rounded_rectangle([mx1, my1, mx2, my2], radius=22, fill=(255, 251, 235), outline=(217, 119, 6), width=5)
draw.rounded_rectangle([mx1, my1, mx2, my1 + 82], radius=22, fill=(217, 119, 6))
draw.rectangle([mx1, my1 + 48, mx2, my1 + 82], fill=(217, 119, 6))
draw_centered_text(mx1, mx2, my1 + 18, "แหล่งข้อมูลตลาด (Market Data)", f_box_hdr, (255, 255, 255))

# Candlestick Icon inside MT5 box
mcx, mcy = (mx1 + mx2) // 2, my1 + 175
draw.rounded_rectangle([mcx - 125, mcy - 58, mcx + 125, mcy + 58], radius=14, fill=(255, 255, 255), outline=(217, 119, 6), width=4)
candles = [
    (mcx - 80, mcy - 32, mcy + 32, mcy - 14, mcy + 18, (22, 163, 74)),
    (mcx - 28, mcy - 42, mcy + 22, mcy - 28, mcy + 8, (220, 38, 38)),
    (mcx + 24, mcy - 28, mcy + 40, mcy - 4, mcy + 26, (22, 163, 74)),
    (mcx + 76, mcy - 45, mcy + 18, mcy - 36, mcy - 4, (22, 163, 74)),
]
for cx_c, w_top, w_bot, b_top, b_bot, col in candles:
    draw.line([(cx_c, w_top), (cx_c, w_bot)], fill=col, width=4)
    draw.rectangle([cx_c - 13, b_top, cx_c + 13, b_bot], fill=col)

draw_centered_text(mx1, mx2, my1 + 258, "MetaTrader 5 (MT5) Terminal", f_box_sub, (180, 83, 9))
mt5_lines = [
    "• เชื่อมต่อข้อมูลราคาตลาดการเงิน",
    "• ดึงข้อมูลแท่งเทียนย้อนหลัง (OHLCV):",
    "  - ราคาเปิด (Open) และราคาปิด (Close)",
    "  - ราคาสูงสุด (High) และต่ำสุด (Low)",
    "  - ปริมาณการซื้อขาย (Tick Volume)",
    "• ครอบคลุมข้อมูลทั้ง 7 กรอบเวลา:",
    "  W1, D1, H4, H1, M30, M15 และ M5"
]
yy = my1 + 318
for ln in mt5_lines:
    draw.text((mx1 + 28, yy), ln, font=f_body, fill=(15, 23, 42))
    yy += 45

# Arrows between MT5 (x=620) and Backend (x=1040) -> 420px wide gap!
draw_arrow_h(628, 1032, 1260, (217, 119, 6), label_top="ดึงข้อมูลราคา (MT5 API)", label_bot="ระบุคู่เงินและกรอบเวลา", direction="left")
draw_arrow_h(628, 1032, 1485, (217, 119, 6), label_top="ชุดข้อมูลแท่งเทียน (OHLCV)", label_bot="ส่งกลับข้อมูลราคาทั้ง 7 กรอบเวลา", direction="right")

# 4. BACKEND SERVER BOX (Right Bottom: x=1040..2348, y=960..1775)
bx1, by1, bx2, by2 = 1040, 960, 2348, 1775
draw.rounded_rectangle([bx1, by1, bx2, by2], radius=22, fill=(238, 242, 255), outline=(67, 56, 202), width=5)
draw.rounded_rectangle([bx1, by1, bx2, by1 + 82], radius=22, fill=(67, 56, 202))
draw.rectangle([bx1, by1 + 48, bx2, by1 + 82], fill=(67, 56, 202))
draw_centered_text(bx1, bx2, by1 + 18, "2) ส่วนประมวลผลกลาง (Backend Server : Python FastAPI)", f_box_hdr, (255, 255, 255))

# Sub-box 1 inside Backend: SMC Rule-based Algorithm Engine
s1x1, s1y1, s1x2, s1y2 = bx1 + 30, by1 + 108, bx1 + 638, by2 - 28
draw.rounded_rectangle([s1x1, s1y1, s1x2, s1y2], radius=16, fill=(255, 255, 255), outline=(99, 102, 241), width=3)
draw.rounded_rectangle([s1x1 + 16, s1y1 + 14, s1x2 - 16, s1y1 + 98], radius=10, fill=(224, 231, 255))
draw_centered_text(s1x1, s1x2, s1y1 + 18, "อัลกอริทึมวิเคราะห์โครงสร้าง", f_box_sub, (49, 46, 129))
draw_centered_text(s1x1, s1x2, s1y1 + 56, "(SMC Rule-based Engine)", f_body_b, (67, 56, 202))

be_left_lines = [
    "• จัดเตรียมข้อมูลด้วย Pandas & NumPy",
    "• ตรวจจับจุด Swing High (SH) และ",
    "  Swing Low (SL) ด้วยหน้าต่าง N แท่ง",
    "  (Look-back & Look-forward)",
    "• ตรวจจับการเบรกโครงสร้าง (BOS)",
    "  และการเปลี่ยนแนวโน้ม (CHoCH)",
    "• ระบุโซน Order Block (OB) อัตโนมัติ",
    "  และตรวจสอบสถานะการทดสอบโซน",
    "  (Mitigation)"
]
yy = s1y1 + 116
for ln in be_left_lines:
    draw.text((s1x1 + 22, yy), ln, font=f_body, fill=(15, 23, 42))
    yy += 43

# Arrow connecting Sub-box 1 -> Sub-box 2 inside Backend
draw_arrow_h(s1x2 + 4, bx1 + 664, (s1y1 + s1y2) // 2, (67, 56, 202), direction="right")

# Sub-box 2 inside Backend: Multi-Timeframe Engine & Scoring System
s2x1, s2y1, s2x2, s2y2 = bx1 + 668, by1 + 108, bx2 - 30, by2 - 28
draw.rounded_rectangle([s2x1, s2y1, s2x2, s2y2], radius=16, fill=(255, 255, 255), outline=(99, 102, 241), width=3)
draw.rounded_rectangle([s2x1 + 16, s2y1 + 14, s2x2 - 16, s2y1 + 98], radius=10, fill=(224, 231, 255))
draw_centered_text(s2x1, s2x2, s2y1 + 18, "Multi-Timeframe Engine", f_box_sub, (49, 46, 129))
draw_centered_text(s2x1, s2x2, s2y1 + 56, "& Scoring System", f_body_b, (67, 56, 202))

be_right_lines = [
    "• ประมวลผลโครงสร้างตลาดพร้อมกัน",
    "  ทั้ง 7 กรอบเวลา (W1 ถึง M5)",
    "• กำหนดค่าน้ำหนักความสำคัญ (wk)",
    "  ตามลำดับชั้นของกรอบเวลา",
    "• คำนวณคะแนนทิศทางสุทธิ (Stotal)",
    "  ตามสมการ (3) เพื่อคัดกรองสัญญาณ",
    "  ที่ขัดแย้งกันระหว่างกรอบเวลา",
    "• จัดรูปแบบผลลัพธ์เป็นพิกัด JSON",
    "  ส่งกลับไปยังส่วนแสดงผลบนเว็บ"
]
yy = s2y1 + 116
for ln in be_right_lines:
    draw.text((s2x1 + 22, yy), ln, font=f_body, fill=(15, 23, 42))
    yy += 43

out_path = r"e:\Project\smc-backtest-backend\new_figure_1.png"
img.save(out_path, "PNG")
shutil.copyfile(out_path, r"C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d\new_figure_1.png")
print("Saved refined System Overview Figure 1 to:", out_path)
