from http import HTTPStatus
from typing import List

from picachu.domain import Photo
from flask import request

from picachu.domain.data_access_layer.session import session


class GetSortedPhotosQuery:
    @classmethod
    def get_sorted_photos(cls, gallery_id: int, sorted_by: str, offset: int, limit: int) -> List[Photo]:
        current_session = session()

        gallery_list = current_session \
            .query(Photo) \
            .filter(Photo.gallery_id == gallery_id)

        if sorted_by == 'overallUniqueness':
            gallery_list = gallery_list.order_by(Photo.overall_uniqueness.desc())
        elif sorted_by == 'downloadDate':
            gallery_list = gallery_list.order_by(Photo.date_of_upload.desc())

        sorted_photos = gallery_list \
            .offset(offset) \
            .limit(limit) \
            .all()
        return sorted_photos
