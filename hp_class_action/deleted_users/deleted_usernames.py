from pathlib import Path
from typing import Union

import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from hp_class_action.app_config import get_project_download_path
from hp_class_action.hinge_issue.scrap_data.web_requests import get_web_page
from hp_class_action.hp_database.mdb_handlers import (fetch_query)


def get_user_details_of_posters() -> Union[pd.DataFrame, None]:
    """Return list of users that have posted their claim on the forum"""
    sql_query = """
            SELECT * 
            FROM hp_trial.hp_users
            ORDER BY created_at
            """
    results = fetch_query(sql_query=sql_query)
    if results is None:
        return None
    result_df = pd.DataFrame(results)
    return result_df


def check_user_still_exists():
    mdb_user_df = get_user_details_of_posters()
    deleted_users: list = []

    # check user profile url still exist
    print('Checking deleted users:')
    for index, row in tqdm(mdb_user_df.iterrows(), total=mdb_user_df.shape[0]):
        page_source = get_web_page(url_to_open=row['user_profile_url'],
                                   check_response_url=False)
        web_soup = bs(page_source, 'lxml')
        username_element = web_soup.find('div', attrs={'class': 'lia-user-name'})
        if username_element is None:
            deleted_users.append(row)

    print(f'Found {len(deleted_users)} deleted users.')
    if len(deleted_users) == 0:
        return
    deleted_user_df = pd.DataFrame(deleted_users)
    print(f"Found {len(deleted_users)} deleted users:\n"
          f"{deleted_user_df}")
    deleted_user_df.to_csv(path_or_buf=Path(get_project_download_path(),
                                            'deleted_users.csv', ),
                           index=False, sep=','
                           )


if __name__ == '__main__':
    check_user_still_exists()
    exit(0)
    print(get_user_details_of_posters())
