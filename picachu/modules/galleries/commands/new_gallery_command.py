from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session


class NewGalleryCommand:
    @classmethod
    def create(cls, gallery_entity: Gallery) -> int:
        current_session = session()
        try:
            current_session.add(gallery_entity)
            current_session.commit()
            return gallery_entity.id
        finally:
            current_session.close()
