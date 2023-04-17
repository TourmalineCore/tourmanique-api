from pydantic import BaseModel, validator


class ValidationGalleryName(BaseModel):
    gallery_name: str

    @validator('gallery_name')
    def validate_gallery_name(cls, gallery_name: str) -> str:
        if gallery_name.strip() == '':
            raise ValueError('Gallery name must not be empty.')
        return gallery_name.strip()
