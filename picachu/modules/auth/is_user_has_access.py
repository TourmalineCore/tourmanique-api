from picachu.domain import Gallery
from picachu.domain.data_access_layer.session import session
from picachu.modules.auth.auth_routes import USER_ID


class IsUserHasAccess:
    def __init__(self):
        pass

    @staticmethod
    def to_service(user_id):
        if user_id == USER_ID:
            return True
        return False

    @staticmethod
    def to_gallery(current_user_id, gallery_id):
        current_session = session()
        try:
            return current_session \
                .query(Gallery) \
                .filter(Gallery.user_id == current_user_id) \
                .filter(Gallery.id == gallery_id) \
                .one_or_none()
        finally:
            current_session.close()
