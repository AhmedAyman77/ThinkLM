from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/api/voice/transcribe")
async def transcribe_stub(request: Request):
    return {"detail": "Voice service not connected yet"}, 503


@router.post("/api/voice/synthesize")
async def synthesize_stub(request: Request):
    return {"detail": "Voice service not connected yet"}, 503


@router.get("/api/files")
async def list_files_stub(request: Request):
    return {"detail": "File processor service not connected yet"}, 503