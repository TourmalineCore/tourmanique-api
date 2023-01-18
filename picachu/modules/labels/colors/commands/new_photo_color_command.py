from picachu.domain import PhotoColor
from picachu.domain.dal import create_session
from picachu.modules.labels.emotions.commands.new_emotion_command import NewEmotionCommand
from picachu.modules.labels.emotions.queries.get_emotions_query import GetEmotionQuery


class NewPhotoColorCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(color_entity: PhotoColor, photo_id: int) -> int:
        current_session = create_session()
        color_entity.photo_id=photo_id

        try:
            current_session.add(color_entity)
            current_session.commit()

        finally:
            current_session.close()

