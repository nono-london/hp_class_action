import platform
import sys
from typing import Union
from mysql.connector import MySQLConnection
import mysql.connector
from mysql.connector.errors import (ProgrammingError)

from hp_class_action.app_config_secret import (MYSQL_USERNAME, MYSQL_DATABASE_NAME,
                                               MYSQL_HOST_URL, MYSQL_PORT,
                                               MYSQL_PASSWORD, PA_MYSQL_PORT,
                                               PA_MYSQL_USERNAME, PA_MYSQL_PASSWORD,
                                               PA_MYSQL_HOST_URL, PA_MYSQL_DATABASE_NAME)


class MySqlHelper:
    def __init__(self):
        self.mysql_conn:Union[None, MySQLConnection] = None
        if sys.platform == 'win32' or platform.node() == "wings":
            self.HOST_URL = MYSQL_HOST_URL
            self.PORT = MYSQL_PORT
            self.DATABASE_NAME = MYSQL_DATABASE_NAME
            self.USERNAME = MYSQL_USERNAME
            self.PASSWORD = MYSQL_PASSWORD
        else:
            self.HOST_URL = PA_MYSQL_HOST_URL
            self.PORT = PA_MYSQL_PORT
            self.DATABASE_NAME = PA_MYSQL_DATABASE_NAME
            self.USERNAME = PA_MYSQL_USERNAME
            self.PASSWORD = PA_MYSQL_PASSWORD

    def set_connection(self):
        # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        if self.mysql_conn and self.mysql_conn.is_connected():
            return
        else:
            self.mysql_conn = mysql.connector.connect(
                user=self.USERNAME,
                password=self.PASSWORD,
                host=self.HOST_URL,
                database=self.DATABASE_NAME,
                port=self.PORT
            )

    def close_connection(self):
        if self.mysql_conn and self.mysql_conn.is_connected():
            self.mysql_conn.close()

    def execute_query(self, sql_query: str,
                      variables: tuple = None,
                      keep_conn_alive:bool=False) -> bool:
        """Execute query and return False if Error"""
        self.set_connection()
        db_cursor = self.mysql_conn.cursor()
        try:
            db_cursor.execute(operation=sql_query,
                              params=variables)

        except ProgrammingError as ex:
            print(f'Sql Error: {ex.__class__.__name__}')
            print(ex)
            return False

        finally:
            db_cursor.close()
            self.mysql_conn.commit()
            if not keep_conn_alive:
                self.close_connection()
        return True

    def fetch_query(self, sql_query: str, variables: tuple = None) -> Union[list, None]:
        """Return SELECT query results as a list oof dicts"""

        self.set_connection()
        db_cursor = self.mysql_conn.cursor(dictionary=True)
        try:
            db_cursor.execute(operation=sql_query,
                              params=variables)
            results: list = db_cursor.fetchall()

        except ProgrammingError as ex:
            print(f'Sql Error: {ex.__class__.__name__}')
            print(ex)
            return None

        finally:
            db_cursor.close()
            self.close_connection()
        return results
