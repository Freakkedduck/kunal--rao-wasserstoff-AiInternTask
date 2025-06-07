import PyMuPDF  # fitz  # type:ignore
import pytesseract # type:ignore
from PIL import Image # type:ignore
import os

def process_document(file_path, filename):
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(file_path)
    else:
        return [{"page": 1, "text": "Unsupported file type."}]

def extract_text_from_pdf(pdf_path):
    doc = PyMuPDF.open(pdf_path) # fitz 
    content = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if not text:  # If blank, try OCR
            pix = page.get_pixmap(dpi=300)
            img_path = f"temp_page_{i}.png"
            pix.save(img_path)
            text = pytesseract.image_to_string(Image.open(img_path))
            os.remove(img_path)
        content.append({"page": i + 1, "text": text})
    return content

def extract_text_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return [{"page": 1, "text": text}]
