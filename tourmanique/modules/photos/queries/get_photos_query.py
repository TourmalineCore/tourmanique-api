from typing import List

from tourmanique.domain import Photo, Gallery
from tourmanique.domain.data_access_layer.session import session


class GetPhotoQuery:

    def __init__(self):
        pass

    @staticmethod
    def by_id(photo_id):
        current_session = session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.id == photo_id) \
                .one_or_none()

        finally:
            current_session.close()

    @staticmethod
    def by_s3_path(photo_path_in_s3):
        current_session = session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.photo_file_path_s3 == photo_path_in_s3) \
                .one_or_none()

        finally:
            current_session.close()

    @staticmethod
    def count_photos(gallery_id: int) -> int:
        current_session = session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.gallery_id == gallery_id) \
                .count()
        finally:
            current_session.close()

    @staticmethod
    def for_gallery_preview(gallery_id) -> List[Photo]:
        current_session = session()
        try:
            photos_list = current_session \
                .query(Photo) \
                .filter(Photo.gallery_id == gallery_id) \
                .order_by(Photo.date_of_upload.desc()) \
                .limit(4) \
                .all()
            return photos_list
        finally:
            current_session.close()
