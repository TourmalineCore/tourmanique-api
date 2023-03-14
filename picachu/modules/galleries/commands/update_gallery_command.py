from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session
from picachu.modules.galleries.queries.get_gallery_query import GetGalleryQuery


class UpdateGalleryCommand:
    @classmethod
    def rename(cls, new_gallery_name: str, gallery_id: int):
        current_session = session()
        try:
            gallery_entity = GetGalleryQuery().by_id(gallery_id)
            gallery_entity.name = new_gallery_name
            current_session.add(gallery_entity)
            current_session.commit()
            return gallery_entity.name
        finally:
            current_session.close()