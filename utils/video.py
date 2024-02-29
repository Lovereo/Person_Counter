import queue
import threading

import cv2
import time
import asyncio
import torch
from PIL import Image
from ultralytics import YOLO

from utils.public_way import send_tcp_request


class RTSPCamera:
    def __init__(self):
        self.cap: cv2.VideoCapture = None
        self.last_frame_time = time.time()
        self.frame_counter = 0
        self.person_count = 0
        self.model = YOLO('../weights/yolov8s.pt')
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        self.model.to(self.device)
        self.camera_number = 1
        self.state = 0
        self.number = 0
        self.frame_queue = queue.Queue()
        self.error_number = 0
        self.process_thread = threading.Thread(target=self.process_frames_async)
        self.process_thread.daemon = True  # 设置为守护线程，以确保程序退出时线程也会退出
        self.process_thread.start()

    def process_frames_async(self):
        while True:
            frame = self.frame_queue.get()
            # 处理帧图像
            self.person_count = self.dispose_frame_async(frame)

    async def generate_frames(self):
        while True:
            rval, frame = self.cap.read()
            if not rval:
                break

            frame = cv2.resize(frame, (670, 370))
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = buffer.tobytes()

            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpg_as_text + b'\r\n')

            elapsed_time = time.time() - self.last_frame_time
            if elapsed_time >= 2:
                self.frame_queue.put(frame)
                self.last_frame_time = time.time()

    def dispose_frame_async(self, frame):
        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = self.model(pil_frame)  # 不需要异步调用
        boxes = results[0].boxes
        person_count = 0
        for boxs in boxes:
            if results[0].names[boxs.cls[0].item()] == 'person':
                if float(round(boxs.conf[0].item(), 2)) >= 0.65:
                    person_count += 1
        return person_count

    def get_person_count(self) -> int:
        person_num = self.person_count
        if person_num == 0:
            return 0
        return person_num

    def is_alive(self):
        alive_num = 0
        for i in range(self.camera_number):
            if self.cap and self.cap.isOpened():
                alive_num += 1
        return alive_num

    def release(self):
        self.cap.release()

    def get_error(self):
        person_number = self.get_person_count()
        if person_number >= 9 and person_number != self.number:
            if self.state == 0:
                send_tcp_request("483A0170010100004544")
                self.state = 1
            self.number = person_number
            self.error_number += 1
            return "警告:当前区域人数已经超限"
        else:
            # if self.state == 1:
            # print("1")
            send_tcp_request("483A0170010000004544")
            self.state = 0
            self.number = 0
            return ""

    def get_error_number(self):
        return self.error_number

    def clear_error_number(self):
        self.error_number = 0
        print("Error number cleared.")

    async def reset_error_number(self):
        while True:
            # 获取当前时间
            current_time = time.time()
            # 计算距离第二天零点的时间差
            time_diff = 86400 - (current_time % 86400)
            # 等待直到下一天
            await asyncio.sleep(time_diff)
            # 清零错误数
            self.clear_error_number()
            print("Error number cleared.")
