from picachu.domain import PhotoColor
from picachu.domain.dal import create_session


class NewColorCommand:
    def __init__(self):
        pass

    @staticmethod
    def create_color(color_entity: PhotoColor) -> int:
        current_session = create_session()
        try:
            current_session.add(color_entity)
            current_session.commit()
            return color_entity.id
        finally:
            current_session.close()
