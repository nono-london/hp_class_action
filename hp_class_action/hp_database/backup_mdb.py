from pathlib import Path

import pandas as pd

from hp_class_action.app_config import get_project_download_path
from hp_class_action.hp_database.mdb_handlers import (fetch_query)


def backup_mdb_to_csv():
    file_full_name: str = str(Path(get_project_download_path(),
                                   f"mdb_backup.csv")
                              )
    sql_query: str = """
                    SELECT a.*, b.*
                    FROM hp_users a LEFT JOIN forum_posts b
                        ON a.user_id=b.user_id
                    ORDER BY a.username, b.post_datetime DESC
    """
    results = fetch_query(sql_query=sql_query)
    result_df = pd.DataFrame(results)
    result_df.to_csv(path_or_buf=file_full_name,
                     sep=',',
                     index=False)


if __name__ == '__main__':
    backup_mdb_to_csv()
