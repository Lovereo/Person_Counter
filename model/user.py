import datetime

from pydantic import BaseModel


class UserInfo(BaseModel):
    uid: int
    sys: int
    create_date: datetime.datetime | None
    last_date: datetime.datetime


class User(BaseModel):
    id: int | None
    username: str
    password: str
    user_info: UserInfo | None


class SuccessInfo(BaseModel):
    msg: str
    token: str


class UserLoginSuccess(BaseModel):
    code: int
    data: SuccessInfo | None = None




