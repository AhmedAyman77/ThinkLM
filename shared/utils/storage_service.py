from ..supabase_client import supabase_client
from ..constant import SupabaseEnum

class StorageService:
    def __init__(self):
        self.client = supabase_client
    
    def upload(self, storage_path: str, mime_type: str,  content: bytes = None, raw_text: str = None) -> None:
        if not content and not raw_text:
            raise ValueError("Either content or raw_text must be provided.")

        file = content if content else raw_text.encode("utf-8")
    
        self.client.storage.from_(SupabaseEnum.STORAGE_BUCKET.value).upload(
            path=storage_path,
            file=file,
            file_options={"content-type": mime_type}
        )

    def download(self, storage_path: str) -> bytes:
        return self.client.storage.from_(SupabaseEnum.STORAGE_BUCKET.value).download(storage_path)

storage_service = StorageService()