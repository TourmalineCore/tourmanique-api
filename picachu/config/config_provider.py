from picachu.config.flask_config import env, debug
from picachu.config.jwt_config import jwt_secret_key
from picachu.config.postgres_config import postgres_database, postgres_host, postgres_password, postgres_username
from picachu.domain.data_access_layer.engine import app_db_engine_provider


class ConfigProvider:
    ENV = env
    DEBUG = debug
    JWT_SECRET_KEY = jwt_secret_key
    SQLALCHEMY_DATABASE_URI = app_db_engine_provider.build_engine_string(
        database=postgres_database,
        host=postgres_host,
        password=postgres_password,
        username=postgres_username,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfigProvider(ConfigProvider):
    SQLALCHEMY_DATABASE_URI = app_db_engine_provider.build_engine_string(
        database='test_db',
        host='test-db',
        password='postgres',
        username='postgres',
    )
