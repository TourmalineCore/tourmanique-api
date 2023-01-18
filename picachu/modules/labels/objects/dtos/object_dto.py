from pydantic import BaseModel


class ObjectDto(BaseModel):
    name: str

    class Config:
        orm_mode = True
