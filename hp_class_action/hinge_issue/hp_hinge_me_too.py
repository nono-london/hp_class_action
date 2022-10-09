from typing import Union
import json
from bs4 import BeautifulSoup as bs
from bs4 import element
from lxml.html import Element
from datetime import datetime
from hp_class_action.hinge_issue.hp_hinge_broken import get_web_page
from hp_class_action.hp_database.hp_forum_issue import execute_query, fetch_query


BASE_URL: str = "https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/8499984/rating-system/forum_topic_metoo/page/1#userlist"


def get_post_ids() -> Union[list, None]:
    sql_str = """SELECT hp_post_id FROM hp_forum_issues
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
    # xpath_value = "// div[@class='lia-user-name']"
    # lxml_str = fromstring(page_source)
    # metoo_elements: [Element] = lxml_str.xpath(xpath_value)
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
    """"""
    sql_query = """UPDATE hp_forum_issues
    SET me_too=%s
    WHERE hp_post_id=%s
    """
    execute_query(sql_query=sql_query, variables=(metoo_json, post_id))


def update_mdb_with_full_post(full_post: str, post_id: int):
    """"""
    sql_query = """UPDATE hp_forum_issues
    SET post_full=%s
    WHERE hp_post_id=%s
    
    """
    execute_query(sql_query=sql_query, variables=(full_post, post_id))


def update_summary_metoo():
    """Update mdb with full summary and me too users' s names"""
    post_ids: list = get_post_ids()
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
    update_summary_metoo()
    exit(0)
    print(get_post_ids())
