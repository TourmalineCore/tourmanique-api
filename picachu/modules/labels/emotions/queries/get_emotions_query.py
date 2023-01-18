from picachu.domain import Photo, Emotion
from picachu.domain.association_tables.association_tables import photo_emotion_table
from picachu.domain.dal import create_session


class GetEmotionQuery:

    def __init__(self):
        pass

    def by_photo_id(self, photo_id):
        current_session = create_session()
        try:
            return current_session \
                .query(Emotion) \
                .join(photo_emotion_table) \
                .join(Photo) \
                .filter(photo_emotion_table.c.photo_id == photo_id) \
                .one_or_none()

        finally:
            current_session.close()


    def by_name(self, emotion_name):
        current_session = create_session()
        try:
            return current_session \
                .query(Emotion) \
                .filter(Emotion.name == emotion_name) \
                .one_or_none()
        finally:
            current_session.close()
