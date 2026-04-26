from google import genai
from shared import settings

class EmbeddingService:
    
    model_id = settings.EMBEDDING_MODEL_ID
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def embed(self, chunks: list[str]) -> list[list[float]]:
        response = self.client.models.embed_content(
            model=self.model_id,
            content=chunks
        )
        return [e.values for e in response.embeddings]

embedding_service = EmbeddingService()