import cv2
from fastapi import APIRouter, WebSocket
from starlette.responses import StreamingResponse

from ulits.Video_processing import Video_processing

videoRouter = APIRouter(prefix='/video', tags=['About Video'])

video_processor = Video_processing("../weights/yolov8s.pt", "rtsp://admin:tangtangtui123.@192.168.3.66/live")

#
# @videoRouter.get('/output', summary="Video")
# async def get_video(websocket: WebSocket):
#     await video_processor.detect_objects_and_send_stream(websocket)
# async def generate_frames():
#     cap = cv2.VideoCapture(0)  # Open webcam (you can replace 0 with your camera index)
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # Process the frame (e.g., resize, encode to JPEG)
#         _, jpg = cv2.imencode(".jpg", frame)
#         frame_bytes = jpg.tobytes()
#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@videoRouter.get("/output")
async def video_feed():
    return StreamingResponse(video_processor.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")