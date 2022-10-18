from pathlib import Path
from sys import path

from hp_class_action.app_config import (get_project_download_path,
                                        get_project_root_path)


def test_project_in_sys_path():
    """Check if the project root folder is in sys.path"""
    assert get_project_root_path() in path


def test_download_folder_exists():
    assert Path(get_project_download_path()).exists()


if __name__ == '__main__':
    test_project_in_sys_path()
    test_download_folder_exists()
