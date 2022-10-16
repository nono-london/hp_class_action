import pandas as pd
from bs4 import BeautifulSoup as bs
from bs4.element import Tag

from hp_class_action.hinge_issue.scrap_data.web_requests import get_web_page
from hp_class_action.hp_user_class import UserPost

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_user_posts(page_source: str) -> list:
    web_soup = bs(page_source, 'lxml')
    user_posts_elements: list = web_soup.find_all('div', attrs={"data-lia-message-uid": True})

    return user_posts_elements


def webscrap_query_search(max_pages: int = 50):
    # number of displayed user posts per web page
    results_per_page: int = 50
    # number of pages to query (there is a maximum of 2000 results per search)
    offset_pages: int = min(int(2000 / results_per_page) + 10, max_pages)

    # https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&page=4&sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size=50
    for i in range(1, offset_pages):
        print(f'Getting page: {i}')
        if i == 1:
            base_url = f"https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&" \
                       f"sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size={results_per_page}"
            # base_url = f"https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&" \
            #            f"sort_by=score&collapse_discussion=true&search_type=thread&search_page_size=50"
        else:
            base_url = f"""https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&page={i}&
            sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size={results_per_page}"""
            # base_url = f"https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&page={i}&" \
            #            f"sort_by=score&collapse_discussion=true&search_type=thread&search_page_size={results_per_page}"
        page_source = get_web_page(url_to_open=base_url,
                                   max_tries=10,
                                   timeout=10,
                                   check_response_url=False)
        if page_source is None:
            print(f'No data found for page: {i}\nURL:{base_url}')
            break
        user_post_tags: [Tag] = get_user_posts(page_source=page_source)
        for user_post_tag in user_post_tags:
            user_post = UserPost(user_post_element=user_post_tag)
            user_post.get_info_from_tag()
            print("-" * 100)
            print(user_post)


if __name__ == '__main__':
    webscrap_query_search(max_pages=100)
