from typing import List

import cv2
from fastapi import APIRouter
from starlette.responses import StreamingResponse, JSONResponse
from model import video

from ulits.Video_processing import Video_processing

videoRouter = APIRouter(prefix='/video', tags=['About Video'])

video_processor = Video_processing("../weights/yolov8n.pt", "rtsp://admin:tangtangtui123.@192.168.3.66/live")

@videoRouter.get("/output")
async def video_feed():
    return StreamingResponse(video_processor.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@videoRouter.get("/number", response_model=video.Number)
async def get_number():
    return video.Number(value=str(video_processor.get_person_count()))


@videoRouter.get("/error", response_model=video.Error)
async def get_error():
    return video.Error(value=video_processor.get_error())


@videoRouter.get("/isalive", response_model=List[video.IsAlive])
async def is_alive():
    items = [
        {"name": "运行", "value": video_processor.is_alive()},
        {"name": "关闭", "value": video_processor.camera_number - video_processor.is_alive()}
    ]
    return items
