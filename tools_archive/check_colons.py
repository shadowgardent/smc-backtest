import sys, os, pymupdf
from PIL import Image
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
doc = pymupdf.open(r'C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d\.user_uploaded\media_1791971945863_729dcfef.pdf')

os.makedirs('colon_crops', exist_ok=True)

results = []

for page_idx in range(5):
    img_path = f'annot_imgs/page_{page_idx+1}_img_0_1800x2545.png'
    if not os.path.exists(img_path):
        continue
    annot_img = Image.open(img_path).convert('RGBA')
    page = doc[page_idx]
    pw, ph = page.rect.width, page.rect.height
    iw, ih = annot_img.size
    sx, sy = iw / pw, ih / ph

    words = page.get_text('words')
    colon_words = [w for w in words if ':' in w[4]]
    
    for idx, cw in enumerate(colon_words):
        x0, y0, x1, y1 = cw[0], cw[1], cw[2], cw[3]
        cx0 = max(0, int((x0 - 10) * sx))
        cy0 = max(0, int((y0 - 15) * sy))
        cx1 = min(iw, int((x1 + 30) * sx))
        cy1 = min(ih, int((y1 + 20) * sy))
        
        crop = annot_img.crop((cx0, cy0, cx1, cy1))
        arr = np.array(crop)
        
        # Check non-transparent pixels and colors
        alpha = arr[:, :, 3]
        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]
        
        # In this overlay, background might be transparent or white? Let's check:
        # Actually let's check what the background of annot_img is
        blue_mask = (b > 120) & (b > r + 30)
        blue_count = int(np.sum(blue_mask))
        
        clean_word = "".join(c for c in cw[4] if c.isalnum() or c in "()_")
        crop_name = f'colon_crops/p{page_idx+1}_{idx}_{clean_word}.png'
        crop.save(crop_name)
        
        # also get line context
        results.append({
            'page': page_idx + 1,
            'word': cw[4],
            'blue_pixels': blue_count,
            'crop': crop_name,
            'bbox': (cw[0], cw[1], cw[2], cw[3])
        })

print(f"Total colon occurrences checked: {len(results)}")
for r in results:
    marked = " [MARKED FOR DELETION]" if r['blue_pixels'] > 15 else " [clean]"
    print(f"Page {r['page']} | Word: {r['word']:<35} | Blue pixels: {r['blue_pixels']:<5} {marked}")
