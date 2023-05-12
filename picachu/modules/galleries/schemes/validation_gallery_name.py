from pydantic import BaseModel, validator


class ValidationGalleryName(BaseModel):
    gallery_name: str

    @validator('gallery_name')
    def validate_gallery_name(cls, gallery_name: str) -> [str, bool]:
        gallery_name = gallery_name.strip()
        if gallery_name == '':
            return False
        return gallery_name
