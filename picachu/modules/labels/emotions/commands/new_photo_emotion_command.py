from picachu.domain import Emotion, photo_emotion_table
from picachu.domain.dal import create_session
from picachu.modules.labels.emotions.commands.new_emotion_command import NewEmotionCommand
from picachu.modules.labels.emotions.queries.get_emotions_query import GetEmotionQuery



class NewPhotoEmotionCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(emotion_entity: Emotion, photo_id: int) -> int:
        current_session = create_session()
        emotion = GetEmotionQuery().by_name(emotion_entity.name)
        if not emotion:
            emotion_id = NewEmotionCommand().create(emotion_entity)
        else:
            emotion_id = emotion.id
        try:
            statement = photo_emotion_table.insert().values(photo_id=photo_id,
                                                            emotion_id=emotion_id)
            current_session.execute(statement)
            current_session.commit()

        finally:
            current_session.close()
