from pydantic import BaseModel, validator


class PaginationParams(BaseModel):
    offset: int
    limit: int

    @validator('offset')
    def validate_offset(cls, offset):
        if offset < 0:
            raise ValueError('offset must be greater than or equal to 0')
        return offset

    @validator('limit')
    def validate_limit(cls, limit):
        if limit < 0:
            raise ValueError('limit must be greater than or equal to 0')
        return limit
