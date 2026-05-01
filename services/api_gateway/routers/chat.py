from fastapi import APIRouter, Request
import httpx
from shared import settings

router = APIRouter()


@router.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.AGENT_SERVICE_URL}/chat",
            json=body,
            headers={"x-user-id": request.state.user_id},
        )
    return response.json()