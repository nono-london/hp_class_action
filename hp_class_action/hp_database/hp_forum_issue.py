import sys

import mysql.connector
from mysql.connector.errors import (ProgrammingError, IntegrityError)

from hp_class_action.app_config_secret import (MYSQL_USERNAME, MYSQL_DATABASE_NAME,
                                               MYSQL_HOST_URL, MYSQL_PORT,
                                               MYSQL_PASSWORD,
                                               PA_MYSQL_USERNAME, PA_MYSQL_PASSWORD, PA_MYSQL_PORT,
                                               PA_MYSQL_HOST_URL, PA_MYSQL_DATABASE_NAME)

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
                post_full TEXT NULL
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
        user=USERNAME,
        password=PASSWORD,
        host=HOST_URL,
        database=DATABASE_NAME,
        port=PORT
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


if __name__ == '__main__':
    create_table()
