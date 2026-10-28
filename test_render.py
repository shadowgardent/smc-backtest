from PIL import Image

im = Image.open(r"C:\Users\ONEST\Downloads\SMC_Architecture_Flow_UltraHD.png")
# Inside Input box: around (1200, 750)
print("Color inside Input box:", im.getpixel((1200, 750)))
# Inside user circle: around (600, 1800)
print("Color inside User circle:", im.getpixel((600, 1800)))
# Background outside boxes: around (500, 600)
print("Color outside boxes:", im.getpixel((500, 600)))
