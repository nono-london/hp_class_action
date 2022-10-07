import sys
from os import (makedirs as _makedirs)
from os.path import (dirname as _dirname, abspath as _abspath,
                     join as _join, isfile as _isfile, exists as _exists)


from selenium_helpers.app_config_secret import SELENIUM_URL as _SELENIUM_URL


def get_project_root_path():
    # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
    root_dir = _dirname(_dirname(_abspath(__file__)))
    return root_dir


def get_backup_selenium_folder():
    root_dir = f"//{_SELENIUM_URL}/F_usb_buffalo/Python/selenium_drivers"
    return root_dir


def get_project_download_path():
    # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
    download_folder_path = _join(get_project_root_path(), "hp_class_action", "downloads")
    if not _exists(download_folder_path):
        _makedirs(download_folder_path)
    return download_folder_path


def get_selenium_folder_path():
    # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
    chrome_windows_name: str = "chromedriver.exe"

    if _isfile(_join(get_project_download_path(), chrome_windows_name)):
        return get_project_download_path()
    elif _isfile(_join(get_backup_selenium_folder(), chrome_windows_name)):
        return get_backup_selenium_folder()
    else:
        return None


def pack_python_libs_in_path():
    python_app_folder_path: str = _dirname(get_project_root_path())

    mysql_helpers_folder_path: str = _join(python_app_folder_path, 'mysql_helpers')
    # insert path in 2nd position, first position is reserved
    if mysql_helpers_folder_path not in sys.path:
        sys.path.insert(1, mysql_helpers_folder_path)

    postgres_folder_path: str = _join(python_app_folder_path, 'postgresql_helpers')
    # insert path in 2nd position, first position is reserved
    if postgres_folder_path not in sys.path:
        sys.path.insert(1, postgres_folder_path)

    proxy_helpers_folder_path: str = _join(python_app_folder_path, 'proxy_helpers')
    # insert path in 2nd position, first position is reserved
    if proxy_helpers_folder_path not in sys.path:
        sys.path.insert(1, proxy_helpers_folder_path)

    selenium_folder_path: str = _join(python_app_folder_path, 'selenium_helpers')
    # insert path in 2nd position, first position is reserved
    if selenium_folder_path not in sys.path:
        sys.path.insert(1, selenium_folder_path)


if __name__ == '__main__':
    print(get_project_root_path())
    print(get_project_download_path())
    print(get_selenium_folder_path())
    print(get_backup_selenium_folder())
