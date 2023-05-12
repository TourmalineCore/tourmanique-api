from application import create_app
import logging

import pytest

from pytest_postgresql import factories
from sqlalchemy import create_engine, select
from sqlalchemy.orm.session import sessionmaker

from picachu.domain import Gallery
from picachu.domain.data_access_layer.db import db


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

test_db_proc = factories.postgresql_proc(executable='./pg_ctl.sh',
                                         dbname="picachu_test_db")
test_db = factories.postgresql('test_db_proc')


@pytest.fixture
def flask_app():
    app = create_app()
    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture
def setup_database(flask_app, test_db):
    def dbcreator():
        return test_db.cursor().connection

    engine = create_engine("postgresql+psycopg2://", creator=dbcreator)
    db.metadata.create_all(engine)

    return engine


@pytest.fixture
def db_session(flask_app, setup_database):
    engine = setup_database
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return session_factory


@pytest.fixture
def create_test_data(flask_app, db_session):
    test_objs = []
    galleries_names = ['gallery_1', 'gallery_2', 'gallery_3']
    galleries_user_id = ['1', '1', '2']

    session = db_session()
    for name, user_id in zip(galleries_names, galleries_user_id):
        session.add(Gallery(user_id=user_id,
                            name=name))
    session.commit()
    logger.info("Added test data to the database.")

    return test_objs
