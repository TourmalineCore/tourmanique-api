from picachu.modules.auth.auth_routes import USER_ID


class IsUserHasAccess:
    def to_service(self, user_id):
        if user_id == USER_ID:
            return True
        return False