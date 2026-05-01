from qdrant_client import QdrantClient
from shared import settings, QdrantEnum

class QdrantSearchService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_HOST,
            api_key=settings.QDRANT_API_KEY
        )

    def search(self, collection_name: str, query_vector: list[float]) -> list[dict]:
        results = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=QdrantEnum.TOP_K.value,
        )

        filtered = [
            point for point in results.points
            if point.score >= QdrantEnum.SIMILARITY_THRESHOLD.value
        ]

        return [point.payload for point in filtered]

qdrant_search_service = QdrantSearchService()