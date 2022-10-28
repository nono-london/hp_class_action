"""Launch the scrappers """

import platform
from random import randint
from time import sleep
from time import time

from hp_class_action.deleted_users.deleted_usernames import check_user_still_exists
from hp_class_action.hinge_issue.scrap_data.scrap_metoo import update_summary_metoo
from hp_class_action.hinge_issue.scrap_data.scrap_search_query import webscrap_query_search
from hp_class_action.hp_database.backup_mdb import backup_mdb_to_csv


def launch_scrapper(max_pages: int = 10,
                    force_metoo_update: bool = False):
    start_time = time()
    # Backing up mdb
    print(f'_' * 100)
    print(f'Backing up locally the  mdb')
    backup_mdb_to_csv()

    # Handle broken hinges
    print(f'_' * 100)
    print(f'Scrapping Broken Hinge Issues')
    backup_mdb_to_csv()
    webscrap_query_search(max_pages=max_pages)
    update_summary_metoo(force_update=force_metoo_update)

    # Handle broken hinges
    print(f'_' * 100)
    print(f'Scrapping Deleted Users')
    sleep_time = randint(60, 320)
    print(f"Waiting for {round(sleep_time / 60, 1)} minutes")
    sleep(sleep_time)
    check_user_still_exists()

    # Time program for
    print(f'_' * 100)
    print(f'Program ran for:{round((time() - start_time) / 60 / 60, 1)} hours\n'
          f'Using os: {platform.uname().system}')


if __name__ == '__main__':
    launch_scrapper(max_pages=20,
                    force_metoo_update=True)
