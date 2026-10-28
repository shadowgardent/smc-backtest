import fitz

doc = fitz.open(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Checked.pdf")
print("Total pages in PDF:", len(doc))

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_name = f"e:/Project/smc-backtest-backend/check_page_{i+1}.png"
    pix.save(out_name)
    print(f"Saved page {i+1} to {out_name}")
