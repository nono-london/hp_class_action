from datetime import datetime, timezone
from random import randint
from time import sleep
from typing import Union
from urllib.parse import urljoin

import pandas as pd
from selenium_helpers.chrome_libs.new_libs.chrome_class import ChromeHandler, By
from lxml.html import fromstring, Element
from requests.exceptions import ConnectionError

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


hp_cookies = None




def get_page_rows(page_source: str) -> [Element]:
    xpath_value = "// div[@class='search-result-count']"
    # lxml examples
    lxml_str = fromstring(page_source)
    results_number: int = int(lxml_str.xpath(xpath_value)[0].text.strip().split(" ")[0].replace(",", "").strip())
    xpath_value = "// div[@data-lia-message-uid]"
    page_rows: [Element] = lxml_str.xpath(xpath_value)
    print(f'Found {len(page_rows)} posts.')
    return page_rows


def get_post_url(page_row: Element, message_id: int) -> str:
    """Return the url of the post"""
    xpath_value = f"// div[@data-lia-message-uid={message_id}] //*[@class='page-link lia-link-navigation lia-custom-event']"
    href_element: Element = page_row.xpath(xpath_value)[0]
    href = href_element.get('href')
    href = urljoin(base=base_url, url=href)
    return href


def get_message_id(page_row: Element) -> int:
    """Return the message id"""
    msg_id: int = page_row.get('data-lia-message-uid')
    return msg_id


def get_username(page_row: Element, message_id: int) -> str:
    """Return the username attached to the post"""
    xpath_value = f"// div[@data-lia-message-uid={message_id}] // span[contains(@class,'UserName')]"
    username_element: Element = page_row.xpath(xpath_value)[0]
    username = username_element.text_content().strip()
    return username


def get_posted_datetime(page_row: Element, message_id: int) -> datetime:
    """Return the datetime at which the post was posted"""
    xpath_value = f"// div[@data-lia-message-uid={message_id}] //  span[@class='DateTime']"
    posted_on_element: Element = page_row.xpath(xpath_value)[0]
    posted_on_str: str = posted_on_element.text_content().strip().replace("\n", " ").replace("\t", " ").strip()
    posted_on_str = posted_on_str.split(" ")[0].strip() + " " + posted_on_str.split(" ")[-2].strip() + " " + \
                    posted_on_str.split(" ")[-1].strip()
    posted_on_str = posted_on_str.replace('\u200e', '')
    posted_on: datetime = datetime.strptime(posted_on_str, "%m-%d-%Y %I:%M %p")
    LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
    posted_on = posted_on.replace(tzinfo=LOCAL_TIMEZONE)
    return posted_on


def get_tags(page_row: Element, message_id: int) -> [str]:
    """Return the Tags attached to the post"""
    # xpath_value = "// div[@class='TagList lia-component-tags lia-component-message-view-widget-tags-list'] / @id[contains(.,'tagsList')]"
    xpath_value = f'// div[@data-lia-message-uid={message_id}] // div[contains(@id,"tagsList")] / ul[@aria-label="Tags" and @role="list"]/li '

    tag_elements: [Element] = page_row.xpath(xpath_value)
    tags: set = set()
    for tag_element in tag_elements:
        tag_str = tag_element.text_content().strip().replace("Tags:", "")
        if tag_str:
            tags.add(tag_str)
    return list(sorted(tags))


def get_post_summary(page_row: Element, message_id: int) -> str:
    """Return a partial text/summary of the post"""
    xpath_value = f'// div[@data-lia-message-uid={message_id}] // div[@class="lia-truncated-body-container"] '

    summary_element: Element = page_row.xpath(xpath_value)[0]
    summary_str = summary_element.text_content().strip().replace("\t", " ").replace("\n", " ")
    return summary_str


def webscrap_data(page_rows: [Element]) -> pd.DataFrame:
    results: list = []
    for page_row in page_rows:
        my_post_id = get_message_id(page_row=page_row)

        my_post_url = get_post_url(page_row=page_row, message_id=my_post_id)
        my_username = get_username(page_row=page_row, message_id=my_post_id)
        my_post_datetime = get_posted_datetime(page_row=page_row, message_id=my_post_id)
        my_tags = get_tags(page_row=page_row, message_id=my_post_id)
        my_summary = get_post_summary(page_row=page_row, message_id=my_post_id)

        results.append({'hp_post_id': my_post_id,
                        'post_datetime': my_post_datetime,
                        'username': my_username,
                        'post_url': my_post_url,
                        'post_tags': my_tags,
                        'post_summary': my_summary
                        })

    result_df: pd.DataFrame = pd.DataFrame(results)
    return result_df


result_df = pd.DataFrame()
results_per_page: int = 50
offset_pages: int = int(2000 / 50) + 10
max_tries: int = 5
chrome_driver = ChromeHandler()

# https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&page=4&sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size=50


base_url = f"https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?filter=location&q=broken%20hinge&advanced=true&location=category:Notebook&" \
               f"sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size={results_per_page}"

page_source = chrome_driver.navigate_url(url=base_url).page_source

while True:

    if page_source is None:
        print(f'Page Source is None for url:\n{base_url}')
        continue

    page_rows = get_page_rows(page_source=page_source)
    if page_source is None or len(page_rows) == 0:
        print(f'No posts found for url:\n{base_url}')
        continue

    temp_df: pd.DataFrame = webscrap_data(page_rows=page_rows)
    result_df = pd.concat([result_df, temp_df], ignore_index=True, )
    print(f'Dataframe size is: {len(result_df)}')

    # click next page:
    xpath_value = "// span[@class='lia-paging-page-link']"
    next_element = chrome_driver.browser.find_element(by= By.XPATH, value=xpath_value)
    next_element.click()
    sleep(3)

    # result_df.drop_duplicates(subset=['post_id'], inplace=True)
print(result_df)
result_df.to_csv(path_or_buf='hp_hinges_issues.csv',
             sep=',',
             index=False
             )
