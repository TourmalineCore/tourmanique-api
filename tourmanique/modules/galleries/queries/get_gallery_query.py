from typing import Optional, List

from tourmanique.domain import Gallery
from tourmanique.domain.data_access_layer.session import session


class GetGalleryQuery:
    def __init__(self):
        pass

    @classmethod
    def by_id(cls, gallery_id: int) -> Optional[Gallery]:
        current_session = session()
        try:
            return current_session \
                .query(Gallery) \
                .filter(Gallery.deleted_at_utc == None) \
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
                .filter(Gallery.deleted_at_utc == None) \
                .filter(Gallery.user_id == current_user_id) \
                .all()
            return galleries_list
        finally:
            current_session.close()

    @classmethod
    def deleted_by_id(cls, gallery_id: int) -> Optional[Gallery]:
        current_session = session()
        try:
            return current_session \
                .query(Gallery) \
                .filter(Gallery.deleted_at_utc != None) \
                .filter(Gallery.id == gallery_id) \
                .one_or_none()
        finally:
            current_session.close()