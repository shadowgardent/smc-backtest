import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib

# Set Thai font
matplotlib.rcParams['font.family'] = 'Tahoma'

# Create canvas (width=16 inches, height=8.2 inches at 300 dpi -> 4800 x 2460 px)
fig, ax = plt.subplots(figsize=(16, 8.4), dpi=300)
ax.set_xlim(0, 24)
ax.set_ylim(0, 12.6)
ax.axis('off')

# Color palette from original diagram
c_node_bg = '#EDE9FE'      # Lavender fill (237, 233, 254)
c_node_border = '#8B5CF6'  # Purple border (139, 92, 246)
c_box_border = '#7C7C7C'   # Gray border
c_hdr_bg = '#F5F5F5'       # Light gray header fill
c_line = '#8C8C8C'         # Gray connector line
c_arrow = '#005FB8'        # Blue arrowhead
c_text = '#1F2937'         # Dark gray text

# Helper for drawing node
def draw_rect(x, y, w, h, text, font_size=10.5, font_weight='normal'):
    rect = patches.Rectangle((x - w/2, y - h/2), w, h,
                             facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.4, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=font_size, fontweight=font_weight,
            color=c_text, multialignment='center', zorder=4)

# Helper for drawing paths
def draw_arrow(pts):
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        is_last = (i == len(pts) - 2)
        if is_last:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>", color=c_arrow,
                                        edgecolor=c_arrow, facecolor=c_arrow,
                                        lw=1.4, shrinkA=0, shrinkB=0,
                                        mutation_scale=13),
                        zorder=5)
        else:
            ax.plot([x1, x2], [y1, y2], color=c_line, lw=1.4, zorder=5)

# 1. Main Subgraph Box (ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม)
# x from 4.6 to 18.2, y from 2.6 to 11.8
c_left, c_bottom, c_w, c_h = 4.4, 2.5, 13.8, 9.3
container = patches.Rectangle((c_left, c_bottom), c_w, c_h,
                              facecolor='none', edgecolor=c_box_border, linewidth=1.4, zorder=1)
ax.add_patch(container)

# Header
hdr_h = 0.75
hdr = patches.Rectangle((c_left, c_bottom + c_h - hdr_h), c_w, hdr_h,
                        facecolor=c_hdr_bg, edgecolor=c_box_border, linewidth=1.4, zorder=1)
ax.add_patch(hdr)
ax.text(c_left + 0.35, c_bottom + c_h - hdr_h/2, "ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม",
        ha='left', va='center', fontsize=11.5, fontweight='bold', color=c_text, zorder=2)

# Left: User
u_cx, u_cy = 2.2, 9.4
u_r = 1.45
user_circle = patches.Circle((u_cx, u_cy), radius=u_r,
                             facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.4, zorder=3)
ax.add_patch(user_circle)
ax.text(u_cx, u_cy, "User /\nนักเทรด", ha='center', va='center', fontsize=11.5, fontweight='bold', color=c_text, zorder=4)

# Top row inside container: y = 9.4
y_top = 9.4
node_w = 3.0
node_h = 1.3

x_n1 = 6.2
x_n2 = 9.8
x_n3 = 13.4
x_n4 = 16.8

draw_rect(x_n1, y_top, node_w, node_h, "Input:\nระบุสัญลักษณ์คู่เงิน\n& Timeframe", font_size=10)
draw_rect(x_n2, y_top, node_w, node_h, "Data Fetching API:\nดึงข้อมูลราคา\nOHLCV", font_size=10)
draw_rect(x_n3, y_top, node_w, node_h, "Algorithm:\nประมวลผลจุด\nSwing High / Low", font_size=10)
draw_rect(x_n4, y_top, node_w - 0.2, node_h, "Algorithm:\nตรวจจับ BOS /\nCHoCH / OB", font_size=10)

# Bottom row inside container: y = 5.2
y_bot = 5.2
x_n5 = 12.0
x_n6 = 16.4
node_w_bot = 3.6
draw_rect(x_n5, y_bot, node_w_bot, node_h, "Multi-Timeframe Engine:\nสแกนข้อมูล 7 กรอบเวลา", font_size=10)
draw_rect(x_n6, y_bot, node_w_bot, node_h, "Scoring System:\nคำนวณทิศทางเทรนด์หลัก", font_size=10)

# Outside Right: Web App and Output
x_right = 21.1
y_n7 = 9.4
y_n8 = 5.2
node_w_out = 3.9
draw_rect(x_right, y_n7, node_w_out, node_h, "Web Application:\nเรนเดอร์กราฟ Interactive", font_size=10.5)
draw_rect(x_right, y_n8, node_w_out, node_h, "Output:\nแสดงผลกราฟ SMC\nและ Dashboard สรุปผล", font_size=10.5)

# Connections:
# User -> Node 1
draw_arrow([(u_cx + u_r, u_cy), (x_n1 - node_w/2, y_top)])

# Node 1 -> Node 2
draw_arrow([(x_n1 + node_w/2, y_top), (x_n2 - node_w/2, y_top)])

# Node 2 -> Node 3
draw_arrow([(x_n2 + node_w/2, y_top), (x_n3 - node_w/2, y_top)])

# Node 3 -> Node 4
draw_arrow([(x_n3 + node_w/2, y_top), (x_n4 - (node_w - 0.2)/2, y_top)])

# Node 4 -> Web App (Straight top connection)
draw_arrow([(x_n4 + (node_w - 0.2)/2, y_top), (x_right - node_w_out/2, y_n7)])

# Node 4 -> Node 5 (Branch down-left)
draw_arrow([(x_n4, y_top - node_h/2),
            (x_n4, 7.3),
            (x_n5, 7.3),
            (x_n5, y_bot + node_h/2)])

# Node 5 -> Node 6
draw_arrow([(x_n5 + node_w_bot/2, y_bot), (x_n6 - node_w_bot/2, y_bot)])

# Node 6 -> Web App (Routing to Web App bottom-left)
draw_arrow([(x_n6 + node_w_bot/2, y_bot),
            (19.0, y_bot),
            (19.0, y_n7 - 0.3),
            (x_right - node_w_out/2, y_n7 - 0.3)])

# Web App -> Output
draw_arrow([(x_right, y_n7 - node_h/2), (x_right, y_n8 + node_h/2)])

# Output -> User (Loop back along the bottom)
y_loop = 1.2
draw_arrow([(x_right, y_n8 - node_h/2),
            (x_right, y_loop),
            (u_cx, y_loop),
            (u_cx, u_cy - u_r)])

plt.tight_layout()
out1 = "e:/Project/smc-backtest-backend/SMC_Dataflow_Horizontal_Word.png"
out2 = "C:/Users/ONEST/Downloads/SMC_Dataflow_Horizontal_Word.png"
plt.savefig(out1, dpi=300, bbox_inches='tight')
plt.savefig(out2, dpi=300, bbox_inches='tight')
print("Successfully generated exact horizontal flow!")
