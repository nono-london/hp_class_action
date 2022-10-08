import mysql.connector
from mysql.connector.errors import (ProgrammingError, IntegrityError)

from hp_class_action.app_config_secret import (MYSQL_USER_NAME, MYSQL_DATABASE_NAME,
                                               MYSQL_URL, MYSQL_PORT,
                                               MYSQL_PASSWORD)

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
        user=MYSQL_USER_NAME,
        password=MYSQL_PASSWORD,
        host=MYSQL_URL,
        database=MYSQL_DATABASE_NAME,
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


if __name__ == '__main__':
    create_table()
