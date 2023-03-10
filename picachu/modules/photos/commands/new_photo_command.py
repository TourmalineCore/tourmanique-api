from picachu.domain import Photo
from picachu.domain.data_access_layer.session import session


class NewPhotoCommand:

    def __init__(self):
        pass

    @staticmethod
    def create(photo_entity: Photo) -> int:
        current_session = session()
        try:
            current_session.add(photo_entity)
            current_session.commit()
            return photo_entity.id
        finally:
            current_session.close()
