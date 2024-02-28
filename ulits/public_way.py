import asyncio
import socket
import time
import webbrowser

import cv2
import os
import sys

from fastapi import HTTPException, UploadFile, File
from uvicorn import run

from log import logs
import subprocess

logger = logs.Logger()


def check_system() -> int:
    if sys.platform.startswith('linux'):
        logger.info('当前系统为 Linux')
        return 1
    elif sys.platform.startswith('win'):
        logger.info('当前系统为 Windows')
        return 2
    elif sys.platform.startswith('darwin'):
        logger.info('当前系统为 macOS')
        return 3


def get_time() -> str:
    if check_system() == 1:
        return time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())
    elif check_system() == 2:
        return time.strftime('%Y-%m-%d', time.localtime())
    elif check_system() == 3:
        return time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime())


def get_steel_coordinate(image, dp, min_dist, param1, param2,
                         min_radius, max_radius):
    return cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, min_dist, param1=param1,
                            param2=param2, minRadius=min_radius, maxRadius=max_radius)


def gray_image(enter_image):
    enter_image = cv2.imread(enter_image)
    if enter_image is None:
        return
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    image = cv2.morphologyEx(enter_image, cv2.MORPH_GRADIENT, se)
    if image is not None:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), True
    return None, False


async def save_image(image: UploadFile = File(...)):
    try:
        file_extension = image.filename
        file_path = "images/" + file_extension

        with open(file_path, "wb") as file:
            file.write(image.file.read())

        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")


def check_files(file_name: str):
    if os.path.isdir(file_name):
        logger.error("Output folder is live")
    else:
        os.mkdir(file_name)


def check_variables(*args):
    for variable in args:
        if variable is None:
            return False
    return True


def send_tcp_request(hex_data):
    # 将十六进制字符串转换为字节
    data = bytes.fromhex(hex_data)

    # 创建 TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到服务器
        s.connect(("192.168.3.253", 1030))

        # 发送数据
        s.sendall(data)
        print(f"Sent Hex Data: {hex_data}")

        # 接收数据
        received_data = s.recv(1024)
        print(f"Received Hex Data: {received_data.hex()}")


class PublicWay:
    def __init__(self):
        return

    def get_min_radius(self) -> None:
        return
