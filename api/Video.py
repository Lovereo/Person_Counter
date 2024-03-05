import asyncio
from typing import List

import cv2
from fastapi import APIRouter, Query, Depends
from starlette.background import BackgroundTasks
from starlette.responses import StreamingResponse
from model import video, error

from utils.video import RTSPCamera

videoRouter = APIRouter(prefix='/video', tags=['About Video'])

camera = RTSPCamera()


@videoRouter.get("/output/{camera_url}")
async def video_feed(camera_url: str = Query(...)):
    # camera = RTSPCamera()
    if camera_url is None:
        return {"code": 400, "msg": "摄像头IP错误"}
    camera.cap = cv2.VideoCapture("rtsp://admin:tangtangtui123.@" + str(camera_url) + "/live")
    if camera.cap is None:
        return {"code": 400, "msg": "摄像头异常失败"}
    return StreamingResponse(camera.generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")


@videoRouter.get("/number", response_model=video.Number or error.Error)
async def get_number():
    # camera = RTSPCamera()
    # asyncio.create_task(run_back_camera_frame())
    person_count = camera.get_person_count()
    if person_count is None:
        return error.Error(code=400, message="获取人数失败")
    return video.Number(value=str(person_count))


@videoRouter.get("/error", response_model=video.Error or error.Error)
async def get_error():
    err, value = camera.get_error()
    if err:
        return video.Error(value=value)
    else:
        return error.Error(code=400, message="获取错误次数失败")


@videoRouter.get("/isalive", response_model=List[video.IsAlive] or error.Error)
async def is_alive():
    numbers = camera.is_alive()
    if numbers is None:
        return error.Error(code=400, message="获取摄像头存活数失败")
    items = [
        {"name": "运行", "value": numbers},
        {"name": "关闭", "value": camera.camera_number - numbers}
    ]
    return items


@videoRouter.get("/errorNumber", response_model=video.Error)
async def get_error_number():
    asyncio.create_task(camera.reset_error_number())
    return video.Error(value=camera.get_error_number())
