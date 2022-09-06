from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth.jwt_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Не валидная схема авторизации")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Не валидный токен")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Не валидный токен")

    def verify_jwt(self, jwt_token: str):
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwt_token)
        except:
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid