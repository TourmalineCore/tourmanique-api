from typing import List

from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session


class GetGalleriesQuery:
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
