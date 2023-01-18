from picachu.domain import Emotion
from picachu.domain.dal import create_session


class NewEmotionCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(emotion_entity: Emotion) -> int:
        current_session = create_session()
        try:
            current_session.add(emotion_entity)
            current_session.commit()
            return emotion_entity.id
        finally:
            current_session.close()