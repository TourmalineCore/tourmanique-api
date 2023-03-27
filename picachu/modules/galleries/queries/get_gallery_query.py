from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session


class GetGalleryQuery:
    def __init__(self):
        pass

    @staticmethod
    def by_id(gallery_id):
        current_session = session()
        try:
            return current_session \
                .query(Gallery) \
                .filter(Gallery.id == gallery_id) \
                .one_or_none()
        finally:
            current_session.close()
