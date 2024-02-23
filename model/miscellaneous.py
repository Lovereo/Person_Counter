from pydantic import BaseModel
from typing import List


class ToolsList(BaseModel):
    name: str
    src: str
    serial_number: str
    img_src: str


class ToolsListResponse(BaseModel):
    code: int
    data: List[ToolsList]
