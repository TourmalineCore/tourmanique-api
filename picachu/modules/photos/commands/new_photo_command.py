from picachu.domain import Photo
from picachu.domain.dal import create_session


class NewPhotoCommand:

    def __init__(self):
        pass

    def create(self, photo_entity: Photo) -> int:
        current_session = create_session()
        try:
            current_session.add(photo_entity)
            current_session.commit()
            return photo_entity.id
        finally:
            current_session.close()
