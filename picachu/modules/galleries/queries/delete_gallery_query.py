from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session
from datetime import datetime


class DeleteGalleryQuery:
    @classmethod
    def delete(cls, gallery_id: Gallery) -> int:
        current_session = session()
        try:
            gallery = current_session \
                .query(Gallery) \
                .get(gallery_id)
            gallery.deleted_at_utc = datetime.utcnow()
            current_session.commit()
            return gallery_id
        finally:
            current_session.close()
