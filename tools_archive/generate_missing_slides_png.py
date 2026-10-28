import os
import shutil
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
    for idx in range(len(text)):
        if text[idx] in TONE_MARKS:
            prev_upper = idx > 0 and text[idx - 1] in UPPER_VOWELS
            next_am = idx + 1 < len(text) and text[idx + 1] == '\u0e33'
            if prev_upper or next_am:
                has_stack = True
                break
    if not has_stack:
        draw.text((x, y), text, font=font, fill=fill)
        return
    base_chars = []
    stacked_tones = []
    for idx, ch in enumerate(text):
        prev_upper = len(base_chars) > 0 and base_chars[-1] in UPPER_VOWELS
        next_am = idx + 1 < len(text) and text[idx + 1] == '\u0e33'
        if ch in TONE_MARKS and (prev_upper or next_am):
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

def render_objectives_slide(out_dir, art_dir):
    W, H = 2560, 1440
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    # Top header bar accent (matching Canva pages)
    draw.rectangle([64, 85, 80, 242], fill=(37, 99, 235, 255))

    f_title = get_font(FONT_BOLD, 68)
    f_sub = get_font(FONT_REG, 34)
    f_num = get_font(FONT_BOLD, 88)
    f_h3 = get_font(FONT_BOLD, 40)
    f_body = get_font(FONT_REG, 29)
    f_pill = get_font(FONT_BOLD, 25)

    draw_th(draw, (120, 82), "วัตถุประสงค์ของโครงการวิจัย", f_title, (15, 23, 42, 255))
    draw_th(draw, (122, 176), "2 เป้าหมายหลักในการพัฒนาระบบวิเคราะห์โครงสร้างตลาดการเงินด้วยอัลกอริทึม SMC", f_sub, (100, 116, 139, 255))

    # Left Card: Objective 01 (Dark Navy Card matching Canva style)
    lx1, ly1, lx2, ly2 = 120, 320, 1235, 1210
    draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=16, fill=(23, 43, 117, 255))

    draw_th(draw, (lx1 + 65, ly1 + 60), "01", f_num, (255, 255, 255, 255))
    draw_th(draw, (lx1 + 65, ly1 + 205), "พัฒนาเว็บแอปพลิเคชันแสดงกราฟ", f_h3, (147, 197, 253, 255))
    draw_th(draw, (lx1 + 65, ly1 + 262), "และโครงสร้างตลาดแบบอินเทอร์แอคทีฟ", f_h3, (147, 197, 253, 255))

    draw_th(draw, (lx1 + 65, ly1 + 355), "ออกแบบและพัฒนาระบบที่ดึงข้อมูลแท่งเทียน OHLCV จาก MT5", f_body, (241, 245, 249, 255))
    draw_th(draw, (lx1 + 65, ly1 + 402), "มาคำนวณและวาดองค์ประกอบตามทฤษฎี SMC อัตโนมัติ:", f_body, (241, 245, 249, 255))

    pills_1 = [
        ("Swing High / Swing Low", "BOS & CHoCH Structure"),
        ("Order Blocks (OB + ATR)", "Fair Value Gap (FVG)"),
        ("Liquidity (EQH / EQL)", "Premium / Discount Zone"),
    ]
    py = ly1 + 485
    for p_left, p_right in pills_1:
        draw.rounded_rectangle([lx1 + 65, py, lx1 + 535, py + 78], radius=12, fill=(30, 58, 138, 255), outline=(96, 165, 250, 160), width=2)
        draw_th(draw, (lx1 + 90, py + 22), "• " + p_left, f_pill, (255, 255, 255, 255))

        draw.rounded_rectangle([lx1 + 560, py, lx2 - 65, py + 78], radius=12, fill=(30, 58, 138, 255), outline=(96, 165, 250, 160), width=2)
        draw_th(draw, (lx1 + 585, py + 22), "• " + p_right, f_pill, (255, 255, 255, 255))
        py += 102

    # Right Card: Objective 02 (Clean White Card with Blue Border matching Canva style)
    rx1, ry1, rx2, ry2 = 1325, 320, 2440, 1210
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=16, fill=(255, 255, 255, 255), outline=(219, 234, 254, 255), width=3)

    draw_th(draw, (rx1 + 65, ry1 + 60), "02", f_num, (23, 43, 117, 255))
    draw_th(draw, (rx1 + 65, ry1 + 205), "พัฒนาระบบสแกนแนวโน้มพหุกรอบเวลา", f_h3, (37, 99, 235, 255))
    draw_th(draw, (rx1 + 65, ry1 + 262), "และระบบทดสอบย้อนหลัง (Backtesting)", f_h3, (37, 99, 235, 255))

    draw_th(draw, (rx1 + 65, ry1 + 355), "สังเคราะห์สัญญาณจาก 7 กรอบเวลาพร้อมกัน และจำลองการเทรด", f_body, (71, 85, 105, 255))
    draw_th(draw, (rx1 + 65, ry1 + 402), "ย้อนหลังเพื่อประเมินประสิทธิภาพเชิงสถิติอย่างเป็นระบบ:", f_body, (71, 85, 105, 255))

    items_2 = [
        ("Multi-Timeframe Trend Dashboard (7 TFs)", "คำนวณคะแนนถ่วงน้ำหนัก W1 ถึง M5 (-13 ถึง +13 คะแนน)"),
        ("H4 SMC Setup Radar", "ตรวจจับระยะห่างราคาปัจจุบันกับโซน OB และ FVG ที่ยังไม่ถูกทำลาย"),
        ("Automated Backtesting Engine", "จำลองเข้าเทรดตามโซน SMC พร้อมคำนวณ Win Rate และ Profit Factor"),
    ]
    iy = ry1 + 480
    for it_title, it_sub in items_2:
        draw.rounded_rectangle([rx1 + 65, iy, rx2 - 65, iy + 102], radius=12, fill=(248, 250, 252, 255), outline=(191, 219, 254, 255), width=2)
        draw_th(draw, (rx1 + 92, iy + 16), "• " + it_title, f_pill, (23, 43, 117, 255))
        draw_th(draw, (rx1 + 112, iy + 54), it_sub, get_font(FONT_REG, 24), (71, 85, 105, 255))
        iy += 120

    p1 = os.path.join(out_dir, "SMC_Slide_Objectives_16x9.png")
    img.convert("RGB").save(p1, "PNG", optimize=True)
    img.convert("RGB").save(os.path.join(art_dir, "SMC_Slide_Objectives_16x9.png"), "PNG", optimize=True)
    print("Saved:", p1)

def render_conclusion_slide(out_dir, art_dir):
    W, H = 2560, 1440
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([64, 85, 80, 242], fill=(37, 99, 235, 255))

    f_title = get_font(FONT_BOLD, 68)
    f_sub = get_font(FONT_REG, 34)
    f_h3 = get_font(FONT_BOLD, 38)
    f_body = get_font(FONT_REG, 28)

    draw_th(draw, (120, 82), "สรุปผลการวิจัยและข้อเสนอแนะ", f_title, (15, 23, 42, 255))
    draw_th(draw, (122, 176), "บทสรุปการพัฒนาระบบวิเคราะห์โครงสร้างตลาดด้วยอัลกอริทึม SMC และแนวทางพัฒนาต่อยอด", f_sub, (100, 116, 139, 255))

    cards = [
        (
            "01 • สรุปผลด้านอัลกอริทึมและการแสดงผล",
            "เปลี่ยนการตีกราฟด้วยมือสู่ระบบอัตโนมัติที่ตรวจสอบซ้ำได้ 100%",
            "ระบบสามารถตรวจจับ Swing High/Low, BOS, CHoCH, Order Block (กรองด้วย ATR) และ FVG",
            "พร้อมวาดโซนบนกราฟอินเทอร์แอคทีฟได้ถูกต้องตรงตามนิยามทฤษฎี SMC ทุกประการ"
        ),
        (
            "02 • สรุปผลด้านการตัดสินใจและผลประเมินความพึงพอใจ",
            "บูรณาการ 7 Timeframes พร้อมผลประเมินความพึงพอใจระดับดีมาก (4.52 / 5.00)",
            "ตาราง Multi-Timeframe Scoring ช่วยลดการเทรดสวนแนวโน้มหลัก และได้รับคะแนนประเมิน",
            "ด้านเทคนิคและฟังก์ชัน 4.56 • ด้านการแก้ปัญหา 4.52 • ด้านการออกแบบ GUI 4.48"
        ),
        (
            "03 • ข้อเสนอแนะและแนวทางการพัฒนาต่อยอดในอนาคต",
            "ขยายขีดความสามารถสู่ระบบแจ้งเตือนเรียลไทม์และการเรียนรู้ของเครื่อง",
            "พัฒนาต่อยอดระบบแจ้งเตือนสัญญาณอัตโนมัติผ่าน Line / Telegram เมื่อราคาเข้าสู่โซน H4 Radar",
            "และประยุกต์ใช้ Machine Learning ร่วมคัดกรองความน่าจะเป็นของโซน Order Block"
        ),
    ]

    cy = 310
    for badge, title, l1, l2 in cards:
        draw.rounded_rectangle([120, cy, 1680, cy + 265], radius=18, fill=(255, 255, 255, 255), outline=(191, 219, 254, 255), width=3)
        draw.rounded_rectangle([120, cy, 134, cy + 265], radius=8, fill=(37, 99, 235, 255))
        draw_th(draw, (165, cy + 28), badge, get_font(FONT_BOLD, 25), (37, 99, 235, 255))
        draw_th(draw, (165, cy + 78), title, f_h3, (15, 23, 42, 255))
        draw_th(draw, (165, cy + 146), l1, f_body, (71, 85, 105, 255))
        draw_th(draw, (165, cy + 190), l2, f_body, (71, 85, 105, 255))
        cy += 295

    # Right Q&A Navy Box
    qx1, qy1, qx2, qy2 = 1740, 310, 2440, 1165
    draw.rounded_rectangle([qx1, qy1, qx2, qy2], radius=24, fill=(23, 43, 117, 255))
    draw_th(draw, (2090, qy1 + 190), "THANK YOU", get_font(FONT_BOLD, 68), (255, 255, 255, 255), anchor="mm")
    draw_th(draw, (2090, qy1 + 290), "& Q/A", get_font(FONT_BOLD, 56), (147, 197, 253, 255), anchor="mm")
    draw.line([(qx1 + 90, qy1 + 380), (qx2 - 90, qy1 + 380)], fill=(96, 165, 250, 140), width=2)

    draw_th(draw, (2090, qy1 + 455), "ขอขอบคุณคณะกรรมการทุกท่าน", get_font(FONT_BOLD, 34), (255, 255, 255, 255), anchor="mm")
    draw_th(draw, (2090, qy1 + 520), "ยินดีรับฟังข้อเสนอแนะและตอบคำถามครับ", get_font(FONT_REG, 27), (191, 219, 254, 255), anchor="mm")

    draw.rounded_rectangle([qx1 + 65, qy2 - 220, qx2 - 65, qy2 - 65], radius=16, fill=(30, 58, 138, 255), outline=(96, 165, 250, 140), width=2)
    draw_th(draw, (2090, qy2 - 165), "ผู้วิจัย: นายนวพรหม ภูผาผิว", get_font(FONT_BOLD, 27), (255, 255, 255, 255), anchor="mm")
    draw_th(draw, (2090, qy2 - 115), "รหัสนักศึกษา 663450040-2 • มหาวิทยาลัยขอนแก่น", get_font(FONT_REG, 23), (191, 219, 254, 255), anchor="mm")

    p2 = os.path.join(out_dir, "SMC_Slide_Conclusion_QA_16x9.png")
    img.convert("RGB").save(p2, "PNG", optimize=True)
    img.convert("RGB").save(os.path.join(art_dir, "SMC_Slide_Conclusion_QA_16x9.png"), "PNG", optimize=True)
    print("Saved:", p2)

if __name__ == "__main__":
    out_dir = r"C:\Users\ONEST\Downloads"
    art_dir = r"C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d"
    render_objectives_slide(out_dir, art_dir)
    render_conclusion_slide(out_dir, art_dir)
    # Also copy Canva Page 1 and Page 14 previews to art_dir
    shutil.copyfile(
        os.path.join(art_dir, r".system_generated\steps\1768\media_0.png"),
        os.path.join(art_dir, "canva_page1_updated.png")
    )
    shutil.copyfile(
        os.path.join(art_dir, r".system_generated\steps\1773\media_0.png"),
        os.path.join(art_dir, "canva_page14_updated.png")
    )
