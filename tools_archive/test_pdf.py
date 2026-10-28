import fitz # PyMuPDF
doc = fitz.open(r"C:\Users\ONEST\Downloads\Untitled 1.pdf")
print("Page count:", len(doc))
page = doc[0]
print("Rect:", page.rect)
