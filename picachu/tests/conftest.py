import pytest

from application import create_app


@pytest.fixture(scope='session')
def flask_app():
    app = create_app()
    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()
