import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib

# Set Thai font
matplotlib.rcParams['font.family'] = 'Tahoma'

# Set high-res canvas (width=8, height=12 at 300 dpi -> 2400 x 3600 px)
fig, ax = plt.subplots(figsize=(7, 10.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 15)
ax.axis('off')

# Color palette from original image
c_node_bg = '#EDE9FE'      # Light purple/lavender
c_node_border = '#8B5CF6'  # Purple border
c_box_border = '#7C7C7C'   # Gray border
c_box_hdr_bg = '#F5F5F5'   # Light gray header fill
c_line = '#8C8C8C'         # Gray connector line
c_arrowhead = '#005FB8'    # Blue arrowhead
c_text = '#262626'         # Dark gray text

# Coordinates setup
cx = 5.2 # main center x
node_w = 4.2
node_h = 0.65

# 1. Main Subgraph Box (ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม)
# x from 2.0 to 8.4, y from 5.4 to 14.1
box_left, box_bottom, box_w, box_h = 1.9, 5.7, 6.6, 8.4
# Main container border
container = patches.Rectangle((box_left, box_bottom), box_w, box_h,
                              facecolor='none', edgecolor=c_box_border, linewidth=1.2, zorder=1)
ax.add_patch(container)

# Header bar
hdr_h = 0.55
hdr_rect = patches.Rectangle((box_left, box_bottom + box_h - hdr_h), box_w, hdr_h,
                             facecolor=c_box_hdr_bg, edgecolor=c_box_border, linewidth=1.2, zorder=1)
ax.add_patch(hdr_rect)
ax.text(box_left + 0.15, box_bottom + box_h - hdr_h/2, "ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม",
        ha='left', va='center', fontsize=9.5, color=c_text, zorder=2)

# Helper function to draw node
def draw_rect_node(x, y, w, h, text):
    rect = patches.Rectangle((x - w/2, y - h/2), w, h,
                             facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.2, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=9.5, color=c_text, zorder=4)

# 2. Nodes inside container
y_n1 = 12.9
y_n2 = 11.4
y_n3 = 9.9
y_n4 = 8.4

draw_rect_node(cx, y_n1, node_w, node_h, "Input: ระบุสัญลักษณ์คู่เงิน & Timeframe")
draw_rect_node(cx, y_n2, node_w, node_h, "Data Fetching API: ดึงข้อมูลราคา OHLCV")
draw_rect_node(cx, y_n3, node_w, node_h, "Algorithm: ประมวลผลจุด Swing High / Low")
draw_rect_node(cx, y_n4, node_w, node_h, "Algorithm: ตรวจจับ BOS / CHoCH / OB")

# Node 5 and 6 (shifted left)
cx_mtf = 4.0
w_mtf = 4.6
y_n5 = 6.9
y_n6 = 5.6
# Wait, let's adjust container bottom so node 5 and 6 are inside!
draw_rect_node(cx_mtf, y_n5, w_mtf, node_h, "Multi-Timeframe Engine: สแกนข้อมูล 7 กรอบเวลา")
draw_rect_node(cx_mtf, y_n6, w_mtf, node_h, "Scoring System: คำนวณทิศทางเทรนด์หลัก")

# 3. Nodes outside container (below)
y_n7 = 4.1
y_n8 = 2.8
draw_rect_node(cx, y_n7, node_w, node_h, "Web Application: เรนเดอร์กราฟ Interactive")
draw_rect_node(cx, y_n8, node_w + 0.4, node_h, "Output: แสดงผลกราฟ SMC และ Dashboard สรุปผล")

# 4. User Circle at the bottom
y_user = 0.95
r_user = 1.05
user_circle = patches.Circle((cx, y_user), radius=r_user,
                             facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.2, zorder=3)
ax.add_patch(user_circle)
ax.text(cx, y_user, "User / นักเทรด", ha='center', va='center', fontsize=10, color=c_text, zorder=4)

# Helper function to draw orthogonal lines with arrowhead
def draw_arrow_step(pts):
    # pts is list of (x, y)
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        is_last = (i == len(pts) - 2)
        if is_last:
            # Draw line up to target and add blue arrowhead
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>", color=c_arrowhead,
                                        edgecolor=c_arrowhead,
                                        facecolor=c_arrowhead,
                                        lw=1.0,
                                        shrinkA=0, shrinkB=0,
                                        mutation_scale=10),
                        zorder=5)
        else:
            ax.plot([x1, x2], [y1, y2], color=c_line, lw=1.0, zorder=5)

# 5. Connector lines & arrows
# Node 1 -> Node 2
draw_arrow_step([(cx, y_n1 - node_h/2), (cx, y_n2 + node_h/2)])

# Node 2 -> Node 3
draw_arrow_step([(cx, y_n2 - node_h/2), (cx, y_n3 + node_h/2)])

# Node 3 -> Node 4
draw_arrow_step([(cx, y_n3 - node_h/2), (cx, y_n4 + node_h/2)])

# Node 4 -> Node 5 (branch left)
x_branch_left = cx - 0.4
draw_arrow_step([(x_branch_left, y_n4 - node_h/2),
                 (x_branch_left, y_n4 - node_h/2 - 0.35),
                 (cx_mtf, y_n4 - node_h/2 - 0.35),
                 (cx_mtf, y_n5 + node_h/2)])

# Node 4 -> Node 7 (bypass right straight down)
x_bypass = cx + 0.4
draw_arrow_step([(x_bypass, y_n4 - node_h/2),
                 (x_bypass, y_n7 + node_h/2)])

# Node 5 -> Node 6
draw_arrow_step([(cx_mtf, y_n5 - node_h/2), (cx_mtf, y_n6 + node_h/2)])

# Node 6 -> Node 7
draw_arrow_step([(cx_mtf, y_n6 - node_h/2),
                 (cx_mtf, y_n7 + node_h/2 + 0.35),
                 (cx - 0.4, y_n7 + node_h/2 + 0.35),
                 (cx - 0.4, y_n7 + node_h/2)])

# Node 7 -> Node 8
draw_arrow_step([(cx, y_n7 - node_h/2), (cx, y_n8 + node_h/2)])

# Node 8 -> User
draw_arrow_step([(cx, y_n8 - node_h/2), (cx, y_user + r_user)])

# User -> Node 1 (loop all the way around left)
# Leaves top-left of circle, goes to x_lane, goes up to y_top, goes to cx, points into top of Node 1
x_lane = 1.3
y_top = box_bottom + box_h + 0.35
# circle top-left intersection approx
user_exit_x = cx - r_user * 0.707
user_exit_y = y_user + r_user * 0.707
draw_arrow_step([(user_exit_x, user_exit_y),
                 (x_lane, user_exit_y),
                 (x_lane, y_top),
                 (cx, y_top),
                 (cx, y_n1 + node_h/2)])

plt.tight_layout()
out1 = "e:/Project/smc-backtest-backend/SMC_Dataflow_System_Process.png"
out2 = "C:/Users/ONEST/Downloads/SMC_Dataflow_System_Process.png"
plt.savefig(out1, dpi=300, bbox_inches='tight')
plt.savefig(out2, dpi=300, bbox_inches='tight')
print("Successfully generated:", out1)
