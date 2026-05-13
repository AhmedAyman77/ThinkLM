from google import genai
from shared import settings

class EmbeddingService:
    
    model_id = settings.EMBEDDING_MODEL_ID
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def embed(self, chunks: list[str]) -> list[list[float]]:
        embeddings = []
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            response = self.client.models.embed_content(
                model=self.model_id,
                content=batch
            )
            embeddings.extend([e.values for e in response.embeddings])
        return embeddings

embedding_service = EmbeddingService()