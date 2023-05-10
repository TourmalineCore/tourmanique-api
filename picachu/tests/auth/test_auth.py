import logging
import pytest

from sqlalchemy import INTEGER, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import VARCHAR
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine, select
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"

    ID = Column("id", INTEGER, primary_key=True)
    Name = Column("name", VARCHAR(20), nullable=False)

    def __repr__(self):
        return "<Person(Name='%s')>" % (self.Name)

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

test_db = factories.postgresql_proc(port=None, dbname="test_db", executable="/usr/lib/postgresql/13/bin/createdb")


@pytest.fixture(scope="session")
def db_session(test_db):
    """Session for SQLAlchemy."""
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_password = test_db.password
    pg_db = test_db.dbname

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = f"postgresql+psycopg2://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(connection_str)
        with engine.connect() as con:
            Base.metadata.create_all(con)
            logger.info("yielding a sessionmaker against the test postgres db.")

            yield sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="module")
def create_test_data():
    """Let's create the test data with the three witches names."""
    names = ["Winifred", "Sarah", "Mary"]
    test_objs = []
    for idx, name in zip(range(3), names):
        test_objs.append(Person(ID=idx, Name=name))

    return test_objs


def test_persons(db_session, create_test_data):
    s = db_session()
    for obj in create_test_data:
        s.add(obj)
    s.commit()
    logger.info("Added test data to the database.")

    query_result = s.execute(select(Person)).all()
    s.close()

    assert create_test_data[0].Name in str(query_result)
# import pytest
# from pytest_postgresql import factories
# from sqlalchemy import create_engine, text, Float
# from sqlalchemy.dialects.postgresql import psycopg2
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
#
# # Base = declarative_base()
#
# # postgresql_my_proc = factories.postgresql_proc(
# #     # initdb_args=["--encoding=UTF8", "--locale=en_US.UTF-8"],
# #     # pg_ctl="/usr/local/bin/postgres",
# #     # postgresql_bin="/usr/lib/postgresql/13/bin/",
# #     host='postgrehost',
# #     port=5432,
# #     dbname="testdb",
# #     user="testuser",
# #     password="testpass",
# #     load=[create_tables],
# # )
# #
# # postgresql_my = factories.postgresql('postgresql_my_proc')
#
# def load_database(**kwargs):
#     db_connection = psycopg2.connect(**kwargs)
#     with db_connection.cursor() as cur:
#         cur.execute("CREATE TABLE stories (id serial PRIMARY KEY, name varchar);")
#         cur.execute(
#             "INSERT INTO stories (name) VALUES"
#             "('Silmarillion'), ('Star Wars'), ('The Expanse'), ('Battlestar Galactica')"
#         )
#         db_connection.commit()
#
#
# postgresql_proc = factories.postgresql_proc(
#     unixsocketdir='/var/run',
#     load=[load_database],
# )
#
# postgresql = factories.postgresql(
#     "postgresql_proc",
# )
#
#
# def test_example_postgres(postgresql):
#     """Check main postgresql fixture."""
#     cur = postgresql.cursor()
#     cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
#     postgresql.commit()
#     cur.close()
#
# # class User(Base):
# #     __tablename__ = 'users'
# #
# #     id = Column(Integer, primary_key=True)
# #     name = Column(String, nullable=False)
# #     email = Column(String, unique=True, nullable=False)
# #
# # class Product(Base):
# #     __tablename__ = 'products'
# #
# #     id = Column(Integer, primary_key=True)
# #     name = Column(String, nullable=False)
# #     price = Column(Float, nullable=False)
# #
# #
# # # Подключаемся к тестовой базе данных
# # @pytest.fixture
# # def postgres_connection(postgresql):
# #     engine = create_engine(
# #         f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}',
# #         echo=True # можно отключить
# #     )
# #     connection = engine.connect()
# #     yield connection
# #     connection.close()
# #
# # # Создаем схему тестовой базы данных перед началом тестирования
# # # @pytest.fixture()
# # # def create_tables(postgres_connection):
# # #     with postgres_connection.begin() as connection:
# # #         connection.execute(text('DROP TABLE IF EXISTS users CASCADE'))
# # #         connection.execute(text('DROP TABLE IF EXISTS products CASCADE'))
# # #
# # #         connection.execute(text('''
# # #             CREATE TABLE users (
# # #                 id SERIAL PRIMARY KEY,
# # #                 name TEXT NOT NULL,
# # #                 email TEXT NOT NULL UNIQUE
# # #             )
# # #         '''))
# # #
# # #         connection.execute(text('''
# # #             CREATE TABLE products (
# # #                 id SERIAL PRIMARY KEY,
# # #                 name TEXT NOT NULL,
# # #                 price NUMERIC(10, 2) NOT NULL
# # #             )
# # #         '''))
# #
# # # Создаем сессию SQLAlchemy для тестовой базы данных
# # @pytest.fixture
# # def db_session(postgres_connection):
# #     Session = sessionmaker(bind=postgres_connection)
# #     session = Session()
# #     yield session
# #     session.close()
# #
# # # Тест на добавление нового пользователя
# # def test_add_user(db_session):
# #     user = User(name='John Doe', email='john.doe@example.com')
# #     db_session.add(user)
# #     db_session.commit()
# #
# #     count = db_session.query(User).count()
# #     assert count == 1
# #
# # # Тест на добавление нового продукта
# # def test_add_product(db_session):
# #     product = Product(name='Product 1', price=10.99)
# #     db_session.add(product)
# #     db_session.commit()
# #
# #     count = db_session.query(Product).count()
# #     assert count == 1
# #
#
#
# # ############
# # import pytest
# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import scoped_session, sessionmaker
# # from sqlalchemy.pool import NullPool
# # from zope.sqlalchemy import register
# #
# #
# # @pytest.fixture
# # def db_session(postgresql):
# #     """Session for SQLAlchemy."""
# #     # from pyramid_fullauth.models import Base
# #
# #     connection = f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
# #
# #     engine = create_engine(connection, echo=False, poolclass=NullPool)
# #     # pyramid_basemodel.Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
# #     pyramid_basemodel.bind_engine(
# #         engine, pyramid_basemodel.Session, should_create=True, should_drop=True)
# #
# #     yield pyramid_basemodel.Session
# #
# #     transaction.commit()
# #     Base.metadata.drop_all(engine)
# #
# #
# # @pytest.fixture
# # def user(db_session):
# #     """Test user fixture."""
# #     from pyramid_fullauth.models import User
# #     from tests.tools import DEFAULT_USER
# #
# #     new_user = User(**DEFAULT_USER)
# #     db_session.add(new_user)
# #     transaction.commit()
# #     return new_user
# #
# #
# # def test_remove_last_admin(db_session, user):
# #     """
# #     Sample test checks internal login, but shows usage in tests with SQLAlchemy
# #     """
# #     user = db_session.merge(user)
# #     user.is_admin = True
# #     transaction.commit()
# #     user = db_session.merge(user)
# #
# #     with pytest.raises(AttributeError):
# #         user.is_admin = False
# #
# # ############################
# #
# # # import psycopg2
# # # import pytest
# # # from pytest_postgresql import factories
# # #
# # # postgresql_my_proc = factories.postgresql_proc(
# # #     # initdb_args=["--encoding=UTF8", "--locale=en_US.UTF-8"],
# # #     # pg_ctl="/usr/local/bin/postgres",
# # #     # postgresql_bin="/usr/lib/postgresql/13/bin/",
# # #     port=5432,
# # #     dbname="pytest",
# # #     user="pytest",
# # #     password="pytest",
# # # )
# # # postgresql_my = factories.postgresql('postgresql_my_proc')
# # #
# # # print('Start')
# # # # Создание фабрики для базы данных PostgreSQL
# # # # postgresql_my_proc = factories.postgresql_proc(port=None)
# # # print('Создание фабрики')
# # #
# # # # Фикстура для создания соединения с базой данных
# # # @pytest.fixture(scope='function')
# # # def db_conn(postgresql_my_proc):
# # #     print('db_conn')
# # #     conn = psycopg2.connect(**postgresql_my_proc.dsn())
# # #     yield conn
# # #     conn.close()
# # #
# # #
# # # # Фикстура для создания таблицы для тестов в базе данных
# # # @pytest.fixture(scope='function')
# # # def setup_table(db_conn):
# # #     print('setup_table')
# # #     cursor = db_conn.cursor()
# # #     cursor.execute("CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR);")
# # #     db_conn.commit()
# # #     yield
# # #     cursor.execute("DROP TABLE test_table;")
# # #     db_conn.commit()
# # #
# # #
# # # # Тест для проверки добавления данных в таблицу
# # # def test_insert_data(db_conn, setup_table):
# # #     print('test_insert_data')
# # #     cursor = db_conn.cursor()
# # #     cursor.execute("INSERT INTO test_table (name) VALUES ('test_data');")
# # #     db_conn.commit()
# # #     cursor.execute("SELECT * FROM test_table;")
# # #     rows = cursor.fetchall()
# # #     assert rows[0][1] == 'test_data'
# # #     assert len(rows) == 1
# # #
# # #
# # # # from picachu.domain.data_access_layer.db import db
# # # # from picachu.config.postgres_config import postgres_username, postgres_host, postgres_database, postgres_password
# # # #
# # # # import pytest
# # # # from sqlalchemy import create_engine
# # # # from sqlalchemy.orm import sessionmaker
# # # # from pytest_postgresql import factories
# # # #
# # # #
# # # # socket_dir = tempfile.TemporaryDirectory()
# # # # postgresql_my_proc = factories.postgresql_proc(
# # # #     port=None, unixsocketdir=socket_dir.name)
# # # # postgresql_my = factories.postgresql('postgresql_my_proc')
# # # #
# # # #
# # # # @pytest.fixture(scope='function')
# # # # def setup_database(postgresql_my):
# # # #
# # # #     def dbcreator():
# # # #         return postgresql_my.cursor().connection
# # # #
# # # #     connect = f'postgresql+psycopg2://{postgres_username}:@{postgres_password}:{postgres_host}/{postgres_database}'
# # # #     create_engine(db)
# # # #     # engine = create_engine('postgresql+psycopg2://', creator=dbcreator)
# # # #     Base.metadata.create_all(engine)
# # # #     Session = sessionmaker(bind=engine)
# # # #     session = Session()
# # # #     yield session
# # # #     session.close()
# # # #
# # # # # end setup_database()
# # #
# # # # import pytest
# # # # from flask import url_for
# # # #
# # # # from picachu.config.auth_config import auth_username, auth_password
# # # #
# # # #
# # # # def test_log_in_happy_path(flask_app):
# # # #     data = {
# # # #         'login': auth_username,
# # # #         'password': auth_password,
# # # #     }
# # # #
# # # #     response = flask_app.post(url_for('api.auth.log_in'), json=data)
# # # #
# # # #     assert response.status_code == 200
# # # #
# # # #
# # # # @pytest.mark.parametrize(
# # # #     'login, password',
# # # #     [
# # # #         ('Admin', 'admin'),
# # # #         ('ADMIN', 'ADMIN'),
# # # #         ('admin2', 'admin2'),
# # # #         ('', 'admin2'),
# # # #         ('', ''),
# # # #         ('admin2', ''),
# # # #     ]
# # # #     )
# # # # def test_log_in_unhappy_path(login, password, flask_app):
# # # #     data = {
# # # #         'login': login,
# # # #         'password': password,
# # # #     }
# # # #
# # # #     response = flask_app.post(url_for('api.auth.log_in'), json=data)
# # # #     assert response.status_code == 401
