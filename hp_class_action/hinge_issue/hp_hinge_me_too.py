import json
from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup as bs
from bs4 import element
from lxml.html import Element
from requests.exceptions import ConnectionError

from hp_class_action.hp_database.hp_forum_issue import execute_query, fetch_query

BASE_URL: str = "https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/8499984/rating-system/forum_topic_metoo/page/1#userlist"

hp_cookies = None


def get_web_page(url_to_open: str, max_tries: int = 10) -> Union[None, str]:
    global hp_cookies
    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    page_content: Union[None, str] = None
    max_tries: int = max_tries
    while max_tries > 0:
        try:
            response = requests.get(url=url_to_open, headers=headers, timeout=10, cookies=hp_cookies)
            if response.url != url_to_open:
                return None
            page_content = response.text
            hp_cookies = response.cookies
            break
        except ConnectionError as ex:
            print(f'Error while connecting:\n{ex}')
            max_tries -= 1

    return page_content


def get_post_ids(force_update: bool = False) -> Union[list, None]:
    if force_update:
        sql_str = """SELECT hp_post_id FROM hp_forum_issues
                    ORDER BY post_datetime DESC
                   """
    else:
        sql_str = """SELECT hp_post_id FROM hp_forum_issues
                    WHERE post_full IS NULL
                    ORDER BY post_datetime DESC

                """
    results = fetch_query(sql_query=sql_str)
    if results is None or len(results) == 0:
        return None
    results = [x['hp_post_id'] for x in results]
    return results


def get_full_post(page_source: str):
    # xpath_value = "// div[@id='bodyDisplay']/*[@class='lia-message-body-content']/p"
    # lxml_str = fromstring(page_source)
    # text_elements: [Element] = lxml_str.xpath(xpath_value)
    bs_soup = bs(page_source, 'lxml')
    text_elements = bs_soup.find(attrs={'id': 'bodyDisplay'}).find(
        attrs={'class': 'lia-message-body-content'}).find_all('p')

    text_elements = [x.text for x in text_elements]
    result_text = ' '.join(text_elements)
    print(result_text)
    return result_text


def get_metoos(page_source: str) -> Union[None, list]:
    page_soup = bs(page_source, 'lxml')
    metoo_elements: [Element] = page_soup.find('div', attrs={'class': 'UserListBlock'}).find_all('div', attrs={
        'class': 'lia-user-attributes'})

    return metoo_elements


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
    sql_query = """UPDATE hp_forum_issues
    SET me_too= CASE
                        WHEN JSON_STORAGE_SIZE(%s) > JSON_STORAGE_SIZE(me_too)
                        THEN %s
                        ELSE me_too
                    END
                
    WHERE hp_post_id=%s
    
    """
    execute_query(sql_query=sql_query, variables=(metoo_json, metoo_json, post_id))


def update_mdb_with_full_post(full_post: str, post_id: int):
    """"""
    sql_query = """
    UPDATE hp_forum_issues
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
    if (post_ids is None or len(post_ids) == 0):
        exit('No data to update')
    max_metoo_pages: int = 100
    for post_id in post_ids:
        metoos: [dict] = []
        for i in range(1, max_metoo_pages):
            url_to_open: str = f"https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/{post_id}/rating-system/forum_topic_metoo/page/{i}#userlist"
            # url_to_open = "https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/8360940/rating-system/forum_topic_metoo/page/1#userlist"
            print(url_to_open)
            page_source = get_web_page(url_to_open=url_to_open)
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
