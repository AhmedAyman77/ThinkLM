import jwt
import httpx
from shared.config import settings
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from shared.constant import MiddlewareEnum

JWKS_URL = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
jwks_client = jwt.PyJWKClient(JWKS_URL)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in MiddlewareEnum.EXEMPT_PATHS.value:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: Missing or invalid Authorization header"}
            )

        token = auth_header.split(" ")[1]

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["ES256", "HS256"],
                options={"verify_aud": False}
            )
            request.state.user_id = payload.get("sub")

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: Token has expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: Invalid token"}
            )

        return await call_next(request)