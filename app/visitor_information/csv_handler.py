import csv
from pathlib import Path
from typing import Dict


def write_csv_file(csv_file_name, ip_address_dict: Dict, headers):
    folder_path = Path(Path(__file__).parent.parent, 'data_visitors')
    if not folder_path.exists():
        folder_path.mkdir(parents=True)
    file_full_path = Path(folder_path, csv_file_name)

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


if __name__ == '__main__':
    pass
