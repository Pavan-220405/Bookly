from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request

from myapp.auth.utils import decode_access_token, decode_refresh_token


# -----------------------------
# Access Token Bearer
# -----------------------------
class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request : Request) -> HTTPAuthorizationCredentials | None:
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
    
    async def __call__(self, request : Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials
        payload = decode_refresh_token(token)

        return payload

