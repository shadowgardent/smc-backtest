from PIL import Image

im = Image.open("extracted_p29_rgb.png")
print("Image size:", im.size)
print("Top-left pixel (5, 5):", im.getpixel((5, 5)))
print("Inside Input box (300, 100):", im.getpixel((300, 100)))
