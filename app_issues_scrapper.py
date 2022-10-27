"""Launch the search scrapper and the me_too scrapper"""

from hp_class_action.hinge_issue.scrap_data.scrap_search_query import webscrap_query_search
from hp_class_action.hinge_issue.scrap_data.scrap_metoo import update_summary_metoo
from hp_class_action.hp_database.backup_mdb import backup_mdb_to_csv


def launch_scrapper(max_pages: int = 10,
                    force_metoo_update: bool = False):
    print(f'_' * 100)
    print(f'Scrapping Broken Hinge issues')
    backup_mdb_to_csv()
    webscrap_query_search(max_pages=max_pages)
    update_summary_metoo(force_update=force_metoo_update)
    print(f'_' * 100)


if __name__ == '__main__':
    launch_scrapper(max_pages=20,
                    force_metoo_update=True)
