from pydantic import BaseModel


class EmotionDto(BaseModel):
    name: str

    class Config:
        orm_mode = True
