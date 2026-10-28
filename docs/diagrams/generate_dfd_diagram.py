from PIL import Image, ImageDraw, ImageFont
import os
import shutil

W, H = 2600, 1460
img = Image.new("RGB", (W, H), (248, 250, 252))
draw = ImageDraw.Draw(img)

def get_font(size, bold=False):
    candidates = (
        ["C:/Windows/Fonts/leelawdb.ttf", "C:/Windows/Fonts/tahomabd.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold else
        ["C:/Windows/Fonts/leelawUI.ttf", "C:/Windows/Fonts/tahoma.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

f_title = get_font(42, bold=True)
f_sub = get_font(24, bold=False)
f_box_hdr = get_font(25, bold=True)
f_box_sub = get_font(20, bold=False)
f_bullet = get_font(19, bold=False)
f_store = get_font(21, bold=True)
f_store_sub = get_font(17, bold=False)
f_flow = get_font(18, bold=True)
f_flow_sub = get_font(16, bold=False)
f_legend = get_font(21, bold=True)

# Outer Border
draw.rounded_rectangle([20, 20, W - 20, H - 20], radius=24, outline=(203, 213, 225), width=3, fill=(255, 255, 255))

# Header Banner
draw.rounded_rectangle([50, 40, W - 50, 160], radius=16, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
draw.text((80, 62), "Data Flow Diagram Level 1 (DFD Level 1) - SMC Analysis System", font=f_title, fill=(255, 255, 255))
draw.text((80, 118), "แผนภาพการไหลของข้อมูลระดับที่ 1: การรับคำขอ, ดึงข้อมูล MT5, ประมวลผล SMC Engine, และส่งผลลัพธ์สู่หน้าจอแสดงผล", font=f_sub, fill=(148, 163, 184))

# Helper: Draw External Entity (Double rectangle)
def draw_entity(x1, y1, x2, y2, title, subtitle, color=(37, 99, 235)):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=14, fill=(239, 246, 255), outline=color, width=3)
    draw.rounded_rectangle([x1 + 6, y1 + 6, x2 - 6, y2 - 6], radius=10, outline=color, width=1)
    draw.text(((x1 + x2) // 2, y1 + 35), title, font=f_box_hdr, fill=(15, 23, 42), anchor="mm")
    draw.text(((x1 + x2) // 2, y1 + 75), subtitle, font=f_box_sub, fill=(51, 65, 85), anchor="mm")

# Helper: Draw Process (Rounded circle/rect with header bar)
def draw_process(x1, y1, x2, y2, p_num, title, subtitle, bullet1="", bullet2="", color=(16, 185, 129)):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=18, fill=(240, 253, 244), outline=color, width=3)
    # Header bar with process number
    draw.rounded_rectangle([x1, y1, x2, y1 + 42], radius=18, fill=color)
    draw.rectangle([x1, y1 + 22, x2, y1 + 42], fill=color)
    draw.text(((x1 + x2) // 2, y1 + 21), f"Process {p_num}", font=get_font(19, bold=True), fill=(255, 255, 255), anchor="mm")
    draw.text(((x1 + x2) // 2, y1 + 72), title, font=f_box_hdr, fill=(6, 78, 59), anchor="mm")
    draw.text(((x1 + x2) // 2, y1 + 104), subtitle, font=f_box_sub, fill=(15, 118, 110), anchor="mm")
    if bullet1:
        draw.text((x1 + 20, y1 + 132), f"• {bullet1}", font=f_bullet, fill=(30, 41, 59))
    if bullet2:
        draw.text((x1 + 20, y1 + 160), f"• {bullet2}", font=f_bullet, fill=(30, 41, 59))

# Helper: Draw Data Store (Open-ended parallel lines)
def draw_data_store(x1, y1, x2, y2, store_id, name, desc=""):
    draw.rectangle([x1, y1, x2, y2], fill=(255, 251, 235))
    draw.line([(x1, y1), (x2, y1)], fill=(217, 119, 6), width=3)
    draw.line([(x1, y2), (x2, y2)], fill=(217, 119, 6), width=3)
    draw.line([(x1 + 55, y1), (x1 + 55, y2)], fill=(217, 119, 6), width=2)
    draw.text((x1 + 28, (y1 + y2) // 2), store_id, font=f_store, fill=(180, 83, 9), anchor="mm")
    draw.text((x1 + 68, y1 + 22), name, font=f_store, fill=(120, 53, 15))
    if desc:
        draw.text((x1 + 68, y1 + 50), desc, font=f_store_sub, fill=(146, 64, 14))

# Helper: Directed Flow Arrow
def draw_flow_h(x1, x2, y, label="", sub="", direction="right", color=(59, 130, 246)):
    draw.line([(x1, y), (x2, y)], fill=color, width=3)
    ah = 11
    if direction == "right":
        draw.polygon([(x2, y), (x2 - ah * 1.5, y - ah), (x2 - ah * 1.5, y + ah)], fill=color)
    else:
        draw.polygon([(x1, y), (x1 + ah * 1.5, y - ah), (x1 + ah * 1.5, y + ah)], fill=color)
    cx = (x1 + x2) // 2
    if label:
        bb = draw.textbbox((0, 0), label, font=f_flow)
        tw = bb[2] - bb[0]
        draw.rounded_rectangle([cx - tw//2 - 6, y - 28, cx + tw//2 + 6, y - 6], radius=5, fill=(255, 255, 255), outline=color, width=1)
        draw.text((cx, y - 17), label, font=f_flow, fill=color, anchor="mm")
    if sub:
        draw.text((cx, y + 14), sub, font=f_flow_sub, fill=(100, 116, 139), anchor="mm")

def draw_flow_v(x, y1, y2, label="", sub="", direction="down", color=(59, 130, 246)):
    draw.line([(x, y1), (x, y2)], fill=color, width=3)
    ah = 11
    if direction == "down":
        draw.polygon([(x, y2), (x - ah, y2 - ah * 1.5), (x + ah, y2 - ah * 1.5)], fill=color)
    else:
        draw.polygon([(x, y1), (x - ah, y1 + ah * 1.5), (x + ah, y1 + ah * 1.5)], fill=color)
    cy = (y1 + y2) // 2
    if label:
        bb = draw.textbbox((0, 0), label, font=f_flow)
        tw = bb[2] - bb[0]
        draw.rounded_rectangle([x - tw//2 - 6, cy - 13, x + tw//2 + 6, cy + 13], radius=5, fill=(255, 255, 255), outline=color, width=1)
        draw.text((x, cy), label, font=f_flow, fill=color, anchor="mm")

# ==============================================================================
# 5 COLUMNS COORDINATES
# ==============================================================================
# Col 1: Entities E1, E2 (x = 60 .. 420)
# Col 2: Processes 1.0, 2.0 (x = 560 .. 960)
# Col 3: Processes 6.0, 3.0 & Stores D1, D2 (x = 1100 .. 1520)
# Col 4: Processes 4.0, 5.0 (x = 1660 .. 2080)
# Col 5: Stores D3, D4 (x = 2200 .. 2540)

# E1: User / Trader (Top Left)
draw_entity(60, 230, 420, 360, "E1: ผู้ใช้งาน (User / Trader)", "นักลงทุนส่งคำขอ & ดูผลลัพธ์", (37, 99, 235))

# E2: MetaTrader 5 (Bottom Left)
draw_entity(60, 840, 420, 970, "E2: MetaTrader 5 (MT5)", "แหล่งข้อมูลราคาตลาดการเงิน", (217, 119, 6))

# Process 1.0: Request Validation Layer (Col 2 Top)
draw_process(560, 230, 960, 420, "1.0", "รับคำขอและตรวจสอบค่า", "Request Validation Layer", "รับคู่เงิน (Symbol) & กรอบเวลา", "ตรวจสอบผ่าน FastAPI / Pydantic", (37, 99, 235))

# Process 2.0: Data Extraction & Feed (Col 2 Bottom)
draw_process(560, 810, 920, 1000, "2.0", "ดึงข้อมูลราคาตลาด (Feed)", "Market Data Extraction", "เรียก copy_rates_from_pos()", "แปลงเป็น Pandas DataFrame 7 TF", (14, 165, 233))

# Process 6.0: Visualization & Dashboard (Col 3 Top)
draw_process(1120, 230, 1540, 420, "6.0", "เรนเดอร์กราฟและแดชบอร์ด", "Visualization & Presentation", "ส่งออก JSON ให้ Lightweight Charts", "แสดงผลสถานะแนวโน้มบน Angular SPA", (236, 72, 153))

# Process 3.0: Core SMC Engine (Col 3 Middle)
draw_process(1120, 520, 1540, 710, "3.0", "ตรวจจับจุดสวิงและโครงสร้าง", "SMC Rule-based Engine", "หา Swing High/Low (Look-back)", "ตรวจจับสัญญาณ BOS & CHoCH", (16, 185, 129))

# Store D1: ohlcv_candles (Col 3 Bottom A)
draw_data_store(1120, 810, 1540, 885, "D1", "ohlcv_candles", "แคชแท่งเทียน 7 กรอบเวลา (W1-M5)")

# Store D2: swing_points & events (Col 3 Bottom B)
draw_data_store(1120, 925, 1540, 1000, "D2", "swing_points & events", "พิกัด SH, SL, BOS และ CHoCH")

# Process 4.0: Order Block Identification (Col 4 Middle)
draw_process(1680, 520, 2100, 710, "4.0", "ระบุโซนราคา Order Block", "Price Zone Identification", "สกัดช่วงแท่งเทียนต้นกำเนิด OB/FVG", "ตรวจสอบการทดสอบโซน (Mitigation)", (245, 158, 11))

# Process 5.0: Multi-TF Scoring (Col 4 Bottom)
draw_process(1680, 810, 2100, 1000, "5.0", "คำนวณคะแนนพหุกรอบเวลา", "Multi-Timeframe Scoring", "ถ่วงน้ำหนักคะแนนทั้ง 7 กรอบเวลา", "คำนวณคะแนนรวมสุทธิ (Stotal)", (139, 92, 246))

# Store D3: price_zones (Col 5 Middle)
draw_data_store(2220, 570, 2550, 660, "D3", "price_zones", "โซน Order Block & FVG")

# Store D4: mtf_trend_scores (Col 5 Bottom)
draw_data_store(2220, 860, 2550, 950, "D4", "mtf_trend_scores", "คะแนนสุทธิ Stotal & สัญญาณ")

# ==============================================================================
# DATA FLOW CONNECTIONS
# ==============================================================================

# 1. E1 -> P1.0: User Request
draw_flow_h(420, 560, 290, "คู่เงิน & กรอบเวลา", "HTTP GET /api/data", "right", (37, 99, 235))

# 2. P6.0 -> E1: Routed ABOVE Process 1.0 so no line crosses any box!
draw.line([(1120, 280), (1020, 280), (1020, 185), (240, 185), (240, 230)], fill=(236, 72, 153), width=3)
draw.polygon([(240, 230), (232, 230 - 12), (248, 230 - 12)], fill=(236, 72, 153))
bb_p6 = draw.textbbox((0, 0), "กราฟโครงสร้างราคา & แดชบอร์ดสรุปผลแนวโน้ม (JSON Response)", font=f_flow)
tw_p6 = bb_p6[2] - bb_p6[0]
draw.rounded_rectangle([630 - tw_p6//2 - 8, 185 - 14, 630 + tw_p6//2 + 8, 185 + 14], radius=6, fill=(255, 255, 255), outline=(236, 72, 153), width=1)
draw.text((630, 185), "กราฟโครงสร้างราคา & แดชบอร์ดสรุปผลแนวโน้ม (JSON Response)", font=f_flow, fill=(236, 72, 153), anchor="mm")

# 3. P1.0 -> P2.0: Trigger fetch
draw_flow_v(740, 420, 810, "คำสั่งดึงข้อมูลราคา", "Fetch Signal", "down", (14, 165, 233))

# 4. P2.0 <-> E2: Communication with MetaTrader 5
draw_flow_h(560, 420, 870, "เรียก MT5 API (copy_rates)", "Symbol, TF, Count", "left", (217, 119, 6))
draw_flow_h(420, 560, 930, "ข้อมูลแท่งเทียนดิบ", "OHLCV Struct Rates", "right", (217, 119, 6))

# 5. P2.0 -> D1: Store Candles
draw_flow_h(920, 1120, 850, "ชุดแท่งเทียนจัดรูปแบบแล้ว", "Cleaned DataFrames", "right", (14, 165, 233))

# 6. D1 -> P3.0: Feed Candles to Engine
draw_flow_v(1230, 810, 710, "ข้อมูล OHLCV", "Look-back Window", "up", (16, 185, 129))

# 7. P3.0 -> D2: Store Swings & Events
draw_flow_v(1410, 710, 925, "บันทึก SH, SL, BOS, CHoCH", "Structure Metadata", "down", (16, 185, 129))

# 8. P3.0 -> P4.0: Event Trigger for OB
draw_flow_h(1540, 1680, 615, "สัญญาณ BOS/CHoCH", "Event Trigger", "right", (245, 158, 11))

# 9. P4.0 -> D3: Store Price Zones
draw.line([(2100, 615), (2220, 615)], fill=(245, 158, 11), width=3)
draw.polygon([(2220, 615), (2220 - 15, 615 - 9), (2220 - 15, 615 + 9)], fill=(245, 158, 11))
draw.text((2160, 592), "พิกัดโซนราคา", font=f_flow_sub, fill=(245, 158, 11), anchor="mm")

# 10. D2 -> P5.0: Trend State (Dk)
draw.line([(1540, 960), (1680, 960)], fill=(139, 92, 246), width=3)
draw.polygon([(1680, 960), (1680 - 15, 960 - 9), (1680 - 15, 960 + 9)], fill=(139, 92, 246))
draw.text((1610, 935), "สถานะแนวโน้ม (Dk)", font=f_flow, fill=(139, 92, 246), anchor="mm")

# 11. P5.0 -> D4: Store MTF Scores
draw.line([(2100, 905), (2220, 905)], fill=(139, 92, 246), width=3)
draw.polygon([(2220, 905), (2220 - 15, 905 - 9), (2220 - 15, 905 + 9)], fill=(139, 92, 246))
draw.text((2160, 882), "บันทึกคะแนน Stotal", font=f_flow_sub, fill=(139, 92, 246), anchor="mm")

# 12. Feeds to P6.0 (Visualization):
# P3.0 -> P6.0: Structure points (Vertical)
draw_flow_v(1330, 520, 420, "พิกัดเส้น BOS & CHoCH", "Overlay Lines", "up", (16, 185, 129))

# D3 -> P6.0: Active Zones (Routed Line)
draw.line([(2220, 585), (2140, 585), (2140, 260), (1540, 260)], fill=(245, 158, 11), width=3)
draw.polygon([(1540, 260), (1540 + 15, 260 - 9), (1540 + 15, 260 + 9)], fill=(245, 158, 11))
draw.text((1840, 235), "โซน Order Block & FVG ที่ยังไม่ถูกทดสอบ (Active Zones)", font=f_flow, fill=(217, 119, 6), anchor="mm")

# D4 -> P6.0: Scores (Routed Line)
draw.line([(2220, 880), (2120, 880), (2120, 360), (1540, 360)], fill=(139, 92, 246), width=3)
draw.polygon([(1540, 360), (1540 + 15, 360 - 9), (1540 + 15, 360 + 9)], fill=(139, 92, 246))
draw.text((1830, 335), "คะแนนแนวโน้ม 7 กรอบเวลา (Stotal & Trade Signal)", font=f_flow, fill=(139, 92, 246), anchor="mm")

# ==============================================================================
# LEGEND BOX (Bottom Left)
# ==============================================================================
lx1, ly1, lx2, ly2 = 60, 1180, 1050, 1390
draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=16, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
draw.text((lx1 + 25, ly1 + 26), "คำอธิบายสัญลักษณ์ตามมาตรฐาน DFD (Gane & Sarson / DeMarco):", font=f_legend, fill=(15, 23, 42))

# Legend Items
# 1. External Entity
draw.rounded_rectangle([lx1 + 25, ly1 + 65, lx1 + 180, ly1 + 120], radius=8, fill=(239, 246, 255), outline=(37, 99, 235), width=2)
draw.text((lx1 + 102, ly1 + 92), "External Entity", font=get_font(18, bold=True), fill=(37, 99, 235), anchor="mm")
draw.text((lx1 + 25, ly1 + 145), "สิ่งที่อยู่นอกระบบ (User, MT5)", font=f_flow_sub, fill=(71, 85, 105))

# 2. Process
draw.rounded_rectangle([lx1 + 260, ly1 + 65, lx1 + 415, ly1 + 120], radius=8, fill=(240, 253, 244), outline=(16, 185, 129), width=2)
draw.text((lx1 + 337, ly1 + 92), "Process (1.0 - 6.0)", font=get_font(18, bold=True), fill=(16, 185, 129), anchor="mm")
draw.text((lx1 + 260, ly1 + 145), "กระบวนการประมวลผลข้อมูล", font=f_flow_sub, fill=(71, 85, 105))

# 3. Data Store
draw.rectangle([lx1 + 500, ly1 + 65, lx1 + 655, ly1 + 120], fill=(255, 251, 235))
draw.line([(lx1 + 500, ly1 + 65), (lx1 + 655, ly1 + 65)], fill=(217, 119, 6), width=2)
draw.line([(lx1 + 500, ly1 + 120), (lx1 + 655, ly1 + 120)], fill=(217, 119, 6), width=2)
draw.text((lx1 + 577, ly1 + 92), "Data Store (D1 - D4)", font=get_font(18, bold=True), fill=(217, 119, 6), anchor="mm")
draw.text((lx1 + 500, ly1 + 145), "แหล่งจัดเก็บข้อมูล / แคช", font=f_flow_sub, fill=(71, 85, 105))

# 4. Data Flow
draw.line([(lx1 + 740, ly1 + 92), (lx1 + 880, ly1 + 92)], fill=(59, 130, 246), width=4)
draw.polygon([(lx1 + 880, ly1 + 92), (lx1 + 865, ly1 + 82), (lx1 + 865, ly1 + 102)], fill=(59, 130, 246))
draw.text((lx1 + 810, ly1 + 65), "Data Flow", font=get_font(18, bold=True), fill=(59, 130, 246), anchor="mm")
draw.text((lx1 + 740, ly1 + 145), "เส้นทางการไหลของข้อมูล", font=f_flow_sub, fill=(71, 85, 105))

out_path = r"e:\Project\smc-backtest-backend\SMC_DFD_Level1_Architecture.png"
img.save(out_path, "PNG")
dl_path = r"C:\Users\ONEST\Downloads\SMC_DFD_Level1_Architecture.png"
shutil.copyfile(out_path, dl_path)
print("Saved clean DFD Level 1 to:", out_path)
print("Copied to Downloads:", dl_path)
