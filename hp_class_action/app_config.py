import sys
from pathlib import Path


def get_project_root_path() -> str:
    # https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
    root_dir = Path(__file__).resolve().parent.parent
    return str(root_dir)


def get_project_download_path() -> str:
    # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
    download_folder_path = Path(get_project_root_path(), "hp_class_action", "downloads")
    if not download_folder_path.exists():
        download_folder_path.mkdir(parents=True)
    return str(download_folder_path)


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

    pack_python_libs_in_path()
