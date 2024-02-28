from fastapi import FastAPI
from uvicorn import run

from api import Video
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://36.134.141.40:2333"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(Video.videoRouter)

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
