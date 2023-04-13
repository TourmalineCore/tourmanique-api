from pydantic import BaseModel, validator


class SortingParams(BaseModel):
    offset: int
    limit: int
    sorted_by: str

    @validator('offset')
    def validate_offset(cls, offset):
        if offset < 0:
            raise ValueError('Offset must be greater than or equal to 0.')
        return offset

    @validator('limit')
    def validate_limit(cls, limit):
        if limit < 0:
            raise ValueError('Limit must be greater than or equal to 0.')
        return limit

    @validator('sorted_by')
    def validate_sorted_by(cls, sorted_by):
        if sorted_by not in ['uniqueness', 'downloadDate']:
            raise ValueError('Incorrect sortedBy value.')
        return sorted_by
