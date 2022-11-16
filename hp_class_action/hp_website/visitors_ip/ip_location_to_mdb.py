import csv
from json import loads
from typing import Dict, Union, List, Tuple
from urllib.error import URLError
from urllib.request import Request, urlopen

from hp_class_action.app_config import (get_hp_website_visitors_file_path)
from hp_class_action.hp_database.mdb_handlers import execute_query


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


def upload_to_database(csv_row: List, row_headers: List, ip_info: Dict) -> bool:
    sql_query = """
                INSERT IGNORE INTO `hp_trial`.`website_visitors_info`
                    (`visit_datetime`, `visit_url`, `ip_address`, `city`, `region`,
                    `country_code`, `country_code_iso3`, `country_name`, `coordinate`, `timezone`,
                    `utc_offset`, `org`
                    )
                VALUES( %s,  %s, %s, %s, %s,
                         %s, %s, %s, 
                            POINT(%s,%s), %s,
                          %s, %s
                    );
                """

    parameters: Tuple = (
        csv_row[row_headers.index("visit_datetime")], csv_row[row_headers.index("visited_url")],
        ip_info['ip'], ip_info['city'], ip_info['region'],
        ip_info['country_code'], ip_info['country_code_iso3'], ip_info['country_name'],
        ip_info['latitude'], ip_info['longitude'], ip_info['country_code'],
        ip_info['utc_offset'], ip_info['org']
    )
    execute_query(sql_query=sql_query, variables=parameters)


def upload_data():
    headers, rows = read_visitors_file(file_has_header=True)
    for row in rows:
        ip_address = row[headers.index("http_x_real_ip")]
        ip_info = get_ip_info(ip_address)
        upload_to_database(csv_row=row, row_headers=headers, ip_info=ip_info)


if __name__ == '__main__':
    upload_data()
