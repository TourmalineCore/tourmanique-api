from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session
from picachu.modules.auth.auth_routes import USER_ID
from sqlalchemy.sql import exists

class IsUserHasAccess:
    def to_service(self, user_id):
        if user_id == USER_ID:
            return True
        return False

    @staticmethod
    def to_gallery(user_id):
        current_session = session()
        try:
            return current_session \
                .query(exists().where(Gallery.user_id == user_id)) \
                .scalar()
        finally:
            current_session.close()
# toDo: update BD
