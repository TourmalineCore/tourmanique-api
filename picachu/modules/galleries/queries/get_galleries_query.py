from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session


class GetGalleriesQuery:
    @classmethod
    def get(cls, current_user_id) -> int:
        current_session = session()
        try:
            list_galleries = current_session \
                .query(Gallery) \
                .filter(Gallery.user_id == current_user_id) \
                .all()
            return list_galleries
        finally:
            current_session.close()
