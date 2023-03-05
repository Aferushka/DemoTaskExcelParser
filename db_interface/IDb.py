from abc import ABC, abstractmethod


class CustomDbException(Exception):
    pass


class IDb(ABC):
    def __init__(self, host: str = None, port: int = None, db_name: str = None, username: str = None,
                 password: str = None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    @abstractmethod
    def create_table(self, custom_scheme: str = None, drop_if_exists: bool = False, custom_drop_sql: str = None):
        ...

    @abstractmethod
    def create_view(self, custom_scheme: str = None):
        ...

    @abstractmethod
    def execute(self, sql_script: str):
        pass

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def close(self):
        ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()
