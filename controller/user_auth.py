from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from fastapi import HTTPException, status

# 盐值
SECRET_KEY = "ed970259a19edfedf1010199c7002d183bd15bcaec612481b29bac1cb83d8137"

# 加密方式
ALGORITHM = "HS256"

# 过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 1000

# 定义一个验证异常的返回
credentials_exception = HTTPException(

    # 自定义状态码
    status_code=status.HTTP_401_UNAUTHORIZED,

    # 返回信息
    detail="认证失败",

    # 响应头
    # 根据OAuth2规范, 认证失败需要在响应头中添加如下键值对
    headers={'WWW-Authenticate': "Bearer"}
)


def create_jwt_token(data: dict, expire_delta: Optional[timedelta] = None):
    expire = datetime.utcnow() + expire_delta if expire_delta else datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 需要加密的数据data必须为一个字典类型, 在数据中添加过期时间键值对, 键exp的名称是固定写法
    data.update({'exp': expire})

    # 进行jwt加密
    # data:需要加密的字典类型的数据,key:加密需要使用的秘钥, 也叫做盐值,algorithm:加密的算法, 默认为ALGORITHMS.HS256
    token = jwt.encode(claims=data, key=SECRET_KEY, algorithm=ALGORITHM)

    return token


def decrypt_jwt_token(token):
    try:
        # 解密
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        print(f'payload: {payload}')

        # 从解密的字典中获取数据
        user_uid = payload.get('user_uid')
        user_name = payload.get('user_name')
        last_date = payload.get('last_date')

        # 返回解密内容
        return {'user_id': user_uid, 'user_name': user_name, 'last_date': last_date}

    except JWTError as e:
        print(e)
        # 返回异常自定义验证
        raise credentials_exception
