from picachu.domain import Association, photo_association_table, Photo
from picachu.domain.dal import create_session


class GetAssociationQuery:

    def __init__(self):
        pass

    def by_name(self, association_name):
        current_session = create_session()
        try:
            return current_session \
                .query(Association) \
                .filter(Association.name == association_name) \
                .one_or_none()
        finally:
            current_session.close()

    def by_photo_id(self, photo_id):
        current_session = create_session()
        try:
            return current_session \
                .query(Association) \
                .join(photo_association_table) \
                .join(Photo) \
                .filter(photo_association_table.c.photo_id == photo_id) \
                .all()

        finally:
            current_session.close()
