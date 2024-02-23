import cv2
import torch
from ultralytics import YOLO
from PIL import Image
from fastapi import FastAPI, WebSocket
from io import BytesIO
import numpy as np


class Video_processing:
    def __init__(self, model_path, camera_url):
        print(model_path)
        self.model = YOLO(model_path)
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        self.model.to(self.device)
        self.camera_url = camera_url

    async def generate_frames(self):
        cap = cv2.VideoCapture(self.camera_url)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(frame)
            results = self.model(pil_frame)
            boxes = results[0].boxes
            person_count = 0

            for boxs in boxes:
                if results[0].names[boxs.cls[0].item()] == 'person':
                    person_count += 1
                    box = boxs.xyxy[0]
                    x1, y1, x2, y2 = box.tolist()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, results[0].names[boxs.cls[0].item()], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)
                    cv2.putText(frame, "conf:" + str(round(boxs.conf[0].item(), 2)), (x1, y1 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)

            fontsize = 1.5
            if person_count > 4:
                cv2.putText(frame, "Max", (500, 500), cv2.FONT_HERSHEY_SIMPLEX, fontsize,
                            (255, 0, 0), 3)

            cv2.putText(frame, f"Persons detected: {person_count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        fontsize, (255, 0, 0), 3)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = buffer.tobytes()

            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpg_as_text + b'\r\n')

        cap.release()