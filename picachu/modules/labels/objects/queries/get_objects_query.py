from picachu.domain import Object, photo_object_table, Photo
from picachu.domain.dal import create_session


class GetObjectQuery:
    def __init__(self):
        pass

    def by_photo_id(self, photo_id):
        current_session = create_session()
        try:
            return current_session \
                .query(Object) \
                .join(photo_object_table) \
                .join(Photo) \
                .filter(photo_object_table.c.photo_id == photo_id) \
                .all()

        finally:
            current_session.close()

    def by_name(self, object_name):
        current_session = create_session()
        try:
            return current_session \
                .query(Object) \
                .filter(Object.name == object_name) \
                .one_or_none()

        finally:
            current_session.close()