from pydantic import BaseModel


class SteelMaxModel(BaseModel):
    dp: float
    min_dist: float
    param1: float
    param2: float
    min_radius: int
    max_radius: int
    img_src: str


class SteelModel(BaseModel):
    number: int | float | None
    date: str | None
    max_radius: SteelMaxModel | None


class Steel(BaseModel):
    code: int
    data: SteelModel | SteelMaxModel


class SteelTubeModel(BaseModel):
    dp: float
    min_dist: float
    param1: float
    param2: float
    min_radius: int
    max_radius: int


class SteelTube(BaseModel):
    image: str
    data: SteelTubeModel | None


