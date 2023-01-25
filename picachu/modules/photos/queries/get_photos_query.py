from picachu.domain import Photo
from picachu.domain.dal import create_session


class GetPhotoQuery:

    def __init__(self):
        pass

    def by_id(self, photo_id):
        current_session = create_session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.id == photo_id) \
                .one_or_none()

        finally:
            current_session.close()

    def by_s3_path(self, photo_path_in_s3):
        current_session = create_session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.photo_file_path_s3 == photo_path_in_s3) \
                .one_or_none()

        finally:
            current_session.close()
