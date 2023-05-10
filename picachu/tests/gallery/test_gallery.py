# import psycopg2
# import pytest
# from pytest_postgresql import factories
#
# # Создание фабрики для базы данных PostgreSQL
# postgresql_my_proc = factories.postgresql_proc(port=None)
#
#
# # Фикстура для создания соединения с базой данных
# @pytest.fixture(scope='function')
# def db_conn(postgresql_my_proc):
#     conn = psycopg2.connect(**postgresql_my_proc.dsn())
#     yield conn
#     conn.close()
#
#
# # Фикстура для создания таблицы для тестов в базе данных
# @pytest.fixture(scope='function')
# def setup_table(db_conn):
#     cursor = db_conn.cursor()
#     cursor.execute("CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR);")
#     db_conn.commit()
#     yield
#     cursor.execute("DROP TABLE test_table;")
#     db_conn.commit()
#
#
# # Тест для проверки добавления данных в таблицу
# def test_insert_data(db_conn, setup_table):
#     cursor = db_conn.cursor()
#     cursor.execute("INSERT INTO test_table (name) VALUES ('test_data');")
#     db_conn.commit()
#     cursor.execute("SELECT * FROM test_table;")
#     rows = cursor.fetchall()
#     assert len(rows) == 1
#     assert rows[0][1] == 'test_data'
#
#
# # from picachu.domain.data_access_layer.db import db
# # from picachu.config.postgres_config import postgres_username, postgres_host, postgres_database, postgres_password
# #
# # import pytest
# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker
# # from pytest_postgresql import factories
# #
# #
# # socket_dir = tempfile.TemporaryDirectory()
# # postgresql_my_proc = factories.postgresql_proc(
# #     port=None, unixsocketdir=socket_dir.name)
# # postgresql_my = factories.postgresql('postgresql_my_proc')
# #
# #
# # @pytest.fixture(scope='function')
# # def setup_database(postgresql_my):
# #
# #     def dbcreator():
# #         return postgresql_my.cursor().connection
# #
# #     connect = f'postgresql+psycopg2://{postgres_username}:@{postgres_password}:{postgres_host}/{postgres_database}'
# #     create_engine(db)
# #     # engine = create_engine('postgresql+psycopg2://', creator=dbcreator)
# #     Base.metadata.create_all(engine)
# #     Session = sessionmaker(bind=engine)
# #     session = Session()
# #     yield session
# #     session.close()
# #
# # # end setup_database()