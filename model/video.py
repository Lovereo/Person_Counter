from typing import List

from pydantic import BaseModel


class Number(BaseModel):
    value: str


class Error(BaseModel):
    value: str


class IsAlive(BaseModel):
    name: str
    value: int
