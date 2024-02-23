from typing import Any

import numpy as np

from log import logs
from ulits import public_way

logger = logs.Logger()


class AutoAdapt:
    def __init__(self):
        self.result = []

    def get_max_radius(self, image) -> bool | int | Any:
        gray, flag = public_way.gray_image(image)
        if not flag:
            logger.error("Can't get gray image")
            return False
        circles = public_way.get_steel_coordinate(gray, 1, 20, 50.0, 30.0, 10, 20)
        circles = circles.astype(np.float64)
        for circle in circles[0]:
            x, y, radius = circle
            self.result.append(np.ceil(radius))
        return max(self.result) + 2
