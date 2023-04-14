from pydantic import BaseModel, validator


class ValidationGallery(BaseModel):
    new_gallery_name: str

    @validator('new_gallery_name')
    def validate_new_gallery_name(cls, new_gallery_name: str) -> str:
        if new_gallery_name == '':
            raise ValueError('new_gallery_name must not be empty.')
        return new_gallery_name
