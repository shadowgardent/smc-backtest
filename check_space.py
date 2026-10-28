from PIL import Image

# Check page 2 bottom whitespace
im2 = Image.open("e:/Project/smc-backtest-backend/check_page_2.png")
w, h = im2.size
# Check lowest non-white pixel on page 2
dark_ys = [y for y in range(h) for x in range(w) if im2.getpixel((x, y))[0] < 200]
print("Page 2 max y:", max(dark_ys), "out of", h, f"({max(dark_ys)/h*100:.1f}%)")

# Check page 5 bottom whitespace
im5 = Image.open("e:/Project/smc-backtest-backend/check_page_5.png")
dark_ys5 = [y for y in range(h) for x in range(w) if im5.getpixel((x, y))[0] < 200]
print("Page 5 max y:", max(dark_ys5), "out of", h, f"({max(dark_ys5)/h*100:.1f}%)")
