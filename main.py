from fastapi import FastAPI
from uvicorn import run

from api import Video
from starlette.middleware.cors import CORSMiddleware

from api.Video import video_processor

# app.include_router(User.userRouter)
# app.include_router(Miscellaneous.miscellaneousRouter)

if __name__ == "__main__":

    app = FastAPI()

    origins = ["127.0.0.1", "localhost"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"])

    app.include_router(Video.videoRouter)

    run(app, host="0.0.0.0", port=8000)