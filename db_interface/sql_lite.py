import sqlite3

from .IDb import IDb, CustomDbException
from .sqlite_queries import CREATE_TABLE, CREATE_VIEW, DROP_TABLE


class CustomSqLiteSomeErrorException(CustomDbException):
    pass


class SqLite(IDb):
    def commit(self):
        self.connection.commit()

    def create_view(self, custom_scheme: str = None):
        self.cursor.executescript(custom_scheme if custom_scheme else CREATE_VIEW)

    def execute(self, sql_script: str):
        self.cursor.execute('{}'.format(sql_script))
        return self.cursor.fetchall()

    def create_table(self, custom_scheme: str = None, drop_if_exists: bool = False, custom_drop_sql: str = None):
        self.cursor.execute(custom_drop_sql or DROP_TABLE)
        self.cursor.executescript(custom_scheme or CREATE_TABLE)

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise CustomSqLiteSomeErrorException(f'You need something to do with this: {e}')

    def close(self):
        self.connection.close()
