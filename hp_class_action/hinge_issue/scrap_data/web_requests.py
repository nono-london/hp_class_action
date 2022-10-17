from typing import Union

import requests
from requests.exceptions import ConnectionError

BASE_URL: str = "https://h30434.www3.hp.com/t5/ratings/ratingdetailpage/message-uid/8499984/rating-system/forum_topic_metoo/page/1#userlist"

hp_cookies = None


def get_web_page(url_to_open: str,
                 max_tries: int = 10,
                 timeout: int = 10,
                 check_response_url: bool = False) -> Union[None, str]:
    """Return page source of page if found
        check_response_url: check if response URL is identical to url_to_open=> useful to avoid redirect or infinite loops
    """

    global hp_cookies
    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    page_content: Union[None, str] = None
    max_tries: int = max_tries
    while max_tries > 0:
        try:
            response = requests.get(url=url_to_open, headers=headers, timeout=timeout, cookies=hp_cookies)
            if check_response_url:
                if response.url != url_to_open:
                    return None
            page_content = response.text
            hp_cookies = response.cookies
            break
        except ConnectionError as ex:
            print(f'Error while connecting:\n{ex}')
            max_tries -= 1

    return page_content


if __name__ == '__main__':
    print(get_web_page(url_to_open=BASE_URL,
                       max_tries=10))
