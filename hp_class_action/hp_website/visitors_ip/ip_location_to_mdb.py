import csv
from json import loads
from typing import Dict, Union
from urllib.error import URLError
from urllib.request import Request, urlopen

from hp_class_action.app_config import (get_hp_website_visitors_file_path)


def get_ip_info(ip_address: str) -> Union[None, Dict]:
    # https://ipapi.co/#pricing
    # 1000 call per month, 30k calls per month
    response_format = "json"
    url = f"https://ipapi.co/{ip_address}/{response_format}/"

    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print("The server couldn't fulfill the request.")
            print('Error code: ', e.code)
        return None

    # read JSOn data
    # https://stackoverflow.com/questions/32795460/loading-json-object-in-python-using-urllib-request-and-json-modules
    encoding = response.info().get_content_charset('utf-8')
    data = response.read()
    json_data = loads(data.decode(encoding))
    return json_data


def read_visitors_file(file_has_header: bool = True) -> tuple:
    """Return a tuple of list: (header, rows), where headers can be null"""
    # https://www.programiz.com/python-programming/file-operation
    # https://stackoverflow.com/questions/24662571/python-import-csv-to-list
    file_path = get_hp_website_visitors_file_path()[0]

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print(list(csv_reader))
        csv_table = list(csv_reader)
        if file_has_header:
            csv_headers = csv_table[0]
            csv_rows = csv_table[1:]
        else:
            csv_rows = csv_table
    return csv_headers, csv_rows


if __name__ == '__main__':
    print(read_visitors_file())
    # get_ip_info("104.47.70.126")
