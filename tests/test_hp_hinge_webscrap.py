from hp_class_action.hinge_issue.scrap_data.scrap_metoo import update_summary_metoo
from hp_class_action.hinge_issue.scrap_data.scrap_search_query import webscrap_query_search


def test_webscrap_hinge_search():
    webscrap_query_search(max_pages=2)


def test_webscrap_metoo():
    update_summary_metoo(force_update=False)


if __name__ == '__main__':
    test_webscrap_hinge_search()
