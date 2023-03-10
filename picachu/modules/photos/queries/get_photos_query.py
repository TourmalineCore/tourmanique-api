from picachu.domain import Photo
from picachu.domain.data_access_layer.session import session


class GetPhotoQuery:

    def __init__(self):
        pass

    @staticmethod
    def by_id(photo_id):
        current_session = session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.id == photo_id) \
                .one_or_none()

        finally:
            current_session.close()

    @staticmethod
    def by_s3_path(photo_path_in_s3):
        current_session = session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.photo_file_path_s3 == photo_path_in_s3) \
                .one_or_none()

        finally:
            current_session.close()
