import cv2
from ultralytics import YOLO
import torch
import torchvision
from torchvision.transforms import ToTensor
from PIL import Image

model = YOLO("../../../Python_Project/Person_Counter_exe/weights/yolov8s.pt")

ip_camera_url = "rtsp://admin:tangtangtui123.@192.168.3.66/live"

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model.to(device)

cap = cv2.VideoCapture(ip_camera_url)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pil_frame = Image.fromarray(frame)

    results = model(pil_frame)

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
            cv2.putText(frame, "conf:" + str(round(boxs.conf[0].item(), 2)), (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

    fontsize = 1.5
    if person_count > 4:
        cv2.putText(frame, "Max", (500, 500), cv2.FONT_HERSHEY_SIMPLEX, fontsize,
                    (255, 0, 0), 3)

    cv2.putText(frame, f"Perple detected: {person_count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                fontsize, (255, 0, 0), 3)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
