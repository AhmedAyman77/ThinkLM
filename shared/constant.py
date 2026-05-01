from enum import Enum

class QdrantEnum(Enum):
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    TOP_K = 5
    SIMILARITY_THRESHOLD = 0.75
class RedisEnum(Enum):
    QUEUE_NAME = 'file_processing_queue'

class SupabaseEnum(Enum):
    STORAGE_BUCKET = 'documents'

class MiddlewareEnum(Enum):
    EXEMPT_PATHS = ["/health"]

class FileEnum(Enum):
    ALLOWED_MIME_TYPES = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "text/plain"
    ]
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB