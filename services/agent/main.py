from fastapi import FastAPI
from routers.chat import router as chat_router

app = FastAPI(title="ThinkLM Agent Service")

app.include_router(chat_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "agent"}