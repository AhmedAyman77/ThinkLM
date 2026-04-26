import tiktoken
from shared import QdrantEnum

class ChunkService:
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def chunk(self, text: str) -> list[str]:
        tokens = self.tokenizer.encode(text)
        chunks = []
        start = 0

        while start < len(tokens):
            end = min(start + QdrantEnum.CHUNK_SIZE.value, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            start += QdrantEnum.CHUNK_SIZE.value - QdrantEnum.CHUNK_OVERLAP.value

        return chunks

chunk_service = ChunkService()