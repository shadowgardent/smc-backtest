from PIL import Image
im = Image.open("extracted_p29_image.png")
print("Mode:", im.mode)
# save as RGB to inspect
im.convert("RGB").save("extracted_p29_rgb.png")
print("Saved extracted_p29_rgb.png")
