from picachu.domain import photo_emotion_table, Association, photo_association_table
from picachu.domain.dal import create_session
from picachu.modules.labels.associations.commands.new_association_command import NewAssociationCommand
from picachu.modules.labels.associations.queries.get_association_query import GetAssociationQuery
from picachu.modules.labels.emotions.commands.new_emotion_command import NewEmotionCommand
from picachu.modules.labels.emotions.queries.get_emotions_query import GetEmotionQuery



class NewPhotoAssociationCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(association_entity: Association, photo_id: int) -> int:
        current_session = create_session()
        association = GetAssociationQuery().by_name(association_entity.name)
        if not association:
            association_id = NewAssociationCommand().create(association_entity)
        else:
            association_id = association.id
        try:
            statement = photo_association_table.insert().values(photo_id=photo_id,
                                                                association_id=association_id)
            current_session.execute(statement)
            current_session.commit()

        finally:
            current_session.close()
