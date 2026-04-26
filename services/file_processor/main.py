from fastapi import FastAPI
from routers.upload import router as upload_router

app = FastAPI(title="ThinkLM File Processor")

app.include_router(upload_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "file_processor"}