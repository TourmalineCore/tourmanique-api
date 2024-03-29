from http import HTTPStatus

from requests import Response

from tourmanique.domain.data_access_layer.session import session

from tourmanique.modules.galleries.queries.get_gallery_query import GetGalleryQuery


class RestoreGalleryCommand:
    @classmethod
    def restore(cls, gallery_id: int) -> int:
        gallery_entity = GetGalleryQuery().deleted_by_id(gallery_id)
        current_session = session()
        try:
            gallery_entity.deleted_at_utc = None
            current_session.add(gallery_entity)
            current_session.commit()
            return gallery_id
        finally:
            current_session.close()
