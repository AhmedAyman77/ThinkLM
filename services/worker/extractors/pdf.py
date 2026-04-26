import pdfplumber
import io

class PDFExtractor:
    def extract(self, file: bytes) -> str:
        text = ""
        with pdfplumber.open(io.BytesIO(file)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text.strip()
