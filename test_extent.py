import docx

doc = docx.Document(r"C:\Users\ONEST\Downloads\SMC_AUCC2026_Final.docx")
p29 = doc.paragraphs[29]
extent_elements = p29._p.xpath('.//wp:extent')
for ext in extent_elements:
    cx = int(ext.attrib.get('cx', 0))
    cy = int(ext.attrib.get('cy', 0))
    print(f"Drawing size in EMUs: cx={cx}, cy={cy}")
    print(f"Drawing size in cm: width={cx/360000:.2f} cm, height={cy/360000:.2f} cm")
