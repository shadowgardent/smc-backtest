from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Fonts setup (Windows Thai + English fonts)
FONT_DIR = r"C:\Windows\Fonts"
font_th_bold = os.path.join(FONT_DIR, "leelawdb.ttf")
font_th_reg  = os.path.join(FONT_DIR, "leelawui.ttf")
font_mono_b  = os.path.join(FONT_DIR, "consolab.ttf")
font_mono_r  = os.path.join(FONT_DIR, "consola.ttf")

if not os.path.exists(font_th_bold):
    font_th_bold = os.path.join(FONT_DIR, "tahomabd.ttf")
    font_th_reg  = os.path.join(FONT_DIR, "tahoma.ttf")

def f_bold(size): return ImageFont.truetype(font_th_bold, size)
def f_reg(size):  return ImageFont.truetype(font_th_reg, size)
def f_mono(size): return ImageFont.truetype(font_mono_b, size)
def f_monor(size): return ImageFont.truetype(font_mono_r, size)

UPPER_VOWELS = set("\u0e31\u0e34\u0e35\u0e36\u0e37\u0e47")
TONE_MARKS   = set("\u0e48\u0e49\u0e4a\u0e4b\u0e4c")

def draw_th(draw, xy, text, font, fill, anchor=None):
    """Render Thai text with proper stacked tone-mark elevation when preceded by upper vowels."""
    stacked = []
    base_chars = []
    for ch in text:
        if ch in TONE_MARKS and base_chars and base_chars[-1] in UPPER_VOWELS:
            prefix = "".join(base_chars)
            stacked.append((prefix, ch))
        else:
            base_chars.append(ch)
    base_text = "".join(base_chars)
    draw.text(xy, base_text, font=font, fill=fill, anchor=anchor)

    if not stacked:
        return

    # Compute top-left origin of base_text if anchor is used
    bbox = draw.textbbox(xy, base_text, font=font, anchor=anchor)
    origin_x = bbox[0]
    # Draw each stacked tone mark elevated above the upper vowel
    shift_y = max(4, int(font.size * 0.22))
    shift_x = int(font.size * 0.06)
    for prefix, tone in stacked:
        pw = draw.textlength(prefix, font=font)
        draw.text((origin_x + pw - shift_x, xy[1] - shift_y), tone, font=font, fill=fill, anchor=anchor)

def draw_rounded_rect_with_shadow(base_img, bbox, radius, fill, outline=None, width=2, shadow_color=(30, 58, 138, 28), offset=(0, 8), blur=14):
    x1, y1, x2, y2 = bbox
    pad = blur * 2 + 12
    sw = (x2 - x1) + pad * 2
    sh = (y2 - y1) + pad * 2
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        [pad + offset[0], pad + offset[1], pad + (x2 - x1) + offset[0], pad + (y2 - y1) + offset[1]],
        radius=radius,
        fill=shadow_color
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base_img.alpha_composite(shadow, (x1 - pad, y1 - pad))

    draw = ImageDraw.Draw(base_img)
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow_h(draw, x1, y, x2, color=(37, 99, 235, 255), width=5, head_len=14, head_w=9):
    draw.line([(x1, y), (x2 - head_len + 2, y)], fill=color, width=width)
    draw.polygon([
        (x2, y),
        (x2 - head_len, y - head_w),
        (x2 - head_len, y + head_w)
    ], fill=color)

def draw_arrow_v(draw, x, y1, y2, color=(37, 99, 235, 255), width=4, head_len=12, head_w=8):
    if y2 > y1:
        draw.line([(x, y1), (x, y2 - head_len + 2)], fill=color, width=width)
        draw.polygon([(x, y2), (x - head_w, y2 - head_len), (x + head_w, y2 - head_len)], fill=color)
    else:
        draw.line([(x, y1), (x, y2 + head_len - 2)], fill=color, width=width)
        draw.polygon([(x, y2), (x - head_w, y2 + head_len), (x + head_w, y2 + head_len)], fill=color)

def render_diagram_core(canvas, offset_y=0):
    draw = ImageDraw.Draw(canvas)

    # =========================================================================
    # SECTION 1: TOP LAYER GROUP HEADERS (3 ARCHITECTURAL TIERS)
    # =========================================================================
    tier_y = offset_y + 20
    tiers = [
        (70,   788,  "1. CLIENT & API GATEWAY LAYER", (239, 246, 255, 255), (147, 197, 253, 255), (30, 64, 175, 255)),
        (836,  1554, "2. DATA FEED & CORE SMC ENGINE LAYER", (219, 234, 254, 255), (59, 130, 246, 255), (23, 37, 84, 255)),
        (1602, 2320, "3. SERIALIZATION & VISUALIZATION LAYER", (239, 246, 255, 255), (147, 197, 253, 255), (30, 64, 175, 255)),
    ]
    for tx1, tx2, tlabel, tfill, tborder, ttext in tiers:
        draw.rounded_rectangle([tx1, tier_y, tx2, tier_y + 42], radius=21, fill=tfill, outline=tborder, width=2)
        draw.text(((tx1 + tx2) // 2, tier_y + 21), tlabel, font=f_mono(16), fill=ttext, anchor="mm")

    # =========================================================================
    # SECTION 2: MAIN 6 DATA FLOW CARDS
    # =========================================================================
    card_y1 = offset_y + 84
    card_y2 = offset_y + 344
    card_w = 335
    gap = 48
    start_x = 70

    steps = [
        {
            "num": "01",
            "badge": "USER INPUT",
            "title": "เลือก Symbol & TF",
            "subtitle": "Angular SPA Frontend",
            "bullets": [
                "• เลือกคู่เงิน (XAUUSD, EURUSD)",
                "• เลือกกรอบเวลา (M5 ถึง W1)",
                "• เปิด/ปิดเลเยอร์ SMC บนกราฟ"
            ],
            "highlight": False
        },
        {
            "num": "02",
            "badge": "API GATEWAY",
            "title": "FastAPI Validation",
            "subtitle": "RESTful Router Layer",
            "bullets": [
                "• รับคำขอ /api/data & /api/smc",
                "• ตรวจสอบพารามิเตอร์ Pydantic",
                "• จัดการ Async & CORS Policy"
            ],
            "highlight": False
        },
        {
            "num": "03",
            "badge": "MARKET FEED",
            "title": "MT5 OHLCV Data",
            "subtitle": "MetaTrader 5 Python API",
            "bullets": [
                "• ดึงแท่งเทียน copy_rates_from_pos",
                "• ดึงราคาเรียลไทม์ symbol_info_tick",
                "• แปลงเป็น Pandas DataFrame"
            ],
            "highlight": False
        },
        {
            "num": "04",
            "badge": "CORE ENGINE",
            "title": "SMC Pipeline (7 โมดูล)",
            "subtitle": "Vectorized NumPy + FSM",
            "bullets": [
                "• คำนวณ ATR, Swing, BOS/CHoCH",
                "• ตรวจจับโซน OB, FVG, EQH/EQL",
                "• ให้คะแนนพหุกรอบเวลา (7 TFs)"
            ],
            "highlight": True
        },
        {
            "num": "05",
            "badge": "DATA PAYLOAD",
            "title": "JSON Response",
            "subtitle": "Structured Serialization",
            "bullets": [
                "• แปลงพิกัดเวลา UTC & ระดับราคา",
                "• แยกสถานะ Active / Mitigated",
                "• ส่งกลับ JSON ความเร็วสูง"
            ],
            "highlight": False
        },
        {
            "num": "06",
            "badge": "PRESENTATION",
            "title": "Chart & Dashboard",
            "subtitle": "Lightweight Charts + Canvas",
            "bullets": [
                "• วาดกราฟแท่งเทียนอินเทอร์แอคทีฟ",
                "• วาดกล่อง OB/FVG ด้วย HTML5 Canvas",
                "• แสดงตาราง 7-TF & ผล Backtest"
            ],
            "highlight": False
        }
    ]

    card_centers = []
    for idx, st in enumerate(steps):
        cx1 = start_x + idx * (card_w + gap)
        cx2 = cx1 + card_w
        card_centers.append((cx1 + cx2) // 2)

        if st["highlight"]:
            draw_rounded_rect_with_shadow(
                canvas, [cx1, card_y1, cx2, card_y2], radius=22,
                fill=(23, 43, 117, 255), outline=(59, 130, 246, 255), width=4,
                shadow_color=(30, 58, 138, 65), offset=(0, 10), blur=18
            )
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle([cx1 + 18, card_y1 + 16, cx1 + 74, card_y1 + 52], radius=12, fill=(37, 99, 235, 255))
            draw.text((cx1 + 46, card_y1 + 34), st["num"], font=f_mono(20), fill=(255, 255, 255, 255), anchor="mm")

            draw.rounded_rectangle([cx1 + 84, card_y1 + 20, cx2 - 18, card_y1 + 48], radius=14, fill=(30, 64, 175, 255), outline=(96, 165, 250, 255), width=1)
            draw.text(((cx1 + 84 + cx2 - 18) // 2, card_y1 + 34), st["badge"], font=f_mono(13), fill=(219, 234, 254, 255), anchor="mm")

            draw_th(draw, (cx1 + 20, card_y1 + 78), st["title"], font=f_bold(24), fill=(255, 255, 255, 255))
            draw.text((cx1 + 20, card_y1 + 110), st["subtitle"], font=f_mono(14), fill=(147, 197, 253, 255))
            draw.line([(cx1 + 20, card_y1 + 136), (cx2 - 20, card_y1 + 136)], fill=(59, 130, 246, 160), width=2)

            by = card_y1 + 150
            for b in st["bullets"]:
                draw_th(draw, (cx1 + 20, by), b, font=f_reg(16), fill=(239, 246, 255, 255))
                by += 32
        else:
            draw_rounded_rect_with_shadow(
                canvas, [cx1, card_y1, cx2, card_y2], radius=22,
                fill=(255, 255, 255, 255), outline=(59, 130, 246, 255), width=3,
                shadow_color=(30, 58, 138, 28), offset=(0, 8), blur=14
            )
            draw = ImageDraw.Draw(canvas)
            draw.rounded_rectangle([cx1 + 18, card_y1 + 16, cx1 + 74, card_y1 + 52], radius=12, fill=(219, 234, 254, 255), outline=(59, 130, 246, 255), width=2)
            draw.text((cx1 + 46, card_y1 + 34), st["num"], font=f_mono(20), fill=(29, 78, 216, 255), anchor="mm")

            draw.rounded_rectangle([cx1 + 84, card_y1 + 20, cx2 - 18, card_y1 + 48], radius=14, fill=(241, 245, 249, 255))
            draw.text(((cx1 + 84 + cx2 - 18) // 2, card_y1 + 34), st["badge"], font=f_mono(13), fill=(51, 65, 85, 255), anchor="mm")

            draw_th(draw, (cx1 + 20, card_y1 + 78), st["title"], font=f_bold(24), fill=(15, 23, 42, 255))
            draw.text((cx1 + 20, card_y1 + 110), st["subtitle"], font=f_mono(14), fill=(37, 99, 235, 255))
            draw.line([(cx1 + 20, card_y1 + 136), (cx2 - 20, card_y1 + 136)], fill=(219, 234, 254, 255), width=2)

            by = card_y1 + 150
            for b in st["bullets"]:
                draw_th(draw, (cx1 + 20, by), b, font=f_reg(16), fill=(51, 65, 85, 255))
                by += 32

        if idx < len(steps) - 1:
            ax1 = cx2 + 4
            ax2 = cx2 + gap - 4
            ay = (card_y1 + card_y2) // 2
            draw_arrow_h(draw, ax1, ay, ax2, color=(37, 99, 235, 255), width=5, head_len=14, head_w=9)

    # =========================================================================
    # SECTION 3: EXPANDED SUB-PIPELINE FOR STAGE 04 (7 SMC ALGORITHMIC MODULES)
    # =========================================================================
    c4_center = card_centers[3]
    sub_box_y1 = offset_y + 392
    sub_box_y2 = offset_y + 625
    draw_arrow_v(draw, c4_center - 18, card_y2 + 4, sub_box_y1 - 4, color=(29, 78, 216, 255), width=4)
    draw_arrow_v(draw, c4_center + 18, sub_box_y1 - 4, card_y2 + 4, color=(59, 130, 246, 255), width=4)

    draw_rounded_rect_with_shadow(
        canvas, [70, sub_box_y1, 2330, sub_box_y2], radius=24,
        fill=(240, 247, 255, 255), outline=(96, 165, 250, 255), width=3,
        shadow_color=(30, 58, 138, 22), offset=(0, 6), blur=12
    )
    draw = ImageDraw.Draw(canvas)

    # Sub-box header bar
    draw.rounded_rectangle([94, sub_box_y1 + 14, 2306, sub_box_y1 + 66], radius=14, fill=(30, 58, 138, 255))
    draw_th(
        draw,
        (120, sub_box_y1 + 27),
        "ภายในขั้นตอนที่ 04 : ลำดับการประมวลผลอัลกอริทึม SMC ทั้ง 7 โมดูล (services/smc_engine.py & routers/dashboard.py)",
        font=f_bold(19), fill=(255, 255, 255, 255)
    )
    draw.text(
        (2285, sub_box_y1 + 40),
        "DETERMINISTIC PIPELINE",
        font=f_mono(15), fill=(147, 197, 253, 255), anchor="rm"
    )

    modules = [
        ("M1", "calc_atr()", "คำนวณค่า ATR (14)", "กรองความผันผวน"),
        ("M2", "detect_swings()", "Swing High / Low", "หน้าต่าง 2N + 1 แท่ง"),
        ("M3", "detect_structure()", "BOS & CHoCH", "Finite State Machine"),
        ("M4", "detect_order_blocks()", "Order Block (OB)", "Origin + กรอง < 2×ATR"),
        ("M5", "detect_fvg()", "Fair Value Gap", "3 แท่ง + > 2×Mean"),
        ("M6", "EQH/EQL & Zones", "Liquidity & P/D", "เป้าสภาพคล่อง & โซนคุ้มค่า"),
        ("M7", "get_dashboard()", "Multi-TF Score", "ถ่วงน้ำหนัก 7 TF (W1–M5)"),
    ]

    mod_w = 286
    mod_gap = 32
    mod_start_x = 96
    mod_y1 = sub_box_y1 + 80
    mod_y2 = sub_box_y2 - 18

    for m_idx, (mcode, mfunc, mtitle, mdesc) in enumerate(modules):
        mx1 = mod_start_x + m_idx * (mod_w + mod_gap)
        mx2 = mx1 + mod_w
        is_last = (m_idx == len(modules) - 1)
        mfill = (255, 255, 255, 255)
        mborder = (37, 99, 235, 255) if is_last else (147, 197, 253, 255)

        draw.rounded_rectangle([mx1, mod_y1, mx2, mod_y2], radius=16, fill=mfill, outline=mborder, width=2)
        draw.rounded_rectangle([mx1 + 14, mod_y1 + 12, mx1 + 60, mod_y1 + 40], radius=8, fill=(37, 99, 235, 255))
        draw.text((mx1 + 37, mod_y1 + 26), mcode, font=f_mono(15), fill=(255, 255, 255, 255), anchor="mm")

        draw.text((mx1 + 70, mod_y1 + 26), mfunc, font=f_mono(14), fill=(30, 64, 175, 255), anchor="lm")
        draw_th(draw, (mx1 + 16, mod_y1 + 54), mtitle, font=f_bold(19), fill=(15, 23, 42, 255))
        draw_th(draw, (mx1 + 16, mod_y1 + 86), mdesc, font=f_reg(15), fill=(71, 85, 105, 255))

        if m_idx < len(modules) - 1:
            ax1 = mx2 + 3
            ax2 = mx2 + mod_gap - 3
            ay = (mod_y1 + mod_y2) // 2
            draw_arrow_h(draw, ax1, ay, ax2, color=(59, 130, 246, 255), width=4, head_len=10, head_w=7)

    # =========================================================================
    # SECTION 4: BOTTOM PIPELINE FLOW BAR (Validate -> Fetch -> ... -> Render)
    # =========================================================================
    bar_y1 = offset_y + 655
    bar_y2 = offset_y + 735
    draw_rounded_rect_with_shadow(
        canvas, [220, bar_y1, 2180, bar_y2], radius=40,
        fill=(255, 255, 255, 255), outline=(59, 130, 246, 255), width=3,
        shadow_color=(30, 58, 138, 25), offset=(0, 6), blur=12
    )
    draw = ImageDraw.Draw(canvas)

    keywords = ["Validate", "Fetch", "Normalize", "Detect", "Score", "Serialize", "Render"]
    kw_x = 340
    kw_step = 285
    for k_idx, kw in enumerate(keywords):
        kx = kw_x + k_idx * kw_step
        ky = (bar_y1 + bar_y2) // 2
        is_core = kw in ("Detect", "Score")
        pfill = (30, 58, 138, 255) if is_core else (239, 246, 255, 255)
        pborder = (37, 99, 235, 255) if is_core else (147, 197, 253, 255)
        ptxt = (255, 255, 255, 255) if is_core else (23, 43, 117, 255)

        draw.rounded_rectangle([kx - 95, ky - 24, kx + 95, ky + 24], radius=24, fill=pfill, outline=pborder, width=2)
        draw.text((kx, ky), kw, font=f_mono(22), fill=ptxt, anchor="mm")
        if k_idx < len(keywords) - 1:
            arrow_start = kx + 105
            arrow_end = kx + kw_step - 105
            draw_arrow_h(draw, arrow_start, ky, arrow_end, color=(37, 99, 235, 255), width=4, head_len=12, head_w=8)


def main():
    out_dir_dl = r"C:\Users\ONEST\Downloads"
    out_dir_art = r"C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d"
    out_dir_pres = r"e:\Project\smc-backtest-backend\presentation\public\images"
    os.makedirs(out_dir_pres, exist_ok=True)

    # 1. Diagram-Only (Transparent Background, ready to paste onto existing Canva slide)
    diag_img = Image.new("RGBA", (2400, 770), (0, 0, 0, 0))
    render_diagram_core(diag_img, offset_y=0)

    p_trans_dl = os.path.join(out_dir_dl, "SMC_Data_Flow_Diagram_Transparent.png")
    p_trans_art = os.path.join(out_dir_art, "SMC_Data_Flow_Diagram_Transparent.png")
    p_trans_pres = os.path.join(out_dir_pres, "SMC_Data_Flow_Diagram_Transparent.png")
    diag_img.save(p_trans_dl, "PNG")
    diag_img.save(p_trans_art, "PNG")
    diag_img.save(p_trans_pres, "PNG")

    # 2. Full 16:9 Slide (2400 x 1350) matching the exact Canva slide layout
    slide_img = Image.new("RGBA", (2400, 1350), (248, 250, 252, 255))
    sdraw = ImageDraw.Draw(slide_img)

    # Left blue vertical accent bar + Title & Subtitle
    sdraw.rounded_rectangle([80, 78, 96, 218], radius=6, fill=(37, 99, 235, 255))
    draw_th(sdraw, (124, 82), "แผนภาพการไหลของข้อมูล (System Data Flow)", font=f_bold(54), fill=(15, 23, 42, 255))
    draw_th(sdraw, (124, 160), "จากคำสั่งผู้ใช้ สู่การประมวลผลอัลกอริทึม SMC และการแสดงผลโครงสร้างตลาดแบบอินเทอร์แอคทีฟ", font=f_reg(28), fill=(100, 116, 139, 255))

    # Top-right badge
    sdraw.rounded_rectangle([1890, 92, 2320, 152], radius=30, fill=(219, 234, 254, 255), outline=(59, 130, 246, 255), width=2)
    sdraw.text((2105, 122), "END-TO-END ARCHITECTURE", font=f_mono(20), fill=(30, 58, 138, 255), anchor="mm")

    render_diagram_core(slide_img, offset_y=290)

    p_full_dl = os.path.join(out_dir_dl, "SMC_Data_Flow_Slide_16x9.png")
    p_full_art = os.path.join(out_dir_art, "SMC_Data_Flow_Slide_16x9.png")
    p_full_pres = os.path.join(out_dir_pres, "SMC_Data_Flow_Slide_16x9.png")
    slide_img.convert("RGB").save(p_full_dl, "PNG", quality=98)
    slide_img.convert("RGB").save(p_full_art, "PNG", quality=98)
    slide_img.convert("RGB").save(p_full_pres, "PNG", quality=98)
    print("Saved successfully:", p_trans_dl, p_full_dl)

if __name__ == "__main__":
    main()
