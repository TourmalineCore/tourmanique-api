from http import HTTPStatus

from picachu.domain import Photo
from flask import request

from picachu.domain.data_access_layer.session import session


class GetSortedPhotosQuery:
    @classmethod
    def get_sorted_photos(cls, gallery_id: int, sorted_by: str) -> tuple[str, HTTPStatus]:
        current_session = session()
        if sorted_by == 'uniqueness':
            sorting_by_uniq = current_session \
                .query(Photo) \
                .filter(Photo.gallery_id == gallery_id) \
                .order_by(Photo.uniqueness.desc())
            return sorting_by_uniq
        elif sorted_by == 'downloadDate':
            sorting_by_date = current_session \
                .query(Photo) \
                .filter(Photo.gallery_id == gallery_id) \
                .order_by(Photo.date_of_upload.desc())
            return sorting_by_date
        else:
            return 'Bad sorting parameters', HTTPStatus.BAD_REQUEST
