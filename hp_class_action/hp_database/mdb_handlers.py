import platform
import sys
from typing import Union

import mysql.connector
from mysql.connector.errors import (ProgrammingError)

from hp_class_action.app_config_secret import (MYSQL_USERNAME, MYSQL_DATABASE_NAME,
                                               MYSQL_HOST_URL, MYSQL_PORT,
                                               MYSQL_PASSWORD, PA_MYSQL_PORT,
                                               PA_MYSQL_USERNAME, PA_MYSQL_PASSWORD,
                                               PA_MYSQL_HOST_URL, PA_MYSQL_DATABASE_NAME)

if sys.platform == 'win32' or platform.node() == "wings":
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

_TABLE_HP_USERS: str = "hp_users"
_TABLE_REPORTED_ISSUES: str = "forum_posts"
_TABLE_WEBSITE_VISITORS_INFO: str = "website_visitors_info"


def create_table_hp_users():
    sql_query: str = f"""
            CREATE TABLE IF NOT EXISTS {_TABLE_HP_USERS} 
                (
                user_id  INT AUTO_INCREMENT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

                hp_user_id  BIGINT NOT NULL,
                username VARCHAR(50) NOT NULL,
                user_profile_url TEXT NOT NULL,
                user_blocked BOOLEAN NOT NULL DEFAULT 0,
                
                
                UNIQUE KEY hp_user_id_unique (hp_user_id)
                )
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                ;

            """

    execute_query(sql_query=sql_query)


def create_table_reported_issues():
    sql_query: str = f"""
            CREATE TABLE IF NOT EXISTS {_TABLE_REPORTED_ISSUES} 
                (
                post_id  INT AUTO_INCREMENT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                
                user_id INT NOT NULL,

                hp_post_id  BIGINT NOT NULL,
                post_datetime TIMESTAMP NOT NULL,
                post_url TEXT NOT NULL,
                post_summary TEXT NOT NULL,
                post_tags JSON NOT NULL,
                
                post_full TEXT NULL,
                me_too JSON,
                
                KEY `fk_user_id_idx` (`user_id`),
                CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `hp_users` (`user_id`)
                
                );

            """

    execute_query(sql_query=sql_query)

    sql_query = f"""            
                CREATE UNIQUE INDEX hp_id_unique
                ON {_TABLE_REPORTED_ISSUES}(hp_post_id);
                """
    execute_query(sql_query=sql_query)


def create_table_website_visitors_ip():
    sql_query: str = f"""
            CREATE TABLE IF NOT EXISTS {_TABLE_WEBSITE_VISITORS_INFO} 
                (
                ip_id  INT AUTO_INCREMENT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

                visit_datetime TIMESTAMP NOT NULL,
                visit_url VARCHAR(150) NOT NULL,
                
                ip_address  VARCHAR(50) NOT NULL,
                city VARCHAR(50),
                region VARCHAR(50),
                country_code VARCHAR(5),
                country_code_iso3 VARCHAR(3),
                country_name VARCHAR(75),
                coordinate POINT,
                timezone VARCHAR(50),
                utc_offset VARCHAR(5),
                org VARCHAR(50),
                user_agent TEXT,
                
                UNIQUE KEY ip_address_visit_datetime (ip_address, visit_datetime)
                )
            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                ;

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

    return db_conn


def execute_query(sql_query: str, variables: tuple = None) -> bool:
    """Execute query and return False if Error"""

    db_conn = get_connection()
    db_cursor = db_conn.cursor()
    try:
        db_cursor.execute(operation=sql_query,
                          params=variables)

    except ProgrammingError as ex:
        print(f'Sql Error: {ex.__class__.__name__}')
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

    except ProgrammingError as ex:
        print(f'Sql Error: {ex.__class__.__name__}')
        print(ex)
        return None

    finally:
        db_cursor.close()
        db_conn.close()
    return results


if __name__ == '__main__':
    create_table_hp_users()
    create_table_reported_issues()
    create_table_website_visitors_ip()
