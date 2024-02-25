import cv2
import torch
from ultralytics import YOLO
from PIL import Image
from threading import Lock
import asyncio


class Video_processing:
    def __init__(self, model_path, camera_url, max_queue_size=100):
        self.person_count_lock = Lock()
        self.model = YOLO(model_path)
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        self.model.to(self.device)
        self.camera_url = camera_url
        self.person_count = 0
        self.max_queue_size = max_queue_size
        self.frame_queue = asyncio.Queue(maxsize=max_queue_size)
        self.prev_boxes = []  # 存储上一次检测到的边界框信息
        self.frame_count = 0  # 添加一个帧计数器
        self.camera_number = 1
        self.cap = cv2.VideoCapture(self.camera_url)

    def is_alive(self) -> int:
        # cap = cv2.VideoCapture(self.camera_url)
        alive_num = 0
        for i in range(self.camera_number):
            if self.cap.isOpened():
                alive_num += 1
        return alive_num


    async def generate_frames(self):
        self.cap = cv2.VideoCapture(self.camera_url)
        loop = asyncio.get_event_loop()

        async def frame_generator():
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                self.frame_count += 1

                if self.frame_count % 25 == 0:
                    pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # 在此处进行颜色空间转换
                    results = await loop.run_in_executor(None, self.model, pil_frame)
                    boxes = results[0].boxes

                    with self.person_count_lock:
                        self.person_count = 0

                    for boxs in boxes:
                        if results[0].names[boxs.cls[0].item()] == 'person':
                            with self.person_count_lock:
                                self.person_count += 1
                            x1, y1, x2, y2 = boxs.xyxy[0].tolist()
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, results[0].names[boxs.cls[0].item()], (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (0, 255, 0), 2)
                            cv2.putText(frame, "conf:" + str(round(boxs.conf[0].item(), 2)), (x1, y1 + 20),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (0, 255, 0), 2)

                fontsize = 1.5
                if self.person_count > 4:
                    cv2.putText(frame, "Max", (500, 500), cv2.FONT_HERSHEY_SIMPLEX, fontsize,
                                (0, 255, 0), 3)

                cv2.putText(frame, f"Persons detected: {self.person_count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            fontsize, (0, 255, 0), 3)

                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (670, 370))

                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = buffer.tobytes()

                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpg_as_text + b'\r\n')

        async for frame in frame_generator():
            yield frame

        self.cap.release()

    async def get_frame(self):
        return await self.frame_queue.get()

    def get_person_count(self):
        with self.person_count_lock:
            return self.person_count

    def get_error(self):
        if self.get_person_count() >= 1:
            return "警告:当前区域人数已经超限"
        else:
            return ""



