from PIL import Image

im = Image.open(r"C:\Users\ONEST\Downloads\SMC_Architecture_Flow_White.png")
w, h = im.size
print("Size:", w, "x", h)
print("Corner (5, 5):", im.getpixel((5, 5)))
print("Corner (w-5, 5):", im.getpixel((w-5, 5)))
print("Corner (5, h-5):", im.getpixel((5, h-5)))
print("Corner (w-5, h-5):", im.getpixel((w-5, h-5)))
# Check line color near center of a line
print("Min pixel value (black text):", min(im.getdata()))
