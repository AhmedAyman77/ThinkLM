from ..supabase_client import supabase_client

class FilesRepository:
    def __init__(self):
        self.client = supabase_client

    def insert_file(self, file_id: str, user_id: str, file_name: str, mime_type: str, storage_file_path: str=None, storage_content_path: str=None):
        self.client.table("files").insert({
            "id": file_id,
            "user_id": user_id,
            "file_name": file_name,
            "mime_type": mime_type,
            "status": "processing",
            "chunks_count": 0,
            "collection_name": f"collection_{user_id}",
            "file_path": storage_file_path,
            "content_path": storage_content_path
        }).execute()
    
    def update_file_status(self, file_id: str, status: str, chunks_count: int = 0):
        self.client.table("files").update({
            "status": status,
            "chunks_count": chunks_count
        }).eq("id", file_id).execute()
    
    def update_file_content_path(self, file_id: str, content_path: str):
        self.client.table("files").update({
            "content_path": content_path
        }).eq("id", file_id).execute()

files_repository = FilesRepository()