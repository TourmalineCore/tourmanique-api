from picachu.config.postgres_config import postgres_username, postgres_password, postgres_host, postgres_database


class ConnectionStringBuilder:
    def __init__(self):
        self.connection_string = f'postgresql+psycopg2://{postgres_username}:{postgres_password}@{postgres_host}/{postgres_database}'
        # self.connection_string = None
    def build_connection_string(
            self,
            username: str,
            password: str,
            host: str,
            database: str,
    ) -> str:
        self.connection_string = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'
        return self.connection_string

    def get_connection_string(self):
        return self.connection_string


connection_string_builder = ConnectionStringBuilder()
