import fitz
from PIL import Image
import numpy as np

pdf_path = r"C:\Users\ONEST\Downloads\Untitled 1.pdf"
doc = fitz.open(pdf_path)
page = doc[0]

# Render at 4.5x zoom for extreme crispness (~350 DPI)
zoom = 4.5
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat, alpha=False)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Diagram bounds were: X=(381, 3199) Y=(432, 2022) at zoom 4.0
# At zoom 4.5, scale coordinates by 4.5 / 4.0 = 1.125
scale = 4.5 / 4.0
x1 = int(381 * scale)
x2 = int(3199 * scale)
y1 = int(432 * scale)
y2 = int(2022 * scale)

# Add 45px padding
pad = 45
crop_box = (max(0, x1 - pad), max(0, y1 - pad), min(img.width, x2 + pad), min(img.height, y2 + pad))
cropped = img.crop(crop_box)
print("Cropped dimensions:", cropped.size)

# 1. Save Original Miro Colors (Cropped cleanly)
out_orig_dl = r"C:\Users\ONEST\Downloads\SMC_Architecture_Flow_Original.png"
out_orig_ws = r"e:\Project\smc-backtest-backend\SMC_Architecture_Flow_Original.png"
cropped.save(out_orig_dl, dpi=(300, 300))
cropped.save(out_orig_ws, dpi=(300, 300))

# 2. Pure White Background Version (Best for Word/Paper)
arr = np.array(cropped).astype(float)
# The background is around (242, 242, 242)
# Any pixel where min(R, G, B) >= 238 should be pure white (255, 255, 255)
# Linearly stretch pixels from [0, 242] to [0, 255]
# v_out = 255 - (242 - v) * (255 / 242)
bg_level = 241.0
arr_norm = np.clip(arr, 0, bg_level)
arr_white = arr_norm * (255.0 / bg_level)
arr_white = np.clip(arr_white, 0, 255).astype(np.uint8)

img_white = Image.fromarray(arr_white)
out_white_dl = r"C:\Users\ONEST\Downloads\SMC_Architecture_Flow_White.png"
out_white_ws = r"e:\Project\smc-backtest-backend\SMC_Architecture_Flow_White.png"
img_white.save(out_white_dl, dpi=(300, 300))
img_white.save(out_white_ws, dpi=(300, 300))

# Also copy to artifacts directory for preview
out_art = r"C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d\SMC_Architecture_Flow_White.png"
img_white.save(out_art, dpi=(300, 300))

print("Successfully generated all versions!")
print("White version size:", img_white.size)
