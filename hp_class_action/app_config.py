import sys
from pathlib import PurePath, Path
from typing import Union

#from selenium_helpers.app_config_secret import SELENIUM_URL as _SELENIUM_URL


def get_project_root_path() -> str:
    # https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
    root_dir = Path(__file__).cwd().resolve().parent
    return str(root_dir)


# def get_backup_selenium_folder() -> str:
#     root_dir = PurePath(f"//{_SELENIUM_URL}/F_usb_buffalo/Python/selenium_drivers")
#     return str(root_dir)


def get_project_download_path() -> str:
    # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
    download_folder_path = Path(get_project_root_path(), "hp_class_action", "downloads")
    if not download_folder_path.exists():
        download_folder_path.mkdir()
    return str(download_folder_path)


# def get_selenium_folder_path() -> Union[None, str]:
#     # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
#     chrome_windows_name: str = "chromedriver.exe"
#
#     if Path(get_project_download_path(), chrome_windows_name).is_file():
#         return str(get_project_download_path())
#     elif Path(get_backup_selenium_folder(), chrome_windows_name).is_file():
#         return str(get_backup_selenium_folder())
#     else:
#         return None


def pack_python_libs_in_path():
    python_app_folder_path: Path = Path(get_project_root_path()).parent

    mysql_helpers_folder_path: Path = Path(python_app_folder_path, 'mysql_helpers')
    print(mysql_helpers_folder_path)

    # insert path in 2nd position, first position is reserved
    if mysql_helpers_folder_path not in sys.path:
        sys.path.insert(1, str(mysql_helpers_folder_path))

    postgres_folder_path: Path = Path(python_app_folder_path, 'postgresql_helpers')
    # insert path in 2nd position, first position is reserved
    if postgres_folder_path not in sys.path:
        sys.path.insert(1, str(postgres_folder_path))

    proxy_helpers_folder_path: Path = Path(python_app_folder_path, 'proxy_helpers')
    # insert path in 2nd position, first position is reserved
    if proxy_helpers_folder_path not in sys.path:
        sys.path.insert(1, str(proxy_helpers_folder_path))

    selenium_folder_path: Path = Path(python_app_folder_path, 'selenium_helpers')
    # insert path in 2nd position, first position is reserved
    if selenium_folder_path not in sys.path:
        sys.path.insert(1, str(selenium_folder_path))


if __name__ == '__main__':
    print(get_project_root_path())

    print(get_project_download_path())
    # print(get_selenium_folder_path())
    # print(get_backup_selenium_folder())
    pack_python_libs_in_path()
