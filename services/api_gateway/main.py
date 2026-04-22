from fastapi import FastAPI
from routers import router as stubs_router
from middleware import AuthMiddleware

app = FastAPI(title="ThinkLM API Gateway")

app.add_middleware(AuthMiddleware)
app.include_router(stubs_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_gateway"}
