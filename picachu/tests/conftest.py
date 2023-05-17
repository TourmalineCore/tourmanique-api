import datetime

import pytest
from flask_jwt_extended import create_access_token

from application import create_app
from picachu.domain import Gallery
from picachu.domain.data_access_layer.db import db
from picachu.modules.auth.auth_routes import USER_ID


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
    """Create access token"""
    access_token = create_access_token(identity=USER_ID,
                                       expires_delta=datetime.timedelta(days=30))
    return access_token


@pytest.fixture(scope='module')
def add_gallery():
    """Create new gallery"""
    gallery = Gallery(name='Test Gallery')
    db.session.add(gallery)
    db.session.commit()
    yield gallery
    db.session.delete(gallery)
    db.session.commit()

