from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session
from picachu.modules.auth.auth_routes import USER_ID


class IsUserHasAccess:
    def to_service(self, user_id):
        if user_id == USER_ID:
            return True
        return False

    @staticmethod
    def to_gallery(current_user_id):
        current_session = session()
        try:
            return current_session \
                .query(Gallery) \
                .filter(Gallery.user_id == current_user_id) \
                .all()
        finally:
            current_session.close()
