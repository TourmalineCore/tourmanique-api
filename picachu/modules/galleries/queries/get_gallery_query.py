from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session


class GetGalleryQuery:
    def __init__(self):
        pass

    @classmethod
    def by_id(cls, gallery_id: Gallery) -> int:
        current_session = session()
        try:
            return current_session \
                .query(Gallery) \
                .get(gallery_id)
        finally:
            current_session.close()
