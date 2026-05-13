from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/api/voice/transcribe")
async def transcribe_stub(request: Request):
    return JSONResponse(status_code=503, content={"detail": "Voice service not connected yet"})


@router.post("/api/voice/synthesize")
async def synthesize_stub(request: Request):
    return JSONResponse(status_code=503, content={"detail": "Voice service not connected yet"})


@router.get("/api/files")
async def list_files_stub(request: Request):
    return JSONResponse(status_code=503, content={"detail": "File processor service not connected yet"})