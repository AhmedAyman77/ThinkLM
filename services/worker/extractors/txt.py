class TextExtractor:
    def extract(self, file: bytes) -> str:
        return file.decode('utf-8').strip()
