import mysql.connector
from mysql.connector.errors import (ProgrammingError, IntegrityError)
from typing import Union
from hp_class_action.app_config_secret import (MYSQL_USERNAME, MYSQL_DATABASE_NAME,
                                               MYSQL_HOST_URL, MYSQL_PORT,
                                               MYSQL_PASSWORD, PA_MYSQL_PORT,
                                               PA_MYSQL_USERNAME, PA_MYSQL_PASSWORD,
                                               PA_MYSQL_HOST_URL, PA_MYSQL_DATABASE_NAME)

import sys

if sys.platform == 'win32':
    HOST_URL = MYSQL_HOST_URL
    PORT = MYSQL_PORT
    DATABASE_NAME = MYSQL_DATABASE_NAME
    USERNAME = MYSQL_USERNAME
    PASSWORD = MYSQL_PASSWORD
else:
    HOST_URL = PA_MYSQL_HOST_URL
    PORT = PA_MYSQL_PORT
    DATABASE_NAME = PA_MYSQL_DATABASE_NAME
    USERNAME = PA_MYSQL_USERNAME
    PASSWORD = PA_MYSQL_PASSWORD

_TABLE_NAME: str = "hp_forum_issues"


def create_table():
    sql_query: str = f"""
            CREATE TABLE IF NOT EXISTS {_TABLE_NAME} 
                (
                post_id  INT AUTO_INCREMENT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                hp_post_id  INT NOT NULL,
                post_datetime TIMESTAMP NOT NULL,
                username VARCHAR(75) NOT NULL,
                post_url TEXT NOT NULL,
                post_tags JSON NOT NULL,
                post_summary TEXT NOT NULL,
                post_full TEXT NULL,
                me_too JSON
                );
           
            """

    execute_query(sql_query=sql_query)

    sql_query = f"""            
                CREATE UNIQUE INDEX hp_id_unique
                ON {_TABLE_NAME}(hp_post_id);
                """
    execute_query(sql_query=sql_query)


def get_connection():
    # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    db_conn = mysql.connector.connect(
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST_URL,
        database=DATABASE_NAME,
        port=MYSQL_PORT
    )
    print(f'Connected to MySQl: {db_conn.is_connected()}')
    return db_conn


def execute_query(sql_query: str, variables: tuple = None) -> bool:
    """Execute query and return False if Error"""

    db_conn = get_connection()
    db_cursor = db_conn.cursor()
    try:
        result = db_cursor.execute(operation=sql_query,
                                   params=variables)

        print(f'Execute query result: {_TABLE_NAME}: {result}')
    except ProgrammingError as ex:
        print(f'Sql Error: {ex.__class__.__name__}')
        print(ex)
        return False
    except IntegrityError as ex:
        print(f'Integrity Error (Duplicate key?): {ex.__class__.__name__}')
        print(ex)
        return False
    finally:
        db_cursor.close()
        db_conn.commit()
        db_conn.close()
    return True


def fetch_query(sql_query: str, variables: tuple = None) -> Union[list, None]:
    """Return SELECT query results as a list oof dicts"""

    db_conn = get_connection()
    db_cursor = db_conn.cursor(dictionary=True)
    try:
        db_cursor.execute(operation=sql_query,
                          params=variables)
        results: list = db_cursor.fetchall()
        print(db_cursor.warnings)
        print(db_cursor.get_attributes())
    except ProgrammingError as ex:
        print(f'Sql Error: {ex.__class__.__name__}')
        print(ex)
        return None
    except IntegrityError as ex:
        print(f'Integrity Error (Duplicate key?): {ex.__class__.__name__}')
        print(ex)
        return None
    finally:
        db_cursor.close()
        db_conn.close()
    return results


if __name__ == '__main__':
    sql_str = """SELECT * FROM hp_forum_issues LIMIT 2"""
    print(fetch_query(sql_query=sql_str))
    exit(0)
    create_table()
