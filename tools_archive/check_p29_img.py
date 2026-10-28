import docx

doc = docx.Document(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx")
p29 = doc.paragraphs[29]
print("P29 text:", p29.text)
print("P29 runs:", len(p29.runs))

for r in p29.runs:
    # check images
    drawing_elements = r._r.xpath('.//a:blip')
    print("Found blips:", len(drawing_elements))
    for el in drawing_elements:
        embed_id = el.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        target_part = doc.part.related_parts.get(embed_id)
        if target_part:
            print("Image part name:", target_part.partname)
            print("Image content type:", target_part.content_type)
            print("Image size bytes:", len(target_part.blob))
            with open("extracted_p29_image.png", "wb") as f:
                f.write(target_part.blob)
            print("Saved extracted_p29_image.png")

# Also check extent size in drawing
extent_elements = p29._r.xpath('.//wp:extent')
for ext in extent_elements:
    cx = int(ext.attrib.get('cx', 0))
    cy = int(ext.attrib.get('cy', 0))
    # 1 inch = 914400 EMUs, 1 cm = 360000 EMUs
    print(f"Drawing size in EMUs: cx={cx}, cy={cy}")
    print(f"Drawing size in cm: width={cx/360000:.2f} cm, height={cy/360000:.2f} cm")
