from fastapi import FastAPI
from routers import stubs_router, files_router
from middleware import AuthMiddleware

app = FastAPI(title="ThinkLM API Gateway")

app.add_middleware(AuthMiddleware)
app.include_router(stubs_router)
app.include_router(files_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_gateway"}
