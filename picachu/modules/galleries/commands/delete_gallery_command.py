from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session
from datetime import datetime

from picachu.modules.galleries.queries.delete_gallery_query import DeleteGalleryQuery


class DeleteGalleryCommand:
    @classmethod
    def delete(cls, gallery_id: Gallery) -> int:
        gallery_entity = DeleteGalleryQuery().by_id(gallery_id)
        current_session = session()
        try:
            gallery_entity.deleted_at_utc = datetime.utcnow()
            current_session.add(gallery_entity)
            current_session.commit()
            return gallery_id
        finally:
            current_session.close()
