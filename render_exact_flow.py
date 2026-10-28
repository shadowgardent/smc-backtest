import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib

# Set high quality rendering
matplotlib.rcParams['font.family'] = 'Tahoma'

# Original dimensions were 368 x 725
# We can create a canvas using the exact coordinate space (0 to 368, 0 to 725)
# Inverting Y so that y=0 is top and y=725 is bottom for convenience

fig, ax = plt.subplots(figsize=(6, 11.8), dpi=300)
ax.set_xlim(0, 368)
ax.set_ylim(725, 0) # Inverted Y so top is 0, bottom is 725
ax.axis('off')

# Color palette (Exact matches)
c_node_bg = '#EDE9FE'      # (237, 233, 254)
c_node_border = '#8B5CF6'  # (139, 92, 246)
c_container_border = '#7C7C7C' # (124, 124, 124)
c_hdr_bg = '#F5F5F5'       # (245, 245, 245)
c_line = '#8C8C8C'         # gray connector
c_arrow = '#005FB8'        # blue arrowhead
c_text = '#262626'

# 1. Container (ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม)
# x=(18, 356) -> left=18, width=338
# y=(19, 438) -> top=19, height=419
c_left, c_top, c_w, c_h = 18, 19, 338, 419
container_rect = patches.Rectangle((c_left, c_top), c_w, c_h,
                                   facecolor='none', edgecolor=c_container_border, linewidth=1.2, zorder=1)
ax.add_patch(container_rect)

# Header (y=19 to 41 -> height 22)
hdr_h = 22
hdr_rect = patches.Rectangle((c_left, c_top), c_w, hdr_h,
                             facecolor=c_hdr_bg, edgecolor=c_container_border, linewidth=1.2, zorder=1)
ax.add_patch(hdr_rect)
ax.text(c_left + 7, c_top + hdr_h/2 + 1, "ระบบวิเคราะห์ SMC ด้วยอัลกอริทึม",
        ha='left', va='center', fontsize=7.5, color=c_text, zorder=2)

# Helper to draw rectangle node
def draw_rect(x, y, w, h, text, font_size=7.5):
    # (x, y) is top-left
    rect = patches.Rectangle((x, y), w, h,
                             facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.2, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=font_size, color=c_text, zorder=4)

# Helper to draw line and arrow
def draw_path(pts, has_arrow=True):
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        is_last = (i == len(pts) - 2) and has_arrow
        if is_last:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="-|>", color=c_arrow,
                                        edgecolor=c_arrow, facecolor=c_arrow,
                                        lw=1.0, shrinkA=0, shrinkB=0,
                                        mutation_scale=9),
                        zorder=5)
        else:
            ax.plot([x1, x2], [y1, y2], color=c_line, lw=1.0, zorder=5)

# 2. Nodes
# Node 1: y=(56, 83), x=(113, 342) -> w=229, h=27
draw_rect(113, 56, 229, 27, "Input: ระบุสัญลักษณ์คู่เงิน & Timeframe")

# Node 2: y=(123, 150), x=(114, 341) -> w=227, h=27
draw_rect(114, 123, 227, 27, "Data Fetching API: ดึงข้อมูลราคา OHLCV")

# Node 3: y=(189, 216), x=(118, 337) -> w=219, h=27
draw_rect(118, 189, 219, 27, "Algorithm: ประมวลผลจุด Swing High / Low")

# Node 4: y=(256, 283), x=(128, 328) -> w=200, h=27
draw_rect(128, 256, 200, 27, "Algorithm: ตรวจจับ BOS / CHoCH / OB")

# Node 5: y=(322, 349), x=(33, 286) -> w=253, h=27
draw_rect(33, 322, 253, 27, "Multi-Timeframe Engine: สแกนข้อมูล 7 กรอบเวลา")

# Node 6: y=(389, 416), x=(46, 274) -> w=228, h=27
draw_rect(46, 389, 228, 27, "Scoring System: คำนวณทิศทางเทรนด์หลัก")

# Node 7: y=(468, 495), x=(99, 326) -> w=227, h=27
draw_rect(99, 468, 227, 27, "Web Application: เรนเดอร์กราฟ Interactive")

# Node 8: y=(535, 561), x=(85, 340) -> w=255, h=26
draw_rect(85, 535, 255, 26, "Output: แสดงผลกราฟ SMC และ Dashboard สรุปผล")

# Node 9: User circle at bottom left
# Center: x=105, y=656, radius=55
u_cx, u_cy, u_r = 105, 656, 55
user_circle = patches.Circle((u_cx, u_cy), radius=u_r,
                             facecolor=c_node_bg, edgecolor=c_node_border, linewidth=1.2, zorder=3)
ax.add_patch(user_circle)
ax.text(u_cx, u_cy, "User / นักเทรด", ha='center', va='center', fontsize=8, color=c_text, zorder=4)

# 3. Connections
# Node 1 -> Node 2
draw_path([(228, 83), (228, 123)])

# Node 2 -> Node 3
draw_path([(228, 150), (228, 189)])

# Node 3 -> Node 4
draw_path([(228, 216), (228, 256)])

# Node 4 -> Node 5 (branch left)
# leaves Node 4 at x=228, goes down to y=303, turns left to x=160, goes down to y=322
draw_path([(228, 283), (228, 303), (160, 303), (160, 322)])

# Node 4 -> Node 7 (bypass right)
# leaves Node 4 at x=213 (or x=212), goes down all the way to Node 7 top at (213, 468)
draw_path([(213, 283), (213, 468)])

# Node 5 -> Node 6
draw_path([(160, 349), (160, 389)])

# Node 6 -> Node 7
# leaves Node 6 at x=160, goes down to y=456, turns right to x=174, goes down to y=468
draw_path([(160, 416), (160, 456), (174, 456), (174, 468)])

# Node 7 -> Node 8
draw_path([(213, 495), (213, 535)])

# Node 8 -> User
# leaves Node 8 at x=213, y=561, goes down to y=591, turns left to x=124, goes down to circle top (124, 604)
# calculate exact circle top at x=124: y = u_cy - sqrt(r^2 - (124-105)^2) = 656 - sqrt(3025 - 361) = 656 - 51.6 = 604.4
draw_path([(213, 561), (213, 591), (124, 591), (124, 604)])

# User -> Node 1 (loop up to top)
# leaves circle top-left at x=86: y = 656 - sqrt(3025 - (86-105)^2) = 656 - 51.6 = 604.4
# goes up to y=591, turns left to x=11, goes up along x=11 to y=10, turns right to x=228, goes down to top of Node 1 at y=56
draw_path([(86, 604), (86, 591), (11, 591), (11, 10), (228, 10), (228, 56)])

plt.tight_layout()
out_backend = "e:/Project/smc-backtest-backend/SMC_Dataflow_System_Process.png"
out_downloads = "C:/Users/ONEST/Downloads/SMC_Dataflow_System_Process.png"
plt.savefig(out_backend, dpi=300, bbox_inches='tight')
plt.savefig(out_downloads, dpi=300, bbox_inches='tight')
print("Successfully generated high-res PNG:")
print("1.", out_backend)
print("2.", out_downloads)
