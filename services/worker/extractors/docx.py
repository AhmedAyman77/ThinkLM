from docx import Document
import io

class DOCXExtractor:
    def extract(self, file: bytes) -> str:
        text = ""
        document = Document(io.BytesIO(file))
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
        
        return text.strip()
