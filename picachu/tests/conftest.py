import datetime

import pytest
from flask_jwt_extended import create_access_token

from application import create_app
from picachu.modules.auth.auth_routes import log_in, USER_ID


@pytest.fixture(scope='session')
def flask_app():
    app = create_app()

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope='session')
def access_token(flask_app):
    access_token = create_access_token(identity=USER_ID,
                                       expires_delta=datetime.timedelta(days=30))
    return access_token
