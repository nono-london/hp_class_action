from datetime import datetime
from pathlib import Path
from typing import Dict, List

from flask import (request)

from app.visitor_information.csv_handler import write_csv_file


def get_customer_ip_address():
    # getting IP address of customer
    http_x_real_ip = None
    remote_addr = None
    http_x_forwarded_for = None
    visited_url = request.url
    print(f"request.headers:\n"
          f"{request.headers}")
    header_agent = request.headers.get('User-Agent')

    try:
        http_x_real_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    except Exception as ex:
        print(f'Error while getting "http_x_real_ip"\n'
              f'{ex}')
    try:
        remote_addr = request.environ['REMOTE_ADDR']
    except Exception as ex:
        print(f'Error while getting "remote_addr"\n'
              f'{ex}')

    try:
        http_x_forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    except Exception as ex:
        print(f'Error while getting "http_x_forwarded_for"\n'
              f'{ex}')
    print(f'http_x_real_ip: {http_x_real_ip}, '
          f'remote_addr:{remote_addr}, '
          f'http_x_forwarded_for:{http_x_forwarded_for}')
    headers: List = ['visit_datetime', 'http_x_real_ip',
                     'remote_addr', 'http_x_forwarded_for',
                     'visited_url', 'user_agent']
    row: Dict = {'visit_datetime': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                 'http_x_real_ip': http_x_real_ip,
                 'remote_addr': remote_addr,
                 'http_x_forwarded_for': http_x_forwarded_for,
                 'visited_url': visited_url,
                 'user_agent': header_agent
                 }

    write_csv_file(csv_file_name='visitor_ips.csv', headers=headers, ip_address_dict=row, )


if __name__ == '__main__':
    print(Path().joinpath(Path().cwd().parent, 'data_visitors'))
