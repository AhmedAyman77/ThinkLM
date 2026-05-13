from extractors.pdf import PDFExtractor
from extractors.txt import TextExtractor
from extractors.docx import DOCXExtractor
from utils.chunk_service import chunk_service
from utils.embedding_service import embedding_service
from utils.qdrant_service import qdrant_service
from shared import storage_service, files_repository

MIME_EXTRACTOR_MAP = {
    "application/pdf": PDFExtractor(),
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DOCXExtractor(),
    "application/msword": DOCXExtractor(),
    "text/plain": TextExtractor(),
}

class ProcessingController:
    def __init__(self):
        self.chunk_service = chunk_service
        self.qdrant_service = qdrant_service
        self.embedding_service = embedding_service
        self.storage_service = storage_service
        self.files_repository = files_repository
    
    def extract_text(self, file_bytes: bytes, mime_type: str) -> str:
        extractor = MIME_EXTRACTOR_MAP.get(mime_type)
        if not extractor:
            raise ValueError(f"Unsupported mime type: {mime_type}")
        return extractor.extract(file_bytes)

    def process(self, job: dict):
        file_id = job["file_id"]
        user_id = job["user_id"]
        mime_type = job["mime_type"]
        storage_file_path = job["storage_file_path"]
        file_name = job["file_name"]
        collection_name = f"collection_{user_id}"

        file_bytes = self.storage_service.download(storage_file_path)
        
        # save raw text to storage
        raw_text = self.extract_text(file_bytes, mime_type)
        if not raw_text.strip():
            raise ValueError("No text could be extracted from the file")

        storage_content_path = f"{user_id}/{file_id}_extracted.txt"
        self.storage_service.upload(raw_text=raw_text, storage_path=storage_content_path, mime_type="text/plain")
        self.files_repository.update_file_content_path(file_id, storage_content_path)

        chunks = self.chunk_service.chunk(raw_text)
        embeddings = self.embedding_service.embed(chunks)

        self.qdrant_service.ensure_collection(collection_name)
        self.qdrant_service.store_chunks(collection_name, chunks, embeddings, file_id, file_name)

        self.files_repository.update_file_status(file_id, "ready", len(chunks))