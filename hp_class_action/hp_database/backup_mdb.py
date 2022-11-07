from datetime import datetime
from pathlib import Path
from typing import Union
from math import isnan
import pandas as pd

from hp_class_action.app_config import get_project_download_path
from hp_class_action.hp_database.mdb_handlers import (fetch_query, execute_query)
pd.set_option('display.max_columns', None)

_MDB_BACKUP_FULL_PATH: Path = Path(get_project_download_path(),
                                   f"mdb_backup.csv")


def backup_mdb_to_csv() -> datetime:
    """Save a copy of all fields and tables from mdb
        Returns datetime at which the backup was last modified
    """
    sql_query: str = """
                    SELECT a.*, b.*
                    FROM hp_users a LEFT JOIN forum_posts b
                        ON a.user_id=b.user_id
                    ORDER BY a.username, b.post_datetime DESC
    """
    results = fetch_query(sql_query=sql_query)
    result_df = pd.DataFrame(results)
    result_df.to_csv(path_or_buf=_MDB_BACKUP_FULL_PATH,
                     sep=',',
                     index=False)
    creation_date = Path(_MDB_BACKUP_FULL_PATH).stat().st_mtime
    creation_date = datetime.fromtimestamp(creation_date)
    return creation_date


def read_csv_backup() -> Union[pd.DataFrame, None]:
    if not _MDB_BACKUP_FULL_PATH.exists():
        print(f'Database backup file not found:\n'
              f'{_MDB_BACKUP_FULL_PATH}')
        return None
    result_df = pd.read_csv(filepath_or_buffer=_MDB_BACKUP_FULL_PATH,
                            sep=',',
                            date_parser=["created_at", "post_datetime"])

    return result_df


def upload_users_from_csv():
    """Upload all user name from the locally saved csv """
    csv_df = read_csv_backup()
    sql_query = """
    INSERT IGNORE INTO `hp_trial`.`hp_users`
        (
        `hp_user_id`,
        `username`,
        `user_profile_url`,
        `user_blocked`
        )
    VALUES(%s, %s, %s, %s)
    """
    for index, row in csv_df.iterrows():
        result = execute_query(sql_query, variables=(
            row['hp_user_id'], row['username'],
            row['user_profile_url'], row['user_blocked']))
        print(result,end=', ')
    print()


def upload_posts_from_csv():
    """Upload all posts from the locally saved csv """
    csv_df = read_csv_backup()
    sql_query = """
                INSERT IGNORE INTO `hp_trial`.`forum_posts`
                (`user_id`,
                `hp_post_id`,
                `post_datetime`,
                `post_url`,
                `post_summary`,
                `post_tags`,
                `me_too`)
                VALUES
                (
                    (SELECT user_id FROM hp_users WHERE hp_user_id = %s),
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s              
                )
    """
    for index, row in csv_df.iterrows():
        post_url = None if (~isinstance(
            row['post_url'], str)) else row['post_url']
        post_summary = None if (~isinstance(
            row['post_summary'], str)) else row['post_summary']
        post_tags = None if (~isinstance(
            row['post_tags'], str)) else row['post_tags']
        me_too = None if (~isinstance(
            row['me_too'], str)) else row['me_too']
        sql_vars = (
            row['hp_user_id'],
            row['hp_post_id'], row['post_datetime'], post_url,
            post_summary, post_tags, me_too
        )
        result = execute_query(sql_query, variables=sql_vars  )
        if result is False:
            print([type(field) for field in sql_vars])
            exit(f'field values are\n: {sql_vars}')
        print(result, end=', ')
    print()



if __name__ == '__main__':
    upload_posts_from_csv()
    exit(0)
    print(read_csv_backup())
    exit(0)
    print(backup_mdb_to_csv())
    exit(0)