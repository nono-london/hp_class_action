import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from hp_class_action.app_config import get_project_download_path
from hp_class_action.hp_database.hp_forum_issue import (execute_query, get_connection,
                                                        fetch_query)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
LOCAL_FILE_NAME: str = str(Path().joinpath(get_project_download_path(), 'hp_hinges_issues.csv'))


def read_local_data():
    result_df = pd.read_csv(LOCAL_FILE_NAME,
                            sep=',',
                            parse_dates=['post_datetime'])
    print(result_df.drop_duplicates(subset=['hp_post_id', 'post_datetime'],
                                    keep='first'))
    return result_df


def upload_data(data_df: pd.DataFrame):
    sql_query = """
        INSERT INTO hp_forum_issues (
            hp_post_id, post_datetime, username,
            post_url,post_tags,post_summary
            )
            VALUES(
            %s,%s,%s,
            %s,%s,%s
            ) 
    """

    for index, row in data_df.iterrows():
        execute_query(sql_query=sql_query,
                      variables=(row['hp_post_id'], row['post_datetime'], row['username'],
                                 row['post_url'], json.dumps(row['post_tags']), row['post_summary']
                                 )
                      )


def chart_monthly_claims():
    """Charts monthly claims without last month"""
    sql_query: str = """
                SELECT STR_TO_DATE( CONCAT_WS('-',YEAR(post_datetime), MONTH(post_datetime),1),'%Y-%m-%d') AS "Claim Month"
                , COUNT(*) "Monthly Claims"
                FROM hp_trial.hp_forum_issues
                GROUP BY YEAR(post_datetime), MONTH(post_datetime)
                ORDER BY post_datetime
        """
    result_df = pd.read_sql(con=get_connection(),
                            sql=sql_query)

    result_df.set_index("Claim Month", inplace=True)
    # https://pandas.pydata.org/pandas-docs/version/0.13/visualization.html
    result_df = result_df.iloc[:-1, :]
    print(result_df)
    result_df.plot()
    plt.show()


def chart_yearly_claims():
    """Charts yearly claims"""
    sql_query: str = """
                SELECT STR_TO_DATE( CONCAT_WS('-',YEAR(post_datetime), 1,1),'%Y-%m-%d') AS "Claim Year"
                , COUNT(*) "Yearly Claims"
                FROM hp_trial.hp_forum_issues
                GROUP BY YEAR(post_datetime)
                ORDER BY post_datetime
        """
    result_df = pd.read_sql(con=get_connection(),
                            sql=sql_query)

    result_df.set_index("Claim Year", inplace=True)
    # https://pandas.pydata.org/pandas-docs/version/0.13/visualization.html
    result_df = result_df.iloc[:, :]
    print(result_df)
    result_df.plot()
    plt.show()


def all_claims():
    """Returns a df with claims from post id and from people who had same issue"""

    sql_query: str = """
            SELECT hp_post_id, post_datetime, username, me_too
            FROM hp_forum_issues
            ORDER BY post_datetime DESC
            LIMIT 50
        """
    results: list = fetch_query(sql_query=sql_query)
    for row_dict in results:
        if row_dict['me_too'] is not None:
            row_dict['me_too'] = json.loads(row_dict['me_too'])

    usernames:list = list(set([x['username'] for x in results]))
    # create list of me_too users
    print('#'*100)
    print(f'usernames:{usernames}')
    user_details: [dict] = [x['me_too'] for x in results if x['me_too'] is not None]
    print('#' * 100)
    print(f'usernames:{user_details}')
    print('#' * 100)
    username_set = set()
    for list_dict in user_details:
        for row_dict in list_dict:
            username_set.add(row_dict['username'])
    print(username_set)
    username_union = username_set.union(set(usernames))
    unclaimed_users = [x for x in username_union if x not in usernames]

    print('#' * 100)
    print(f'username_union:{user_details}')

    print('#' * 100)
    print(f'usernames len:{len(usernames)}')
    print(f'username_union len:{len(username_union)}')
    print(f'unclaimed_users len:{len(unclaimed_users)}')

    # unclaimed_users with claim_date
    for username in unclaimed_users:
        for row_dict in results:
            if row_dict['username']==username:
                print(row_dict['post_datetime'])






if __name__ == '__main__':
    all_claims()
    exit(0)
    chart_yearly_claims()
    exit(0)
    my_result_df = read_local_data()
    upload_data(my_result_df)
    chart_monthly_claims()
