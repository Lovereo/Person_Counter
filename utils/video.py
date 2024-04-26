import queue
import threading
import cv2
import time
from PIL import Image
from ultralytics import YOLO

from utils.public_way import send_on_tcp_request, send_off_tcp_request


CAMERAS = {
    "camera1": "rtsp://admin:a1234567@192.168.31.71:554/Streaming/Channels/1",
    "camera2": "rtsp://admin:a1234567@192.168.31.68:554/Streaming/Channels/1"
}

raw_frames_queue = {
    "camera1": queue.Queue(),
    "camera2": queue.Queue()
}

# 初始化 YOLO 模型
model = YOLO('../weights/yolov8s.pt', verbose=False)

latest_person_counts = {
    "camera1": 0,
    "camera2": 0
}

camera_active = {
    "camera1": False,
    "camera2": False
}


exceed_count = 0
exceed_count_lock = threading.Lock()

def process_frame(camera_id):
    global exceed_count
    while True:
        frame = raw_frames_queue[camera_id].get()
        if frame is None:
            break  # 如果接收到 None，结束线程

        # 将帧转换为 YOLO 可处理的格式
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        results = model(img)
        boxes = results[0].boxes
        person_count = 0
        for box in boxes:
            if results[0].names[box.cls[0].item()] == 'person' and float(box.conf[0].item()) >= 0.65:
                person_count += 1
        if person_count > 9:
            with exceed_count_lock:
                exceed_count += 1
            send_on_tcp_request()
        send_off_tcp_request()
        latest_person_counts[camera_id] = person_count
        raw_frames_queue[camera_id].task_done()
        time.sleep(2)  # 每2秒进行一次检测

def generate_frames(camera_id):
    cap = cv2.VideoCapture(CAMERAS[camera_id])
    if not cap.isOpened():
        print(f"Failed to open camera {camera_id}")
        return

    camera_active[camera_id] = True  # 开始读取时设置为 True
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        camera_active[camera_id] = True  # 读取成功时持续设置为 True
        # 将原始帧放入队列
        raw_frames_queue[camera_id].put(frame)


        # 转换为 JPEG
        processed_frame = cv2.resize(frame, (670, 370))
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
    camera_active[camera_id] = False  # 结束时设置为 False

for camera_id in CAMERAS.keys():
    thread = threading.Thread(target=process_frame, args=(camera_id,))
    thread.start()