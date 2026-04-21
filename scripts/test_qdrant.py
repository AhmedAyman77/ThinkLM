import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

load_dotenv()

def test_qdrant_connection():
    try:
        qdrant_key = os.getenv("QDRANT_API_KEY")
        qdrant_host = os.getenv("QDRANT_HOST")

        qdrant_client = QdrantClient(
            url=qdrant_host,
            api_key=qdrant_key
        )

        qdrant_client.recreate_collection(
            collection_name="test_collection",
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
        )

        qdrant_client.upsert(
            collection_name="test_collection",
            points=[
                PointStruct(id=1, vector=[0.1] * 3072, payload={"text": "Hello, Qdrant!"})
            ]
        )

        res = qdrant_client.query_points(
            collection_name="test_collection",
            query=[0.1] * 3072,
            limit=1
        )

        assert res.points[0].payload["text"] == "Hello, Qdrant!"
        print("Qdrant connection test passed!")

        qdrant_client.delete_collection(collection_name="test_collection")
        print("Qdrant collection deleted successfully.")

    except Exception as e:
        print(f"Qdrant connection test failed: {e}")

if __name__ == "__main__":
    test_qdrant_connection()
