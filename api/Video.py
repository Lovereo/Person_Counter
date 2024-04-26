from typing import List

from fastapi import APIRouter
from starlette.responses import StreamingResponse
from model import video, error
from utils.video import generate_frames, latest_person_counts, exceed_count, camera_active

videoRouter = APIRouter(prefix='/video', tags=['About Video'])


connections = {}


@videoRouter.get("/output/{camera_id}")
def video_feed(camera_id: str):
    """ 返回视频流的 Response """
    return StreamingResponse(generate_frames(camera_id),
                             media_type="multipart/x-mixed-replace;boundary=frame")


@videoRouter.get("/person_count/{camera_id}", response_model=video.Number or error.Error)
async def get_person_count(camera_id: str):
    if camera_id in latest_person_counts:
        return video.Number(value=latest_person_counts[camera_id])
    else:
        return error.Error(code=400, message="获取人数失败")


@videoRouter.get("/errorNumber", response_model=video.Error)
def get_error_number():
    # video.Error(value=exceed_count)
    return video.Error(value=exceed_count)


@videoRouter.get("/camera_status", response_model=List[video.IsAlive] or error.Error)
def get_camera_status():
    active_count = sum(status for status in camera_active.values() if status)
    inactive_count = len(camera_active) - active_count
    items = [
        {"name": "运行", "value": active_count},
        {"name": "关闭", "value": inactive_count}
    ]
    return items
