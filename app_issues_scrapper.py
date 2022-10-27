"""Launch the scrappers """

from hp_class_action.hinge_issue.scrap_data.scrap_search_query import webscrap_query_search
from hp_class_action.hinge_issue.scrap_data.scrap_metoo import update_summary_metoo
from hp_class_action.hp_database.backup_mdb import backup_mdb_to_csv
from hp_class_action.deleted_users.deleted_usernames import check_user_still_exists
from time import sleep
from random import randint


def launch_scrapper(max_pages: int = 10,
                    force_metoo_update: bool = False):
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


if __name__ == '__main__':
    launch_scrapper(max_pages=20,
                    force_metoo_update=True)
