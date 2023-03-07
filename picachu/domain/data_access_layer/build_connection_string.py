from picachu.config.postgres_config import postgres_username, postgres_host, postgres_database, postgres_password


def _build_full_connection_string(password):
    return f'postgresql+psycopg2://{postgres_username}:{password}@{postgres_host}/{postgres_database}'


def build_connection_string():
    return _build_full_connection_string(postgres_password)
