import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib

# Set Thai font
matplotlib.rcParams['font.family'] = 'Tahoma'

fig, ax = plt.subplots(figsize=(7, 9.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 13.5)
ax.axis('off')

# Style colors matching user image
c_node_bg = '#EDE9FE'      # light purple/lavender
c_node_border = '#A78BFA'  # soft purple border
c_box_bg = '#FEFCE8'       # light yellow/cream
c_box_border = '#CA8A04'   # yellow/gold border
c_arrow = '#4B5563'        # gray arrow
c_text = '#1E1B4B'

# 1. Background subgraph box: "ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม"
box = patches.FancyBboxPatch((2.2, 3.1), 5.6, 8.5,
                             boxstyle="round,pad=0.12,rounding_size=0.15",
                             facecolor=c_box_bg, edgecolor=c_box_border, linewidth=1.2, zorder=1)
ax.add_patch(box)
ax.text(5.0, 11.8, "ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม", ha='center', va='center', fontsize=11, fontweight='bold', color='#451A03', zorder=2)

def draw_node(x, y, w, h, text, shape='rect'):
    if shape == 'circle':
        circle = patches.Circle((x, y), radius=w/2, facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, color=c_text, zorder=4)
    else:
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                     boxstyle="round,pad=0.06,rounding_size=0.08",
                                     facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.2, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9.5, color=c_text, multialignment='center', zorder=4)

# Draw Nodes
draw_node(5.0, 12.6, 1.25, 1.25, "User / นักเทรด", shape='circle')

draw_node(5.0, 10.9, 3.2, 0.7, "Input: ระบุสัญลักษณ์คู่เงิน &\nTimeframe")
draw_node(5.0, 9.6, 3.2, 0.7, "Data Fetching API: ดึงข้อมูล\nราคา OHLCV")
draw_node(5.0, 8.3, 3.2, 0.7, "Algorithm: ประมวลผลจุด\nSwing High / Low")
draw_node(5.0, 7.0, 3.2, 0.7, "Algorithm: ตรวจจับ BOS /\nCHoCH / OB")

# Right branch inside box
draw_node(5.8, 5.5, 3.0, 0.68, "Multi-Timeframe Engine:\nสแกนข้อมูล 7 กรอบเวลา")
draw_node(5.8, 4.2, 3.0, 0.68, "Scoring System: คำนวณ\nทิศทางเทรนด์หลัก")

# Outside bottom
draw_node(4.2, 2.3, 3.2, 0.7, "Web Application: เรนเดอร์\nกราฟ Interactive")
draw_node(5.0, 0.9, 3.4, 0.7, "Output: แสดงผลกราฟ SMC\nและ Dashboard สรุปผล")

def draw_arrow(p1, p2, rad=0.0):
    ax.annotate('', xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="-|>", color=c_arrow, lw=1.2,
                                connectionstyle=f"arc3,rad={rad}",
                                mutation_scale=11),
                zorder=5)

# Arrows
draw_arrow((5.0, 11.95), (5.0, 11.3)) # User -> Input
draw_arrow((5.0, 10.5), (5.0, 10.0))  # Input -> Data Fetch
draw_arrow((5.0, 9.2), (5.0, 8.7))    # Data Fetch -> Swing
draw_arrow((5.0, 7.9), (5.0, 7.4))    # Swing -> BOS

# From BOS/CHoCH to Web App (curved down-left)
draw_arrow((4.2, 6.6), (3.6, 2.7), rad=0.12)

# From BOS/CHoCH to MTF Engine
draw_arrow((5.5, 6.6), (5.8, 5.9))

# MTF Engine -> Scoring
draw_arrow((5.8, 5.1), (5.8, 4.6))

# Scoring -> Web App
draw_arrow((5.4, 3.8), (4.8, 2.7), rad=0.08)

# Web App -> Output
draw_arrow((4.2, 1.9), (4.7, 1.3))

# Output -> User (loop all the way back up on the right)
ax.annotate('', xy=(5.7, 12.6), xytext=(6.8, 0.9),
            arrowprops=dict(arrowstyle="-|>", color=c_arrow, lw=1.2,
                            connectionstyle="arc3,rad=-0.42",
                            mutation_scale=11),
            zorder=5)

plt.tight_layout()
out1 = "e:/Project/smc-backtest-backend/SMC_System_Flow_Word.png"
out2 = "C:/Users/ONEST/Downloads/SMC_System_Flow_Word.png"
plt.savefig(out1, dpi=300, bbox_inches='tight')
plt.savefig(out2, dpi=300, bbox_inches='tight')
print("Successfully generated Thai image:", out1)
