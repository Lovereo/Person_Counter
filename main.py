from fastapi import FastAPI
from uvicorn import run

from api import Video
from starlette.middleware.cors import CORSMiddleware

# from api.Video import video_processor

# app.include_router(User.userRouter)
# app.include_router(Miscellaneous.miscellaneousRouter)

app = FastAPI()

# origins = ["*"]
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://36.134.141.40:2333"
]


# origins = ["http://127.0.0.1:8000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(Video.videoRouter)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
