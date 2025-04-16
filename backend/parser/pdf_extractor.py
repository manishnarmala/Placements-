import pdfplumber
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber error: {e}")

    if text.strip():
        return text

    # Fallback to OCR if no text found
    try:
        images = convert_from_path(pdf_path, poppler_path=r"C:\poppler\Library\bin")
        for img in images:
            text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"OCR error: {e}")

    return text.strip()
