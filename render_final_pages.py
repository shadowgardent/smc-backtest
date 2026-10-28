import fitz

doc = fitz.open(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.pdf")
print("Total PDF pages:", len(doc))

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_name = f"e:/Project/smc-backtest-backend/final_eval_page_{i+1}.png"
    pix.save(out_name)
    print(f"Rendered Page {i+1}: {out_name}")
