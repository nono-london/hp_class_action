"""Launch the search scrapper and the me_too scrapper"""

from hp_class_action.hinge_issue.scrap_data.scrap_search_query import webscrap_query_search
from hp_class_action.hinge_issue.scrap_data.scrap_metoo import update_summary_metoo


def launch_scrapper():
    webscrap_query_search(max_pages=10)
    update_summary_metoo(force_update=False)


if __name__ == '__main__':
    launch_scrapper()
