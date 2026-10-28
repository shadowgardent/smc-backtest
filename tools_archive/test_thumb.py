from PIL import Image
im = Image.open("C:/Users/ONEST/Downloads/SMC_System_Flow_Clean.png")
print("Size:", im.size)
# generate thumbnail
thumb = im.resize((800, 450), Image.LANCZOS)
thumb.save("e:/Project/smc-backtest-backend/thumb_clean.png")
print("Thumbnail saved successfully!")
