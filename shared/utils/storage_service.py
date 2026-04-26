from ..supabase_client import supabase_client
from ..constant import SupabaseEnum

class StorageService:
    def __init__(self):
        self.client = supabase_client
    
    def upload(self, content: bytes, storage_path: str, mime_type: str) -> None:
        self.client.storage.from_(SupabaseEnum.STORAGE_BUCKET.value).upload(
            path=storage_path,
            file=content,
            file_options={"content-type": mime_type}
        )

    def download(self, storage_path: str) -> bytes:
        return self.client.storage.from_(SupabaseEnum.STORAGE_BUCKET.value).download(storage_path)

storage_service = StorageService()