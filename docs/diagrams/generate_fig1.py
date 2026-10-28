import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def generate_figure_1():
    # Set up figure
    fig, ax = plt.subplots(figsize=(8, 10.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 130)
    ax.axis('off')
    
    # Colors
    c_bg_sec = '#F1F5F9'       # Light slate
    c_border_sec = '#94A3B8'   # Slate border
    c_header_sec = '#1E293B'   # Dark slate text
    
    c_box_bg = '#FFFFFF'       # White
    c_box_border = '#2563EB'   # Royal blue border
    c_text_main = '#0F172A'    # Near black text
    c_text_sub = '#334155'     # Slate text
    c_arrow = '#2563EB'        # Blue arrow
    
    # Helper to draw rounded box
    def draw_box(x, y, w, h, bg_color, border_color, lw=1.5, radius=1.5):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.2,rounding_size={radius}",
                                     facecolor=bg_color, edgecolor=border_color, linewidth=lw, zorder=2)
        ax.add_patch(box)

    # Helper for arrow
    def draw_arrow(x1, y1, x2, y2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=c_arrow, edgecolor=c_arrow, width=2.0, headwidth=8, headlength=8, shrink=0.05),
                    zorder=5)

    # -------------------------------------------------------------
    # 1. Section 1: Input (Y: 110 to 128)
    # -------------------------------------------------------------
    draw_box(6, 111, 88, 16, c_bg_sec, c_border_sec, lw=1.5, radius=1.5)
    ax.text(9, 123.5, "1. ส่วนรับข้อมูล (Input)", fontsize=13, fontweight='bold', color=c_header_sec, fontname='Tahoma', zorder=3)
    
    draw_box(12, 113, 76, 8, c_box_bg, c_box_border, lw=1.8, radius=1.2)
    ax.text(50, 117, "ผู้ใช้งานเลือกคู่เงิน (Symbol) และกรอบเวลา (Timeframe)", fontsize=11, fontweight='bold',
            ha='center', va='center', color=c_text_main, fontname='Tahoma', zorder=4)

    draw_arrow(50, 111, 50, 105)

    # -------------------------------------------------------------
    # 2. Section 2: Processing Engine (Y: 34 to 105)
    # -------------------------------------------------------------
    draw_box(6, 35, 88, 70, c_bg_sec, c_border_sec, lw=1.5, radius=1.5)
    ax.text(9, 101.5, "2. ส่วนประมวลผล (Processing Engine)", fontsize=13, fontweight='bold', color=c_header_sec, fontname='Tahoma', zorder=3)
    
    # Step 1
    draw_box(12, 88, 76, 9.5, c_box_bg, c_box_border, lw=1.8, radius=1.2)
    ax.text(50, 93.8, "Data Fetching API", fontsize=11.5, fontweight='bold', ha='center', va='center', color='#1D4ED8', fontname='Tahoma', zorder=4)
    ax.text(50, 90.2, "ดึงข้อมูลราคา OHLCV ผ่าน MetaTrader 5", fontsize=10.5, ha='center', va='center', color=c_text_sub, fontname='Tahoma', zorder=4)
    
    draw_arrow(50, 88, 50, 82)

    # Step 2
    draw_box(12, 72.5, 76, 9.5, c_box_bg, c_box_border, lw=1.8, radius=1.2)
    ax.text(50, 78.3, "Swing Detection", fontsize=11.5, fontweight='bold', ha='center', va='center', color='#1D4ED8', fontname='Tahoma', zorder=4)
    ax.text(50, 74.7, "ตรวจจับจุดสวิง Swing High และ Swing Low", fontsize=10.5, ha='center', va='center', color=c_text_sub, fontname='Tahoma', zorder=4)

    draw_arrow(50, 72.5, 50, 66.5)

    # Step 3
    draw_box(12, 57, 76, 9.5, c_box_bg, c_box_border, lw=1.8, radius=1.2)
    ax.text(50, 62.8, "Structure & Zone Detection", fontsize=11.5, fontweight='bold', ha='center', va='center', color='#1D4ED8', fontname='Tahoma', zorder=4)
    ax.text(50, 59.2, "ตรวจจับสัญญาณ BOS, CHoCH และระบุ Order Block", fontsize=10.5, ha='center', va='center', color=c_text_sub, fontname='Tahoma', zorder=4)

    draw_arrow(50, 57, 50, 51)

    # Step 4
    draw_box(12, 40, 76, 11, c_box_bg, c_box_border, lw=1.8, radius=1.2)
    ax.text(50, 47, "Multi-Timeframe Scoring Model", fontsize=11.5, fontweight='bold', ha='center', va='center', color='#1D4ED8', fontname='Tahoma', zorder=4)
    ax.text(50, 43, "คำนวณคะแนนทิศทางตลาดและถ่วงน้ำหนัก 7 กรอบเวลา", fontsize=10.5, ha='center', va='center', color=c_text_sub, fontname='Tahoma', zorder=4)

    # Arrows from Section 2 to Section 3
    # Two arrows branching down to the two output boxes
    draw_arrow(32, 35, 32, 27)
    draw_arrow(68, 35, 68, 27)

    # -------------------------------------------------------------
    # 3. Section 3: Output Visualization (Y: 2 to 27)
    # -------------------------------------------------------------
    draw_box(6, 2, 88, 25, c_bg_sec, c_border_sec, lw=1.5, radius=1.5)
    ax.text(9, 23.5, "3. ส่วนแสดงผล (Output Visualization)", fontsize=13, fontweight='bold', color=c_header_sec, fontname='Tahoma', zorder=3)

    # Output Box 1 (Left)
    draw_box(10, 5.5, 38, 14.5, c_box_bg, '#059669', lw=1.8, radius=1.2)
    ax.text(29, 15.5, "Interactive Chart", fontsize=11, fontweight='bold', ha='center', va='center', color='#047857', fontname='Tahoma', zorder=4)
    ax.text(29, 11.5, "กราฟแท่งเทียนเชิงโต้ตอบ\n+ เลเยอร์ SMC อัตโนมัติ", fontsize=9.5, ha='center', va='center', color=c_text_main, fontname='Tahoma', zorder=4)

    # Output Box 2 (Right)
    draw_box(52, 5.5, 38, 14.5, c_box_bg, '#7C3AED', lw=1.8, radius=1.2)
    ax.text(71, 15.5, "Multi-TF Dashboard", fontsize=11, fontweight='bold', ha='center', va='center', color='#6D28D9', fontname='Tahoma', zorder=4)
    ax.text(71, 11.5, "กระดานสรุปสถานะตลาด\nทิศทางและคะแนน 7 กรอบเวลา", fontsize=9.5, ha='center', va='center', color=c_text_main, fontname='Tahoma', zorder=4)

    plt.tight_layout()
    plt.savefig('new_figure_1.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated new_figure_1.png successfully!")

if __name__ == '__main__':
    generate_figure_1()
