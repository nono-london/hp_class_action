import json
from datetime import datetime
from typing import Union

from bs4 import BeautifulSoup as bs
from bs4 import element
from lxml.html import Element
from hp_class_action.hinge_issue.scrap_data.web_requests import get_web_page
from hp_class_action.hp_database.hp_forum_issue import (execute_query,
                                                        fetch_query)

BASE_URL: str = "https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/8499984/rating-system/forum_topic_metoo/page/1#userlist"

hp_cookies = None



def get_post_ids(force_update: bool = False) -> Union[list, None]:
    if force_update:
        sql_str = """SELECT hp_post_id FROM forum_posts
                    ORDER BY post_datetime DESC
                   """
    else:
        sql_str = """SELECT hp_post_id FROM forum_posts
                    WHERE post_full IS NULL
                    ORDER BY post_datetime DESC

                """
    results = fetch_query(sql_query=sql_str)
    if results is None or len(results) == 0:
        return None
    results = [x['hp_post_id'] for x in results]
    return results


def get_full_post(page_source: str):
    bs_soup = bs(page_source, 'lxml')
    text_element = bs_soup.find(attrs={'id': 'bodyDisplay'})
    if text_element is not None:
        return text_element.text
    else:
        return None


def get_metoos(page_source: str) -> Union[None, list]:
    page_soup = bs(page_source, 'lxml')
    try:
        metoo_elements: [Element] = page_soup.find('div', attrs={'class': 'UserListBlock'}).find_all('div', attrs={
        'class': 'lia-user-attributes'})
        return metoo_elements
    except AttributeError as ex:
        return None
    except Exception as ex:
        print(f"get_metoos error:{ex.__class__.__name__}")
        exit(ex)



def extract_metoo_data(metoo_element: element) -> dict:
    href_element: Element = metoo_element.find('a',
                                               attrs={'class': "lia-link-navigation lia-page-link lia-user-name-link"})
    username = href_element.text
    href = href_element.get('href')
    user_id = href.split('/')[-1]
    post_date = metoo_element.find('span', attrs={'class': 'local-date'})
    post_date = datetime.strptime(post_date.text.replace('\u200e', ''), '%m-%d-%Y').strftime('%Y-%m-%d')

    user_attrs: dict = {'hp_user_id': user_id, 'username': username, 'post_datetime': post_date}
    print(user_attrs)
    return user_attrs


def update_mdb_with_me_too(metoo_json: str, post_id: int):
    """Update me_too column if a bigger size is found: ie more users complained"""
    sql_query = """UPDATE forum_posts
    SET me_too= CASE
                        WHEN me_too IS NULL OR JSON_STORAGE_SIZE(%s) > JSON_STORAGE_SIZE(me_too)
                        THEN %s
                        ELSE me_too
                    END

    WHERE hp_post_id=%s

    """
    execute_query(sql_query=sql_query, variables=(metoo_json, metoo_json, post_id))


def update_mdb_with_full_post(full_post: str, post_id: int):
    """"""
    sql_query = """
    UPDATE forum_posts
    SET post_full= CASE 
                        WHEN post_full is NULL OR LENGTH(%s) > LENGTH(post_full) 
                            THEN %s
                        ELSE post_full
                    END
    WHERE hp_post_id=%s

    """
    execute_query(sql_query=sql_query, variables=(full_post, full_post, post_id))


def update_summary_metoo(force_update: bool = False):
    """Update mdb with full summary and me too users' s names"""
    post_ids: list = get_post_ids(force_update=force_update)
    if post_ids is None or len(post_ids) == 0:
        print('No data to update')
        return
    max_metoo_pages: int = 100
    for post_id in post_ids:
        metoos: [dict] = []
        for i in range(1, max_metoo_pages):
            url_to_open: str = f"https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/{post_id}/rating-system/forum_topic_metoo/page/{i}#userlist"
            # url_to_open = "https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/8360940/rating-system/forum_topic_metoo/page/1#userlist"
            print(url_to_open)
            page_source = get_web_page(url_to_open=url_to_open,
                                       max_tries=10,
                                       timeout=10,
                                       check_response_url=True)
            if page_source is None:
                break

            if i == 1:
                full_post: str = get_full_post(page_source=page_source)
                update_mdb_with_full_post(full_post=full_post,
                                          post_id=post_id)

            metoo_elements = get_metoos(page_source=page_source)
            if metoo_elements is None or len(metoo_elements) == 0:
                break
            for metoo_element in metoo_elements:
                user_metoos = extract_metoo_data(metoo_element=metoo_element)
                if len(user_metoos) == 0:
                    break
                metoos.append(user_metoos)
        if len(metoos) > 0:
            update_mdb_with_me_too(metoo_json=json.dumps(metoos),
                                   post_id=post_id)


if __name__ == '__main__':
    update_summary_metoo(force_update=True, )
