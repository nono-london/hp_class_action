from datetime import datetime
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup as bs

from hp_class_action.app_config import get_project_download_path
from hp_class_action.hinge_issue.scrap_data.scrap_search_query import UserPost
from hp_class_action.hinge_issue.scrap_data.web_requests import get_web_page
from hp_class_action.hp_database.hp_forum_issue_bis import (fetch_query)


def compare_users_with_old_data():
    """compare usernames between table: hp_forum_issues(old) and hp_posts(new)"""
    sql_query_old_usernames = """
        SELECT distinct(username)
        FROM hp_trial.hp_forum_issues
        ORDER BY username 
        """
    old_usernames = fetch_query(sql_query=sql_query_old_usernames)
    old_usernames = [username['username'] for username in old_usernames]

    sql_query_new_usernames = """
            SELECT distinct(username)
            FROM hp_trial.hp_users
            ORDER BY username 
            """
    new_usernames = fetch_query(sql_query=sql_query_new_usernames)
    new_usernames = [username['username'] for username in new_usernames]

    print(f'Old usernames size: {len(old_usernames)}')
    print(f'New usernames size: {len(new_usernames)}')

    deleted_usernames = list(set(old_usernames) - set(new_usernames))
    print(f'Deleted usernames size: {len(deleted_usernames)}')

    # get url from old mdb
    sql_query = """SELECT username, post_url FROM hp_forum_issues WHERE username=%s"""
    deleted_message_with_urls = []
    for deleted_username in deleted_usernames:
        deleted_message_with_urls.append(fetch_query(sql_query=sql_query,
                                                     variables=(deleted_username,))
                                         )
    print(deleted_message_with_urls)
    exit(0)
    for user_post in deleted_message_with_urls:
        post_url = user_post[0]['post_url']
        user_post_element = get_web_page(url_to_open=post_url,
                                         max_tries=10,
                                         timeout=10,
                                         check_response_url=False)
        print(user_post_element)
        web_soup = bs(user_post_element, 'lxml')
        web_soup = web_soup.find('div', attrs={"data-lia-message-uid": True})

        user_post = UserPost(user_post_element=web_soup)
        user_post.get_info_from_tag()

        print(user_post_element)


def upload_old_mdb_posts_to_new_mdb():
    """get all post urls from old mdb and retrieve data from web
        and upload it to new mdb
        if post has been deleted, related usernames are stored in csv file
    """
    missing_posts_sql = """
        SELECT a.hp_post_id,a.username, a.post_url
        FROM hp_trial.hp_forum_issues a LEFT JOIN forum_posts b 
            ON a.hp_post_id=b.hp_post_id
            WHERE b.hp_post_id IS NULL
        """
    missing_posts = fetch_query(sql_query=missing_posts_sql)

    print(f'Old usernames size: {len(missing_posts)}')

    # get url from old mdb
    deleted_users = []
    for user_post in missing_posts:
        post_url = user_post['post_url']
        user_post_element = get_web_page(url_to_open=post_url,
                                         max_tries=10,
                                         timeout=10,
                                         check_response_url=False)

        web_soup = bs(user_post_element, 'lxml')
        web_soup = web_soup.find('div', attrs={"data-lia-message-uid": True})
        if web_soup is None:
            print(f'user {user_post["username"]} has been deleted')
            deleted_users.append({'username': user_post["username"]})

        user_post = UserPost(user_post_element=web_soup)
        user_post.get_info_from_tag()
        print('-' * 100)
        print(user_post)

    if len(deleted_users) == 0:
        return
    deleted_users_df = pd.DataFrame(deleted_users)
    deleted_users_df['update_datetime'] = datetime.utcnow()

    path_to_save = Path(get_project_download_path(),
                        'not_found_post_users_old_mdb.csv')
    deleted_users_df.to_csv(path_or_buf=path_to_save,
                            sep=',',
                            index=False)


if __name__ == '__main__':
    upload_old_mdb_posts_to_new_mdb()
    exit(0)
    compare_users_with_old_data()
    exit(0)
