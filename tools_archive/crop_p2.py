from PIL import Image

im = Image.open("e:/Project/smc-backtest-backend/check_page_2.png")
w, h = im.size
print("Page 2 size:", w, "x", h)

# In page 2, Figure 1 is in the middle-bottom
# Let's crop y from 40% to 80% of page height
crop_fig1 = im.crop((int(w * 0.1), int(h * 0.35), int(w * 0.9), int(h * 0.75)))
crop_fig1.save("e:/Project/smc-backtest-backend/fig1_page2_crop.png")
print("Saved fig1_page2_crop.png:", crop_fig1.size)
