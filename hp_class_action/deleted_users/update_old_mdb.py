from bs4 import BeautifulSoup as bs

from hp_class_action.hinge_issue.scrap_data.scrap_search_query import UserPost
from hp_class_action.hinge_issue.scrap_data.web_requests import get_web_page
from hp_class_action.hp_database.hp_forum_issue_bis import (fetch_query)


def compare_users_with_old_data():
    """compare usrnames between table: hp_forum_issues(old) and hp_posts(new)"""
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


def update_old_data():
    """compare usrnames between table: hp_forum_issues(old) and hp_posts(new)"""
    sql_query_old_usernames = """
        SELECT username, post_url
        FROM hp_trial.hp_forum_issues
        ORDER BY username 
        """
    old_usernames = fetch_query(sql_query=sql_query_old_usernames)

    print(f'Old usernames size: {len(old_usernames)}')

    # get url from old mdb

    for user_post in old_usernames:
        post_url = user_post['post_url']
        user_post_element = get_web_page(url_to_open=post_url,
                                         max_tries=10,
                                         timeout=10,
                                         check_response_url=False)

        web_soup = bs(user_post_element, 'lxml')
        web_soup = web_soup.find('div', attrs={"data-lia-message-uid": True})

        user_post = UserPost(user_post_element=web_soup)
        user_post.get_info_from_tag()
        print('-' * 100)
        print(user_post)


if __name__ == '__main__':
    update_old_data()
    exit(0)
    compare_users_with_old_data()
