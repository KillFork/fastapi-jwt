from fastapi import APIRouter, Body, Depends
from app.models.user_model import UserSchema, UserLoginSchema
from app.services.auth.jwt_handler import sign_JWT, decodeJWT, refresh_JWT, verify_refresh_token
from app.services.auth.jwt_bearer import JWTBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/user", tags=["user"])
users = []

@router.post("/signup", tags=["user"])
def sign_up(user: UserSchema = Body(default=None)):
    user.password = pwd_context.hash(user.password)
    users.append(user)
    return user


@router.post("/login", tags=["user"])
def login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        access_token = sign_JWT(user.email)
        refresh_token = refresh_JWT(user.email)
        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        return {
            "error": "Неправильный логин или пароль"
        }


@router.get("/get-current-users", dependencies=[Depends(JWTBearer())], tags=["user"])
def get_current_users(token: str = Depends(JWTBearer())):
    decode = decodeJWT(token)
    for user in users:
        if user.email == decode['user_email']:
            return user

@router.get('/new_token')
def create_new_token(token: str = Depends(JWTBearer())):
    if verify_refresh_token(token):
        access_token = sign_JWT(decodeJWT(token)['user_email'])
        return access_token
    else:
        return {
            "error": "Неправильный refresh токен"
        }


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and pwd_context.verify(data.password, user.password):
            return True
        else:
            return False
