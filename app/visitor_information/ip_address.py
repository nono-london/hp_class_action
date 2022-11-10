import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from flask import (request)


def get_customer_ip_address():
    # getting IP address of customer
    http_x_real_ip = None
    remote_addr = None
    http_x_forwarded_for = None

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
    headers: List = ['visit_datetime', 'http_x_real_ip', 'remote_addr', 'http_x_forwarded_for']
    row: Dict = {'visit_datetime': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                 'http_x_real_ip': http_x_real_ip,
                 'remote_addr': remote_addr,
                 'http_x_forwarded_for': http_x_forwarded_for}

    write_ips_to_csv(row, headers)


def write_ips_to_csv(ip_address_dict: Dict, headers):
    folder_path = Path(Path(__file__).parent.parent, 'data_visitors')
    if not folder_path.exists():
        folder_path.mkdir(parents=True)
    file_full_path = Path(folder_path, 'visitor_ips.csv')

    if file_full_path.exists():
        write_type = 'a'
    else:
        write_type = 'w'

    with open(file_full_path, write_type, newline='') as file:
        # Create a CSV dictionary writer and add the student header as field names
        writer = csv.DictWriter(file, fieldnames=headers)
        # Use writerows() not writerow()
        if write_type == 'w':
            writer.writeheader()
        writer.writerow(ip_address_dict)


print(Path().joinpath(Path().cwd().parent, 'data_visitors'))
