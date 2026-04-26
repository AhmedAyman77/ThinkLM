import httpx
from shared import settings
from fastapi import APIRouter, Request, UploadFile, File

router = APIRouter()

@router.post("/api/files/upload", status_code=202)
async def upload_file(request: Request, file: UploadFile = File(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.FILE_PROCESSOR_URL}/upload",
            # httpx expects a tuple of (filename, file content, content type) to properly handle file uploads
            files={"file": (file.filename, await file.read(), file.content_type)},
            headers={"x-user-id": request.state.user_id},
        )
    return response.json()
