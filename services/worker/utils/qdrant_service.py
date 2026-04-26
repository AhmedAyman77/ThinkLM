import uuid
from shared import settings
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_HOST,
            api_key=settings.QDRANT_API_KEY
        )
    
    def ensure_collection(self, collection_name: str):
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_MODEL_SIZE,
                    distance=Distance.COSINE
                )
            )
    
    def store_chunks(self, collection_name: str, chunks: list[str], embeddings: list[list[float]], file_id: str, file_name: str):
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[i],
                payload={
                    "text": chunks[i],
                    "file_id": file_id,
                    "file_name": file_name
                }
            )
            for i in range(len(chunks))
        ]

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

qdrant_service = QdrantService()