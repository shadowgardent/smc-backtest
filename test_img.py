from PIL import Image
im = Image.open("e:/Project/smc-backtest-backend/user_crop_preview.png")

# Check rows between Node 4 (bottom 282) and Node 5 (top 322)
for y in range(283, 322, 5):
    non_white = [(x, im.getpixel((x, y))[:3]) for x in range(im.size[0]) if im.getpixel((x, y))[:3] != (255, 255, 255)]
    xs = [p[0] for p in non_white]
    print(f"y={y}: xs={xs}")

# Check rows between Node 6 (bottom 415) and Node 7 (top 468)
for y in range(416, 468, 5):
    non_white = [(x, im.getpixel((x, y))[:3]) for x in range(im.size[0]) if im.getpixel((x, y))[:3] != (255, 255, 255)]
    xs = [p[0] for p in non_white]
    print(f"y={y}: xs={xs}")
