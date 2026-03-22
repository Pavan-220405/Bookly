from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request, status

from myapp.auth.utils import decode_access_token, decode_refresh_token
from myapp.db.redis_engine import token_in_blocklist


# -----------------------------
# Access Token Bearer
# -----------------------------
class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request : Request) -> dict:
        creds = await super().__call__(request)

        token = creds.credentials
        payload = decode_access_token(token)

        return payload


# -----------------------------
# Refresh Token Bearer
# -----------------------------
class RefreshTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request : Request) -> dict:
        creds = await super().__call__(request)

        token = creds.credentials
        payload = decode_refresh_token(token)

        if await token_in_blocklist(jti=payload["jti"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Refresh token revoked. Please login again")
        
        return payload

