from datetime import datetime
from pathlib import Path

import pandas as pd

from hp_class_action.app_config import get_project_download_path
from hp_class_action.hp_database.mdb_handlers import (fetch_query)

_MDB_BACKUP_FULL_PATH: str = str(Path(get_project_download_path(),
                                      f"mdb_backup.csv")
                                 )


def backup_mdb_to_csv() -> datetime:
    """Save a copy of all fields and tables from mdb
        Returns datetime at which the backup was created
    """
    sql_query: str = """
                    SELECT a.*, b.*
                    FROM hp_users a LEFT JOIN forum_posts b
                        ON a.user_id=b.user_id
                    ORDER BY a.username, b.post_datetime DESC
    """
    results = fetch_query(sql_query=sql_query)
    result_df = pd.DataFrame(results)
    result_df.to_csv(path_or_buf=_MDB_BACKUP_FULL_PATH,
                     sep=',',
                     index=False)
    creation_date = Path(_MDB_BACKUP_FULL_PATH).stat().st_ctime
    creation_date = datetime.fromtimestamp(creation_date)
    return creation_date


if __name__ == '__main__':
    print(backup_mdb_to_csv())
