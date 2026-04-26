import uuid
from fastapi import UploadFile, HTTPException
from shared import files_repository, storage_service, queue_service, FileEnum

class UploadController:
    def __init__(self):
        self.storage = storage_service
        self.files_repository = files_repository
        self.queue = queue_service
    
    def validate_mime_type(self, mime_type: str):
        if mime_type not in FileEnum.ALLOWED_MIME_TYPES.value:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    
    def validate_file_size(self, file: UploadFile):
        file.file.seek(0, 2)  # Move to end of file
        size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        if size > FileEnum.MAX_FILE_SIZE.value:
            raise HTTPException(status_code=400, detail="File size exceeds limit")
    
    async def handle_upload(self, file: UploadFile, user_id: str) -> dict:
        self.validate_mime_type(file.content_type)
        self.validate_file_size(file)

        file_id = str(uuid.uuid4())
        storage_path = f"{user_id}/{file_id}_{file.filename}"
        
        # Save file to storage
        content = await file.read()
        self.storage.upload(content=content, storage_path=storage_path, mime_type=file.content_type)

        # Record metadata in database
        self.files_repository.insert_file(file_id=file_id, user_id=user_id, file_name=file.filename, mime_type=file.content_type, storage_path=storage_path)

        # Push job to processing queue
        self.queue.push_job(file_id, user_id, file.filename, file.content_type, storage_path)

        return {"file_id": file_id, "status": "processing"}
