from picachu.domain import Association
from picachu.domain.dal import create_session


class NewAssociationCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(association_entity: Association) -> int:
        current_session = create_session()
        try:
            current_session.add(association_entity)
            current_session.commit()
            return association_entity.id
        finally:
            current_session.close()