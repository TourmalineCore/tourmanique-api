from pydantic import BaseModel


class ColorDto(BaseModel):
    red: int
    green: int
    blue: int

    class Config:
        orm_mode = True
