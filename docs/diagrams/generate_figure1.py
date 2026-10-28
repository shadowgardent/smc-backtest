import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create crisp figure for Figure 1 (Architecture)
plt.rcParams['font.family'] = 'Leelawadee UI'

fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10.5)
ax.axis('off')

# Colors
c_input_border = '#3b82f6'
c_input_fill = '#eff6ff'
c_proc_border = '#8b5cf6'
c_proc_fill = '#f5f3ff'
c_out_border = '#10b981'
c_out_fill = '#ecfdf5'
c_box_border = '#64748b'
c_box_fill = '#ffffff'
c_text_main = '#1e293b'

# Subgraph 1: Input
g1 = patches.FancyBboxPatch((1.2, 8.8), 7.6, 1.3, boxstyle="round,pad=0.2",
                           edgecolor=c_input_border, facecolor=c_input_fill, linewidth=1.8, linestyle='--')
ax.add_patch(g1)
ax.text(1.5, 9.8, "1. ส่วนรับข้อมูล (Input)", fontsize=11, fontweight='bold', color='#1d4ed8')
b_input = patches.FancyBboxPatch((1.5, 8.9), 7.0, 0.75, boxstyle="round,pad=0.1",
                                edgecolor='#93c5fd', facecolor='#ffffff', linewidth=1.2)
ax.add_patch(b_input)
ax.text(5.0, 9.27, "ผู้ใช้งานระบุคู่เงิน (Symbol) และกรอบเวลา (Timeframe)", fontsize=10.5, ha='center', va='center', color=c_text_main)

# Arrow 1 -> Process
ax.annotate('', xy=(5.0, 8.1), xytext=(5.0, 8.8),
            arrowprops=dict(facecolor='#64748b', edgecolor='#64748b', width=1.8, headwidth=7, headlength=7))

# Subgraph 2: Processing Engine
g2 = patches.FancyBboxPatch((0.8, 3.4), 8.4, 4.6, boxstyle="round,pad=0.2",
                           edgecolor=c_proc_border, facecolor=c_proc_fill, linewidth=1.8, linestyle='--')
ax.add_patch(g2)
ax.text(1.1, 7.7, "2. ส่วนประมวลผล (Processing Engine)", fontsize=11, fontweight='bold', color='#6d28d9')

proc_boxes = [
    ("A. Data Fetching API: ดึงข้อมูล OHLCV ผ่าน MetaTrader 5 (MT5)", 7.05),
    ("B. Swing Detection: ตรวจจับจุด Swing High / Swing Low (Look-back / Forward)", 6.15),
    ("C. Structure & Zone: ตรวจจับ BOS, CHoCH, Order Block และ FVG", 5.25),
    ("D. Multi-Timeframe Engine: วิเคราะห์ & คำนวณคะแนนถ่วงน้ำหนัก 7 กรอบเวลา", 4.35)
]

for label, y in proc_boxes:
    box = patches.FancyBboxPatch((1.1, y - 0.35), 7.8, 0.7, boxstyle="round,pad=0.1",
                                edgecolor='#c4b5fd', facecolor='#ffffff', linewidth=1.2)
    ax.add_patch(box)
    ax.text(5.0, y, label, fontsize=9.8, ha='center', va='center', color=c_text_main)

# Internal arrows inside Process
for y_from, y_to in [(6.7, 6.5), (5.8, 5.6), (4.9, 4.7)]:
    ax.annotate('', xy=(5.0, y_to), xytext=(5.0, y_from),
                arrowprops=dict(facecolor='#8b5cf6', edgecolor='#8b5cf6', width=1.2, headwidth=5, headlength=5))

# Branch arrows to Output
# Left arrow: from Structure (C) to Interactive Chart
ax.annotate('', xy=(3.0, 2.5), xytext=(3.0, 3.4),
            arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=1.5, headwidth=6, headlength=6))

# Right arrow: from MTFA (D) to Dashboard
ax.annotate('', xy=(7.0, 2.5), xytext=(7.0, 3.4),
            arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=1.5, headwidth=6, headlength=6))

# Subgraph 3: Output
g3 = patches.FancyBboxPatch((0.8, 0.4), 8.4, 2.0, boxstyle="round,pad=0.2",
                           edgecolor=c_out_border, facecolor=c_out_fill, linewidth=1.8, linestyle='--')
ax.add_patch(g3)
ax.text(1.1, 2.1, "3. ส่วนแสดงผล (Output Visualization)", fontsize=11, fontweight='bold', color='#047857')

# Out Box 1
b_out1 = patches.FancyBboxPatch((1.1, 0.6), 3.7, 1.25, boxstyle="round,pad=0.1",
                               edgecolor='#a7f3d0', facecolor='#ffffff', linewidth=1.2)
ax.add_patch(b_out1)
ax.text(2.95, 1.35, "กราฟแท่งเทียนเชิงโต้ตอบ\n(TradingView + Canvas Overlay)", fontsize=9.5, ha='center', va='center', fontweight='bold', color=c_text_main)
ax.text(2.95, 0.85, "พล็อตเส้น Swing, BOS, CHoCH\nและกล่อง Order Block, FVG", fontsize=8.2, ha='center', va='center', color='#475569')

# Out Box 2
b_out2 = patches.FancyBboxPatch((5.2, 0.6), 3.7, 1.25, boxstyle="round,pad=0.1",
                               edgecolor='#a7f3d0', facecolor='#ffffff', linewidth=1.2)
ax.add_patch(b_out2)
ax.text(7.05, 1.35, "กระดานสรุปผลแนวโน้ม\n(Multi-TF Dashboard)", fontsize=9.5, ha='center', va='center', fontweight='bold', color=c_text_main)
ax.text(7.05, 0.85, "Market Matrix 7 กรอบเวลา\nและ H4 Setup Radar", fontsize=8.2, ha='center', va='center', color='#475569')

plt.tight_layout()
out_file = r"C:\Users\ONEST\Downloads\ภาพที่1_แผนภาพการทำงานของระบบ.png"
fig.savefig(out_file, dpi=300, bbox_inches='tight')
print("Successfully generated high-res Figure 1 at:", out_file)
