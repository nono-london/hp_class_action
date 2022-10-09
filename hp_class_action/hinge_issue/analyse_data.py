import json
from pathlib import Path

import pandas as pd

from hp_class_action.app_config import get_project_download_path
from hp_class_action.hp_database.hp_forum_issue import (fetch_query)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
LOCAL_FILE_NAME: str = str(Path().joinpath(get_project_download_path(), 'hp_hinges_issues.csv'))


def get_mdb_dataset() -> list:
    """Get relevant data from mdb"""
    sql_query: str = """
            SELECT hp_post_id, post_datetime, username, me_too
            FROM hp_forum_issues
            ORDER BY post_datetime DESC
            
        """
    results: list = fetch_query(sql_query=sql_query)
    for row_dict in results:
        if row_dict['me_too'] is not None:
            row_dict['me_too'] = json.loads(row_dict['me_too'])
    return results


def clean_metoo_user_details(me_to_user_details: list) -> pd.DataFrame:
    """Select the oldest time a user has claimed on another chat that he had the same issue"""
    user_details: [] = []
    for row_dicts in me_to_user_details:
        for row_dict in row_dicts:
            user_details.append(row_dict)

    user_detail_df: pd.DataFrame = pd.DataFrame(user_details)
    user_detail_df.sort_values(by=['username', 'post_datetime'],
                               ascending=[True, False],
                               inplace=True)
    user_detail_df.drop_duplicates(subset=['username'],
                                   keep='last',
                                   inplace=True,
                                   ignore_index=True)
    return user_detail_df


def all_claims():
    """Returns a df with claims from post id and from people who had same issue"""
    mdb_results = get_mdb_dataset()
    mdb_df: pd.DataFrame = pd.DataFrame(mdb_results)
    mdb_usernames: list = list(set([x['username'] for x in mdb_results]))
    # create list of me_too users
    print('#' * 100)
    print(f'mdb_usernames:{mdb_usernames}')
    metoo_user_details: [dict] = [x['me_too'] for x in mdb_results if x['me_too'] is not None]
    print('#' * 100)
    print(f'metoo_user_details:\n{metoo_user_details}')
    meeto_detail_df = clean_metoo_user_details(me_to_user_details=metoo_user_details)
    result_df = pd.concat([meeto_detail_df[['username', 'post_datetime']], mdb_df[['username', 'post_datetime']]])
    clean_df: pd.DataFrame = result_df.drop_duplicates(subset=['username'],
                                                       ignore_index=True,
                                                       inplace=False)

    print(f'len mdb_df:{len(mdb_df)}')
    print(f'len meeto_detail_df:{len(meeto_detail_df)}')
    print(f'len result_df:{len(result_df)}')
    print(f'len clean_df:{len(clean_df)}')


if __name__ == '__main__':
    all_claims()
