from picachu.domain import Photo
from picachu.domain.data_access_layer.session import session


class GetPhotosInGalleryQuery:
    @classmethod
    def get_photos_in_gallery(cls, gallery_id, offset, limit) -> int:
        current_session = session()
        try:
            list_photos = current_session \
                .query(Photo) \
                .filter(Photo.gallery_id == gallery_id) \
                .offset(offset) \
                .limit(limit) \
                .all()
            return list_photos
        finally:
            current_session.close()
