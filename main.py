from fastapi import FastAPI

from api import Video, User
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(Video.videoRouter)
# app.include_router(User.userRouter)
# app.include_router(Miscellaneous.miscellaneousRouter)