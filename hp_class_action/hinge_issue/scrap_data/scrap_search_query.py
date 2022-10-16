from urllib.parse import urljoin
import json
import pandas as pd
from bs4 import BeautifulSoup as bs
from bs4.element import Tag

from hp_class_action.hinge_issue.scrap_data.web_requests import get_web_page
from hp_class_action.hp_database.hp_forum_issue_bis import (execute_query,
                                                            fetch_query)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from datetime import datetime, timezone
from typing import Union


def get_user_posts(page_source: str) -> list:
    web_soup = bs(page_source, 'lxml')
    user_posts_elements: list = web_soup.find_all('div', attrs={"data-lia-message-uid": True})

    return user_posts_elements


class UserPost:
    def __init__(self, user_post_element: Tag):
        self.base_url: str = 'https://h30434.www3.hp.com/t5/forums/searchpage/'
        self.user_post_element: Tag = user_post_element

        # hp_users
        self.hp_user_id: Union[int, None] = None
        self.username: Union[str, None] = None
        self.user_profile_url: Union[str, None] = None

        # hp forums
        self.post_datetime: Union[datetime, None] = None
        self.post_id: Union[int, None] = None
        self.post_url: Union[str, None] = None

        self.post_summary: Union[str, None] = None
        self.post_full: Union[str, None] = None
        self.post_tags: list = []

    @staticmethod
    def _text_cleaner(bs4_text: str):
        return bs4_text.replace('\u200e', '').replace('\n', '').replace('\t', '').strip()

    def __str__(self):

        return_str =f"username:{self.username}, hp_user_id:{self.hp_user_id}: {self.post_tags}\n{self.post_full}"
        return return_str
    def _get_user_id_name_profile_url(self):
        username_elements = self.user_post_element.select('span[class*="UserName"]')
        self.username = self._text_cleaner(username_elements[0].text)
        href_element = username_elements[0].find('a', attrs={'href': True})
        self.user_profile_url = href_element.get('href')
        self.hp_user_id = int(self.user_profile_url.split('/')[-1])

    def _get_post_id_url(self):
        self.post_id = int(self.user_post_element.get("data-lia-message-uid"))
        post_url = self.user_post_element.find('a', attrs={
            'class': "page-link lia-link-navigation lia-custom-event"})
        if post_url is not None:
            self.post_url = post_url.get('href')
            self.post_url = urljoin(self.base_url, self.post_url)


    def _get_post_datetime(self):
        posted_on_element = self.user_post_element.find('span', attrs={'class': 'DateTime'})
        posted_on_str: str = posted_on_element.text.strip().replace("\n", " ").replace("\t", " ").strip()
        posted_on_str = posted_on_str.split(" ")[0].strip() + " " + posted_on_str.split(" ")[-2].strip() + " " + \
                        posted_on_str.split(" ")[-1].strip()
        posted_on_str = posted_on_str.replace('\u200e', '')
        posted_on: datetime = datetime.strptime(posted_on_str, "%m-%d-%Y %I:%M %p")
        local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
        self.post_datetime = posted_on.replace(tzinfo=local_timezone)

    def _get_post_summary(self):
        post_summary_element = self.user_post_element.find('div', attrs={'class': 'lia-truncated-body-container'})
        if post_summary_element is not None:
            self.post_summary = self._text_cleaner(post_summary_element.text)

    def _get_full_post(self):
        full_post_element = self.user_post_element.find('div', attrs={'class': "lia-message-body-content"})
        if full_post_element is not None:
            self.post_full = self._text_cleaner(full_post_element.text)



    def _get_post_tags(self):
        tag_elements = self.user_post_element.select('div[id*="tagsList"][class*="TagList"]')
        if len(tag_elements)==0:
            self.post_tags=None
            return
        tag_elements = tag_elements[0].find('ul').find_all('li')

        for tag_element in tag_elements:
            if self._text_cleaner(tag_element.text) != "Tags:":
                self.post_tags.append(self._text_cleaner(tag_element.text))

    def _upload_to_mdb(self):
        # Insert user
        sql_query = """
                INSERT IGNORE INTO hp_users(
                        hp_user_id, username, user_profile_url)
                    VALUES (%s, %s, %s)
            """
        sql_variables = (self.hp_user_id, self.username, self.user_profile_url)
        execute_query(sql_query=sql_query,
                      variables=sql_variables)

        # select newly inserted user_id
        sql_query = """
                    SELECT user_id
                    FROM hp_users
                    WHERE hp_user_id=%s
        """
        sql_variables = (self.hp_user_id,)
        hp_user_id = fetch_query(sql_query=sql_query,
                                 variables=sql_variables)

        user_id = hp_user_id[0]['user_id']
        # Insert data in forum table
        sql_query = """
                    INSERT IGNORE INTO forum_posts(
                                    user_id, hp_post_id, post_datetime, post_url, post_summary,
                                    post_full,
                                    post_tags
                                    )
                                VALUES(
                                        %s, %s, %s, %s, %s, 
                                        %s, 
                                        %s 
                                        )
                        ON DUPLICATE KEY
                        UPDATE post_full=VALUES(post_full)

                    
        """
        json_post_tags = json.dumps(self.post_tags)
        sql_variables = (user_id, self.hp_user_id, self.post_datetime, self.post_url, self.post_summary,
                         self.post_full,
                         json_post_tags)
        execute_query(sql_query=sql_query,
                      variables=sql_variables)






    def get_info_from_tag(self):
        self._get_post_datetime()
        self._get_user_id_name_profile_url()
        self._get_post_id_url()
        self._get_post_summary()
        self._get_full_post()
        self._get_post_tags()

        self._upload_to_mdb()



def webscrap_query_search():
    results_per_page: int = 50
    offset_pages: int = int(2000 / 50) + 10

    # https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&page=4&sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size=50
    for i in range(1, offset_pages):
        print(f'Getting page: {i}')
        if i == 1:
            base_url = f"https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&" \
                       f"sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size={results_per_page}"
        else:
            base_url = f"""https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&page={i}&
            sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size={results_per_page}"""
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
            print("-"*100)
            print(user_post)


if __name__ == '__main__':
    webscrap_query_search()
