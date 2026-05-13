import re
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
    
    async def handle_upload(self, file: UploadFile, user_id: str) -> dict:
        self.validate_mime_type(file.content_type)

        bytes_content = await file.read() # Read file content as bytes

        # validation check
        if len(bytes_content) > FileEnum.MAX_FILE_SIZE.value:
            raise HTTPException(status_code=400, detail="File size exceeds limit")
        
        if len(bytes_content) == 0:
            raise HTTPException(status_code=400, detail="File is empty")

        # save file to storage
        file_id = str(uuid.uuid4())
        safe_filename = re.sub(r'[^\w\.\-]', '_', file.filename)
        storage_file_path = f"{user_id}/{file_id}_{safe_filename}"
        
        self.storage.upload(content=bytes_content, storage_path=storage_file_path, mime_type=file.content_type)

        # Record metadata in database
        self.files_repository.insert_file(file_id=file_id, user_id=user_id, file_name=file.filename, mime_type=file.content_type, storage_file_path=storage_file_path)

        # Push job to processing queue\
        try:
            self.queue.push_job(file_id, user_id, file.filename, file.content_type, storage_file_path)
            return {"file_id": file_id, "status": "processing"}
        
        except Exception as e:
            self.files_repository.update_file_status(file_id, "failed")
            raise HTTPException(status_code=500, detail="Failed to queue file for processing")


