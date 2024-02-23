from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from log import logs
from model import user, error
from controller.user import Select_user
from controller.user_auth import create_jwt_token, decrypt_jwt_token

userRouter = APIRouter(prefix='/user', tags=['About User'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
logger = logs.Logger()


@userRouter.post('/login', response_model=user.UserLoginSuccess or error.Error, summary="Login")
async def login(users: user.User = Depends(Select_user)):
    if users:
        token = create_jwt_token({'user_uid': users.user_info.uid, 'user_name': users.username,
                                  'last_date': users.user_info.last_date.strftime("%Y-%m-%d-%H:%M:%S")})
        return user.UserLoginSuccess(code=200, data={"msg": "登录成功", "token": token})

    return error.Error(code=400, message="Login Failed")


@userRouter.get('/me')
async def me(token: str = Depends(oauth2_scheme)):
    # 解密
    jwt_token = decrypt_jwt_token(token)
    return jwt_token
