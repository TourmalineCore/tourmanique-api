from picachu.domain import Object
from picachu.domain.dal import create_session


class NewObjectCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(object_entity: Object) -> int:
        current_session = create_session()
        try:
            current_session.add(object_entity)
            current_session.commit()
            return object_entity.id
        finally:
            current_session.close()