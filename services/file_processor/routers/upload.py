from fastapi import APIRouter, UploadFile, File, Header
from controllers.upload_controller import UploadController

router = APIRouter()
controller = UploadController()


@router.post("/upload", status_code=202)
async def upload_file(
    file: UploadFile = File(...),
    x_user_id: str = Header(...)
):
    return await controller.handle_upload(file, x_user_id)
