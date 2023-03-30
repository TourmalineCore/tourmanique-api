from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session
from datetime import datetime

from picachu.modules.galleries.queries.get_gallery_query import GetGalleryQuery


class DeleteGalleryCommand:
    @classmethod
    def delete(cls, gallery_id: int) -> int:
        gallery_entity = GetGalleryQuery().by_id(gallery_id)
        current_session = session()
        try:
            gallery_entity.deleted_at_utc = datetime.utcnow()
            current_session.add(gallery_entity)
            current_session.commit()
            return gallery_id
        finally:
            current_session.close()
