import os
from PIL import Image, ImageDraw, ImageFont

FONT_REG = r"C:\Windows\Fonts\leelawUI.ttf"
FONT_BOLD = r"C:\Windows\Fonts\leelaUIb.ttf"
FONT_MONO = r"C:\Windows\Fonts\consolab.ttf"

def get_font(path, size):
    return ImageFont.truetype(path, size)

UPPER_VOWELS = set('\u0e31\u0e34\u0e35\u0e36\u0e37\u0e47\u0e4d')
TONE_MARKS = set('\u0e48\u0e49\u0e4a\u0e4b\u0e4c')

def draw_th(draw, xy, text, font, fill, anchor="la"):
    x, y = xy
    if anchor in ("mm", "mt", "mb"):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if anchor[0] == "m":
            x = x - tw / 2
        if anchor[1] == "m":
            y = y - th / 2 - bbox[1]
        elif anchor[1] == "t":
            y = y - bbox[1]
    elif anchor == "ra":
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = x - tw
    has_stack = False
    for idx in range(1, len(text)):
        if text[idx] in TONE_MARKS and text[idx - 1] in UPPER_VOWELS:
            has_stack = True
            break
    if not has_stack:
        draw.text((x, y), text, font=font, fill=fill)
        return
    base_chars = []
    stacked_tones = []
    for ch in text:
        if ch in TONE_MARKS and len(base_chars) > 0 and base_chars[-1] in UPPER_VOWELS:
            prefix = "".join(base_chars)
            pb = draw.textbbox((0, 0), prefix, font=font)
            px = x + (pb[2] - pb[0])
            stacked_tones.append((px, ch))
        else:
            base_chars.append(ch)
    base_str = "".join(base_chars)
    draw.text((x, y), base_str, font=font, fill=fill)
    shift_y = max(4, int(font.size * 0.20))
    for px, tone_ch in stacked_tones:
        draw.text((px, y - shift_y), tone_ch, font=font, fill=fill)

def render_highlights_slide():
    W, H = 2560, 1440
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    # Top header bar accent
    draw.rectangle([90, 95, 108, 240], fill=(37, 99, 235, 255))

    f_title = get_font(FONT_BOLD, 64)
    f_sub = get_font(FONT_REG, 32)
    f_badge = get_font(FONT_MONO, 24)
    f_h3 = get_font(FONT_BOLD, 34)
    f_body = get_font(FONT_REG, 27)
    f_num = get_font(FONT_BOLD, 56)

    draw_th(draw, (135, 92), "จุดเด่นของโครงงานและผลการประเมินความพึงพอใจ", f_title, (15, 23, 42, 255))
    draw_th(draw, (135, 182), "สรุปจุดเด่นทางวิศวกรรมของระบบ และผลการประเมินความพึงพอใจของผู้ใช้งาน 3 ด้าน (ตารางที่ 3 • Likert Scale 5 ระดับ)", f_sub, (71, 85, 105, 255))

    # Left Column: 3 Engineering Highlights
    highlights = [
        (
            "HIGHLIGHT 01 • ZERO SUBJECTIVE BIAS (7×7 TF × SMC MODULES)",
            "มาตรฐานการตรวจจับโครงสร้างตลาดแบบ Deterministic 100%",
            "ใช้ Finite State Machine และเกณฑ์ราคาปิด (Body Break) แยกแยะ BOS และ CHoCH",
            "อย่างเป็นระบบ ช่วยลดความคลุมเครือและขจัดอคติจากการตีกราฟด้วยมือ"
        ),
        (
            "HIGHLIGHT 02 • QUANTITATIVE VOLATILITY FILTERING",
            "คัดกรองเฉพาะโซนสถาบันคุณภาพสูงด้วยเกณฑ์ ATR & Cumulative Mean",
            "กรองแท่ง Order Block ที่ผันผวนผิดปกติ (< 2 × ATR) และช่องว่าง FVG (> 2 × Mean)",
            "พร้อมตรวจสอบและอัปเดตสถานะการถูกทำลายของโซน (Mitigated) อัตโนมัติ"
        ),
        (
            "HIGHLIGHT 03 • UNIFIED MULTI-TIMEFRAME DASHBOARD",
            "ผสานมุมมองภาพใหญ่ 7 Timeframes (W1–M5) คู่กับเรดาร์และระบบ Backtest",
            "คำนวณคะแนนถ่วงน้ำหนัก 7 กรอบเวลา แจ้งเตือนโซนราคาสำคัญ (H4 Setup Radar)",
            "และจำลองการเทรดย้อนหลังพร้อมวัดค่าสถิติในแดชบอร์ดเดียว"
        )
    ]

    ly = 300
    for badge, title, line1, line2 in highlights:
        # Card shadow & box
        draw.rounded_rectangle([96, ly + 8, 1416, ly + 308], radius=24, fill=(30, 58, 138, 18))
        draw.rounded_rectangle([90, ly, 1410, ly + 300], radius=24, fill=(255, 255, 255, 255), outline=(191, 219, 254, 255), width=3)
        draw.rounded_rectangle([90, ly, 104, ly + 300], radius=8, fill=(29, 78, 216, 255))

        # Pill badge
        draw.rounded_rectangle([135, ly + 32, 1020, ly + 78], radius=12, fill=(239, 246, 255, 255), outline=(191, 219, 254, 255), width=2)
        draw_th(draw, (155, ly + 40), badge, f_badge, (29, 78, 216, 255))

        draw_th(draw, (135, ly + 102), title, f_h3, (15, 23, 42, 255))
        draw_th(draw, (135, ly + 168), line1, f_body, (71, 85, 105, 255))
        draw_th(draw, (135, ly + 212), line2, f_body, (71, 85, 105, 255))

        ly += 335

    # Right Column: Dark Navy Evaluation Card (Table 3 from Report — NO '25 users')
    rx1, ry1, rx2, ry2 = 1460, 300, 2470, 1270
    draw.rounded_rectangle([rx1 + 10, ry1 + 10, rx2 + 10, ry2 + 10], radius=30, fill=(15, 23, 42, 45))
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=30, fill=(23, 43, 117, 255), outline=(59, 130, 246, 255), width=3)

    # Top badge inside navy card
    draw.rounded_rectangle([rx1 + 48, ry1 + 42, rx1 + 490, ry1 + 90], radius=12, fill=(30, 64, 175, 255), outline=(96, 165, 250, 255), width=2)
    draw_th(draw, (rx1 + 68, ry1 + 52), "TABLE 3 • USER EVALUATION", f_badge, (191, 219, 254, 255))

    draw.rounded_rectangle([rx2 - 260, ry1 + 42, rx2 - 48, ry1 + 90], radius=12, fill=(37, 99, 235, 255))
    draw_th(draw, (rx2 - 154, ry1 + 66), "Likert 5 ระดับ", get_font(FONT_BOLD, 24), (255, 255, 255, 255), anchor="mm")

    draw_th(draw, (rx1 + 48, ry1 + 115), "ผลการประเมินความพึงพอใจของผู้ใช้งานที่มีต่อระบบ", f_h3, (255, 255, 255, 255))

    eval_rows = [
        ("1. ความเหมาะสมต่อการแก้ปัญหา", "ลดเวลาในการตีกราฟและลดอคติในการตัดสินใจ", "4.52", "S.D. = 0.51 • ระดับดีมาก"),
        ("2. การออกแบบส่วนติดต่อผู้ใช้ (GUI)", "กราฟแสดงผลชัดเจน สีโซนอ่านง่าย ใช้งานสะดวก", "4.48", "S.D. = 0.54 • ระดับดี"),
        ("3. ความเหมาะสมของเทคนิคและฟังก์ชัน", "ความถูกต้องของอัลกอริทึม SMC และ 7 Timeframes", "4.56", "S.D. = 0.50 • ระดับดีมาก"),
    ]

    ey = ry1 + 195
    for r_title, r_sub, score, sd_txt in eval_rows:
        draw.rounded_rectangle([rx1 + 48, ey, rx2 - 48, ey + 195], radius=20, fill=(30, 58, 138, 255), outline=(96, 165, 250, 140), width=2)
        draw_th(draw, (rx1 + 80, ey + 38), r_title, get_font(FONT_BOLD, 31), (255, 255, 255, 255))
        draw_th(draw, (rx1 + 80, ey + 98), r_sub, get_font(FONT_REG, 25), (191, 219, 254, 255))

        draw_th(draw, (rx2 - 80, ey + 30), score, f_num, (147, 197, 253, 255), anchor="ra")
        draw_th(draw, (rx2 - 80, ey + 115), sd_txt, get_font(FONT_BOLD, 23), (219, 234, 254, 255), anchor="ra")
        ey += 220

    # Overall summary bar at bottom of navy card
    draw.line([(rx1 + 48, ry2 - 110), (rx2 - 48, ry2 - 110)], fill=(96, 165, 250, 120), width=2)
    draw_th(draw, (rx1 + 48, ry2 - 78), "ค่าเฉลี่ยรวมทุกด้าน (Overall Mean)", get_font(FONT_BOLD, 28), (191, 219, 254, 255))
    draw_th(draw, (rx2 - 48, ry2 - 84), "4.52 / 5.00 (ระดับดีมาก)", get_font(FONT_BOLD, 34), (255, 255, 255, 255), anchor="ra")

    out_dir = r"C:\Users\ONEST\Downloads"
    os.makedirs(out_dir, exist_ok=True)
    p1 = os.path.join(out_dir, "SMC_Highlights_Slide_16x9.png")
    img.convert("RGB").save(p1, "PNG", optimize=True)

    art_dir = r"C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d"
    img.convert("RGB").save(os.path.join(art_dir, "SMC_Highlights_Slide_16x9.png"), "PNG", optimize=True)
    print("Saved:", p1)

if __name__ == "__main__":
    render_highlights_slide()
