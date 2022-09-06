import time
import jwt
from typing import Dict
from decouple import config
import json

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_response(token: str):
    return {
        "access_token": token
    }


def sign_JWT(user_email: str) -> Dict[str, str]:
    pyload = {
        "user_email": user_email,
        "expires":  time.time() + 900   # 15 min
    }
    token = jwt.encode(pyload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}


def refresh_JWT(user_email: str) -> str:
    pyload = {
        "user_email": user_email,
        "type": 'refresh',
        "expires": time.time() + 60 * 24 * 7 * 60   # 7 month
    }

    refresh_token = jwt.encode(pyload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return refresh_token


def verify_refresh_token(token):
    payload = decodeJWT(token)
    if payload and payload.get('type') == 'refresh':
        return True, payload
    else:
        return False, None