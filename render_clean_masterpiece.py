from PIL import Image, ImageDraw, ImageFont
import math

# High-resolution canvas: 2400 x 1350 px (16:9 widescreen, fits full A4 page width)
W, H = 2400, 1350
img = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Fonts
def get_font(size, bold=False):
    candidates = (
        ["C:/Windows/Fonts/tahomabd.ttf", "C:/Windows/Fonts/leelawdb.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold else
        ["C:/Windows/Fonts/tahoma.ttf", "C:/Windows/Fonts/leelawUI.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

f_title = get_font(38, bold=True)
f_hdr = get_font(32, bold=True)
f_sub = get_font(24, bold=True)
f_node_title = get_font(27, bold=True)
f_node_desc = get_font(24, bold=False)
f_badge = get_font(20, bold=True)

# Color Palette (Elegant Professional Modern Purple & Slate)
c_bg = (255, 255, 255)
c_outer_border = (203, 213, 225)
c_container_bg = (248, 250, 252)
c_container_border = (148, 163, 184)
c_container_hdr = (241, 245, 249)

c_node_bg = (243, 238, 255)        # Light lavender
c_node_border = (139, 92, 246)      # Purple border
c_node_title = (76, 29, 149)        # Deep purple title
c_node_desc = (30, 41, 59)          # Slate dark body

c_user_bg = (238, 242, 255)         # Indigo tinted
c_user_border = (99, 102, 241)

c_line = (100, 116, 139)            # Slate 500 line
c_arrow = (37, 99, 235)             # Blue 600 arrowhead

# 1. Outer Frame & Header Banner
draw.rounded_rectangle([25, 20, W - 25, H - 20], radius=24, outline=c_outer_border, width=3, fill=(255, 255, 255))

# Top Title Bar
draw.rounded_rectangle([50, 40, W - 50, 125], radius=16, fill=(30, 41, 59))
title_text = "ขั้นตอนการทำงานและการไหลของข้อมูลในระบบ (System Process & Data Flow)"
bb = draw.textbbox((0, 0), title_text, font=f_title)
draw.text(((W - (bb[2] - bb[0])) // 2, 82 - (bb[3] - bb[1]) // 2), title_text, font=f_title, fill=(255, 255, 255))

# Helpers
def draw_card(x1, y1, x2, y2, title, desc="", badge="", bg=c_node_bg, border=c_node_border):
    # Shadow
    draw.rounded_rectangle([x1+4, y1+4, x2+4, y2+4], radius=14, fill=(226, 232, 240))
    # Main Box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=14, fill=bg, outline=border, width=3)
    
    # Badge (Optional step number)
    if badge:
        bb_b = draw.textbbox((0, 0), badge, font=f_badge)
        bw = bb_b[2] - bb_b[0] + 16
        draw.rounded_rectangle([x1 + 14, y1 + 12, x1 + 14 + bw, y1 + 38], radius=6, fill=border)
        draw.text((x1 + 22, y1 + 14), badge, font=f_badge, fill=(255, 255, 255))
        tx = x1 + 22 + bw + 8
    else:
        tx = x1 + 20

    # Title & Desc
    if desc:
        draw.text((tx, y1 + 14), title, font=f_node_title, fill=c_node_title)
        draw.text((x1 + 20, y1 + 54), desc, font=f_node_desc, fill=c_node_desc)
    else:
        bb_t = draw.textbbox((0, 0), title, font=f_node_title)
        draw.text((x1 + (x2 - x1 - (bb_t[2] - bb_t[0])) // 2, y1 + (y2 - y1 - (bb_t[3] - bb_t[1])) // 2),
                  title, font=f_node_title, fill=c_node_title)

def draw_arrow_h(x1, x2, y, color=c_line, arrow_color=c_arrow, width=4):
    draw.line([(x1, y), (x2, y)], fill=color, width=width)
    ah = 14
    if x2 > x1:
        draw.polygon([(x2, y), (x2 - ah*1.6, y - ah), (x2 - ah*1.6, y + ah)], fill=arrow_color)
    else:
        draw.polygon([(x2, y), (x2 + ah*1.6, y - ah), (x2 + ah*1.6, y + ah)], fill=arrow_color)

def draw_arrow_v(x, y1, y2, color=c_line, arrow_color=c_arrow, width=4):
    draw.line([(x, y1), (x, y2)], fill=color, width=width)
    ah = 14
    if y2 > y1:
        draw.polygon([(x, y2), (x - ah, y2 - ah*1.6), (x + ah, y2 - ah*1.6)], fill=arrow_color)
    else:
        draw.polygon([(x, y2), (x - ah, y2 + ah*1.6), (x + ah, y2 + ah*1.6)], fill=arrow_color)

def draw_elbow(pts, color=c_line, arrow_color=c_arrow, width=4):
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        is_last = (i == len(pts) - 2)
        if is_last:
            draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
            ah = 14
            if x2 > x1:
                draw.polygon([(x2, y2), (x2 - ah*1.6, y2 - ah), (x2 - ah*1.6, y2 + ah)], fill=arrow_color)
            elif x2 < x1:
                draw.polygon([(x2, y2), (x2 + ah*1.6, y2 - ah), (x2 + ah*1.6, y2 + ah)], fill=arrow_color)
            elif y2 > y1:
                draw.polygon([(x2, y2), (x2 - ah, y2 - ah*1.6), (x2 + ah, y2 - ah*1.6)], fill=arrow_color)
            elif y2 < y1:
                draw.polygon([(x2, y2), (x2 - ah, y2 + ah*1.6), (x2 + ah, y2 + ah*1.6)], fill=arrow_color)
        else:
            draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

# ==============================================================================
# 3-COLUMN ARCHITECTURE LAYOUT
# ==============================================================================

# Column 1: Client & User (Left: x = 70 .. 500)
# Column 2: Core Analysis Engine (Middle Box: x = 560 .. 1840)
# Column 3: Output & Dashboard (Right: x = 1900 .. 2330)

# --- MIDDLE CONTAINER: ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม ---
cx1, cy1, cx2, cy2 = 560, 160, 1840, 1150
# Container background & header
draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=20, fill=c_container_bg, outline=c_container_border, width=3)
draw.rounded_rectangle([cx1, cy1, cx2, cy1 + 65], radius=20, fill=c_container_hdr)
draw.rectangle([cx1, cy1 + 35, cx2, cy1 + 65], fill=c_container_hdr)
draw.line([(cx1, cy1 + 65), (cx2, cy1 + 65)], fill=c_container_border, width=3)

# Container Title
ct_text = "ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม (Core SMC Analysis Engine)"
bb_ct = draw.textbbox((0, 0), ct_text, font=f_hdr)
draw.text((cx1 + 30, cy1 + 32 - (bb_ct[3] - bb_ct[1])//2), ct_text, font=f_hdr, fill=(30, 41, 59))

# --- MIDDLE BOX CARDS (2 Columns inside container: Col A x=600..1180, Col B x=1220..1800) ---
card_w = 560
card_h = 100

# Row 1: Input (Col A) -> Data Fetching (Col B)
r1_y = 265
draw_card(600, r1_y, 600 + card_w, r1_y + card_h, "Input Parameter", "ระบุสัญลักษณ์คู่เงิน (Symbol) & กรอบเวลา (Timeframe)", badge="01")
draw_card(1220, r1_y, 1220 + card_w, r1_y + card_h, "Data Fetching API", "ดึงข้อมูลราคาแท่งเทียนดิบ OHLCV ผ่าน MT5 API", badge="02")

# Row 2: Swing High/Low (Col A) -> BOS / CHoCH / OB (Col B)
r2_y = 485
draw_card(600, r2_y, 600 + card_w, r2_y + card_h, "Swing Processing", "ประมวลผลหาจุดยอดคลื่นและก้นคลื่น (Swing High / Low)", badge="03")
draw_card(1220, r2_y, 1220 + card_w, r2_y + card_h, "Structure & Zones", "ตรวจจับการเบรกทะลุ BOS, การเปลี่ยนแนวโน้ม CHoCH & โซน OB", badge="04")

# Row 3: Multi-Timeframe Engine (Col A) -> Scoring System (Col B)
r3_y = 705
draw_card(600, r3_y, 600 + card_w, r3_y + card_h, "Multi-Timeframe Engine", "สแกนโครงสร้างและข้อมูลแนวโน้ม 7 กรอบเวลา (W1 ถึง M5)", badge="05")
draw_card(1220, r3_y, 1220 + card_w, r3_y + card_h, "Scoring System", "คำนวณถ่วงน้ำหนักหาทิศทางเทรนด์หลัก (Stotal Score)", badge="06")

# --- LEFT COLUMN: USER (x = 70 .. 500) ---
ux1, uy1, ux2, uy2 = 70, 240, 500, 450
draw.rounded_rectangle([ux1+4, uy1+4, ux2+4, uy2+4], radius=20, fill=(226, 232, 240))
draw.rounded_rectangle([ux1, uy1, ux2, uy2], radius=20, fill=c_user_bg, outline=c_user_border, width=4)
# User Circle/Avatar
u_cx, u_cy = (ux1 + ux2) // 2, uy1 + 80
draw.ellipse([u_cx - 45, u_cy - 45, u_cx + 45, u_cy + 45], fill=(199, 210, 254), outline=c_user_border, width=3)
# User text
draw.text((u_cx - 85, uy1 + 140), "User / นักเทรด", font=get_font(28, bold=True), fill=(49, 46, 129))
draw.text((ux1 + 35, uy1 + 185), "• เลือกคู่เงิน & Timeframe ที่ต้องการ\n• ตรวจสอบสัญญาณและโซนราคา", font=f_node_desc, fill=(51, 65, 85))

# --- RIGHT COLUMN: WEB APP & OUTPUT (x = 1900 .. 2330) ---
# Card 07: Web Application (y = 485 .. 620)
wx1, wy1, wx2, wy2 = 1900, 485, 2330, 610
draw_card(wx1, wy1, wx2, wy2, "Web Application", "เรนเดอร์กราฟอินเทอร์แอคทีฟ (TradingView)\nพร้อมเลเยอร์กล่องราคา SMC บน HTML5 Canvas", badge="07")

# Card 08: Output & Dashboard (y = 705 .. 840)
ox1, oy1, ox2, oy2 = 1900, 705, 2330, 830
draw_card(ox1, oy1, ox2, oy2, "Output & Dashboard", "แสดงผลกราฟ SMC ครบวงจร, แดชบอร์ดสรุปผล\nคะแนนแนวโน้ม 7 TF และตารางประเมินสัญญาณ", badge="08")

# ==============================================================================
# CLEAN, TANGLE-FREE CONNECTING ARROWS (ZERO OVERLAPS!)
# ==============================================================================

# 1. User -> Input (Step 01)
draw_arrow_h(500, 600, r1_y + card_h//2, color=c_line, arrow_color=c_arrow)

# 2. Input -> Data Fetching (Step 01 -> 02)
draw_arrow_h(600 + card_w, 1220, r1_y + card_h//2, color=c_line, arrow_color=c_arrow)

# 3. Data Fetching -> Swing Processing (Step 02 -> 03)
# Smooth S-curve routing between Col B Row 1 to Col A Row 2
mid_y1 = (r1_y + card_h + r2_y) // 2 # 420
draw_elbow([(1220 + card_w//2, r1_y + card_h),
            (1220 + card_w//2, mid_y1),
            (600 + card_w//2, mid_y1),
            (600 + card_w//2, r2_y)], color=c_line, arrow_color=c_arrow)

# 4. Swing Processing -> Structure & Zones (Step 03 -> 04)
draw_arrow_h(600 + card_w, 1220, r2_y + card_h//2, color=c_line, arrow_color=c_arrow)

# 5. Structure & Zones -> Web App (Direct Line to Right: Step 04 -> 07)
draw_arrow_h(1220 + card_w, wx1, r2_y + card_h//2, color=c_line, arrow_color=c_arrow)

# 6. Structure & Zones -> Multi-TF Engine (Step 04 -> 05)
# Smooth routing between Col B Row 2 to Col A Row 3
mid_y2 = (r2_y + card_h + r3_y) // 2 # 640
draw_elbow([(1220 + card_w//3, r2_y + card_h),
            (1220 + card_w//3, mid_y2),
            (600 + card_w//2, mid_y2),
            (600 + card_w//2, r3_y)], color=c_line, arrow_color=c_arrow)

# 7. Multi-TF Engine -> Scoring System (Step 05 -> 06)
draw_arrow_h(600 + card_w, 1220, r3_y + card_h//2, color=c_line, arrow_color=c_arrow)

# 8. Scoring System -> Web App (Step 06 -> 07)
# Route from Scoring (1220+card_w, r3_y + card_h//2) -> up to Web App bottom
draw_elbow([(1220 + card_w, r3_y + card_h//2),
            (wx1 + (wx2-wx1)//3, r3_y + card_h//2),
            (wx1 + (wx2-wx1)//3, wy2)], color=c_line, arrow_color=c_arrow)

# 9. Web App -> Output & Dashboard (Step 07 -> 08)
draw_arrow_v(wx1 + (wx2-wx1)//2, wy2, oy1, color=c_line, arrow_color=c_arrow)

# 10. Output & Dashboard -> User (Loop back along the bottom!)
# From Output bottom (ox1 + (ox2-ox1)//2, oy2) -> down to y=1240 -> left to x=285 -> up to User bottom (285, uy2)
draw_elbow([(ox1 + (ox2-ox1)//2, oy2),
            (ox1 + (ox2-ox1)//2, 1240),
            ((ux1 + ux2)//2, 1240),
            ((ux1 + ux2)//2, uy2)], color=c_line, arrow_color=c_arrow)

# Bottom Label for return loop
draw.rounded_rectangle([W//2 - 240, 1215, W//2 + 240, 1265], radius=8, fill=(255, 255, 255), outline=c_line, width=2)
draw.text((W//2 - 215, 1225), "ผลการวิเคราะห์โครงสร้างตลาด & สัญญาณเทรด ส่งกลับสู่ผู้ใช้งาน", font=f_badge, fill=(51, 65, 85))

out_clean = "e:/Project/smc-backtest-backend/SMC_System_Flow_Clean.png"
out_downloads = "C:/Users/ONEST/Downloads/SMC_System_Flow_Clean.png"
img.save(out_clean, dpi=(300, 300))
img.save(out_downloads, dpi=(300, 300))
print("Successfully generated clean masterpiece layout!")
