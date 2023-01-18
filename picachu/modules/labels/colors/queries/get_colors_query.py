from picachu.domain import PhotoColor
from picachu.domain.dal import create_session


class GetColorQuery:
    def __init__(self):
        pass

    def by_photo_id(self, photo_id):
        current_session = create_session()
        try:

            return current_session \
                .query(PhotoColor) \
                .filter(PhotoColor.photo_id == photo_id) \
                .all()

        finally:
            current_session.close()
