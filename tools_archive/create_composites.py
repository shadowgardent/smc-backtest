import sys, os, pymupdf
from PIL import Image
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
doc = pymupdf.open(r'C:\Users\ONEST\.gemini\antigravity\brain\a19985bc-fcd1-432f-9cb1-a7239ee1919d\.user_uploaded\media_1791971945863_729dcfef.pdf')

os.makedirs('colon_composites', exist_ok=True)

for page_idx in range(5):
    img_path = f'annot_imgs/page_{page_idx+1}_img_0_1800x2545.png'
    if not os.path.exists(img_path):
        continue
    annot_img = Image.open(img_path).convert('RGB')
    annot_arr = np.array(annot_img)
    page = doc[page_idx]
    
    # Scale matrix
    pw, ph = page.rect.width, page.rect.height
    iw, ih = annot_img.size
    sx, sy = iw / pw, ih / ph
    
    mat = pymupdf.Matrix(sx, sy)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pdf_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if pdf_img.size != annot_img.size:
        pdf_img = pdf_img.resize(annot_img.size)
    
    pdf_arr = np.array(pdf_img)
    
    # Composite: where annot_arr has any ink (e.g. max channel > 40), put annot_arr
    ink_mask = np.max(annot_arr, axis=2) > 40
    comp_arr = pdf_arr.copy()
    comp_arr[ink_mask] = annot_arr[ink_mask]
    comp = Image.fromarray(comp_arr)

    words = page.get_text('words')
    colon_words = [w for w in words if ':' in w[4]]
    
    for idx, cw in enumerate(colon_words):
        x0, y0, x1, y1 = cw[0], cw[1], cw[2], cw[3]
        cx0 = max(0, int((x0 - 80) * sx))
        cy0 = max(0, int((y0 - 25) * sy))
        cx1 = min(iw, int((x1 + 100) * sx))
        cy1 = min(ih, int((y1 + 35) * sy))
        
        crop_comp = comp.crop((cx0, cy0, cx1, cy1))
        comp_name = f'colon_composites/p{page_idx+1}_{idx}.png'
        crop_comp.save(comp_name)
