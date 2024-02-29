import asyncio
from typing import List

import cv2
from fastapi import APIRouter, Query, Depends
from starlette.background import BackgroundTasks
from starlette.responses import StreamingResponse
from model import video

from utils.video import RTSPCamera

videoRouter = APIRouter(prefix='/video', tags=['About Video'])

camera = RTSPCamera()


@videoRouter.get("/output/{camera_url}")
async def video_feed(camera_url: str = Query(...)):
    # camera = RTSPCamera()
    camera.cap = cv2.VideoCapture("rtsp://admin:tangtangtui123.@" + str(camera_url) + "/live")
    return StreamingResponse(camera.generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")


@videoRouter.get("/number", response_model=video.Number)
async def get_number():
    # camera = RTSPCamera()
    # asyncio.create_task(run_back_camera_frame())
    person_count = camera.get_person_count()
    return video.Number(value=str(person_count))


@videoRouter.get("/error", response_model=video.Error)
async def get_error():
    return video.Error(value=camera.get_error())


@videoRouter.get("/isalive", response_model=List[video.IsAlive])
async def is_alive():
    items = [
        {"name": "运行", "value": camera.is_alive()},
        {"name": "关闭", "value": camera.camera_number - camera.is_alive()}
    ]
    return items


@videoRouter.get("/errorNumber", response_model=video.Error)
async def get_error_number():
    asyncio.create_task(camera.reset_error_number())
    return video.Error(value=camera.get_error_number())
