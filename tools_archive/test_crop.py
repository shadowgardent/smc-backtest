from PIL import Image

im = Image.open("e:/Project/smc-backtest-backend/fig1_page2_crop.png")
# Let's save a clear slice showing Figure 1 and its caption
w, h = im.size
print("Crop size:", w, h)
