from typing import List

from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session


class GetGalleryQuery:
    def __init__(self):
        pass

    @staticmethod
    def by_id(gallery_id: int) -> int:
        current_session = session()
        try:
            return current_session \
                .query(Gallery) \
                .filter(Gallery.id == gallery_id) \
                .one_or_none()
        finally:
            current_session.close()

    @classmethod
    def by_user_id(cls, current_user_id: int) -> List:
        current_session = session()
        try:
            galleries_list = current_session \
                .query(Gallery) \
                .filter(Gallery.user_id == current_user_id) \
                .all()
            return galleries_list
        finally:
            current_session.close()
