import json

import matplotlib.pyplot as plt
import pandas as pd

from hp_class_action.hp_database.hp_forum_issue import (get_connection,
                                                        fetch_query)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def chart_monthly_claims(from_year: int = 2018):
    """Charts monthly claims without last month"""
    sql_query: str = """
                SELECT STR_TO_DATE( CONCAT_WS('-',YEAR(post_datetime), 
                            MONTH(post_datetime),1),'%Y-%m-%d') AS "Claimed Month"
                , COUNT(*) "Monthly Claims"
                FROM forum_posts
                WHERE post_datetime>= STR_TO_DATE( 
                        CONCAT_WS('-', %s, 1, 1),'%Y-%m-%d')
                GROUP BY YEAR(post_datetime), MONTH(post_datetime)
                ORDER BY post_datetime
        """
    result_df = pd.read_sql(con=get_connection(),
                            sql=sql_query,
                            params=(from_year,))
    result_df['Claimed Month'] = pd.to_datetime(result_df['Claimed Month'])

    result_df.set_index("Claimed Month", inplace=True)
    # https://pandas.pydata.org/pandas-docs/version/0.13/visualization.html
    result_df = result_df.iloc[:-1, :]
    print(result_df)
    result_df.plot()
    plt.show()


def chart_yearly_claims(from_year: int = 2018):
    """Charts yearly claims"""
    sql_query: str = """
                SELECT STR_TO_DATE( CONCAT_WS('-',YEAR(post_datetime), 1,1),'%Y-%m-%d') 
                        AS "Claimed Year"
                , COUNT(*) "Yearly Claims"
                FROM forum_posts
                WHERE post_datetime>= STR_TO_DATE( 
                        CONCAT_WS('-', %s, 1, 1),'%Y-%m-%d')
                GROUP BY YEAR(post_datetime)
                ORDER BY post_datetime
        """
    result_df: pd.DataFrame = pd.read_sql(con=get_connection(),
                                          sql=sql_query,
                                          params=(from_year,))
    result_df['Claimed Year'] = pd.to_datetime(result_df['Claimed Year'])

    result_df.set_index("Claimed Year", inplace=True)
    # https://pandas.pydata.org/pandas-docs/version/0.13/visualization.html
    result_df = result_df.iloc[:, :]
    print(result_df)
    result_df.plot()
    plt.show()


def all_claims(from_year: int = 2018):
    """Returns a df with claims from post id and from people who had same issue"""

    sql_query: str = """
            SELECT b.username, a.hp_post_id, a.post_datetime, a.me_too
            FROM forum_posts a INNER JOIN hp_users b 
                ON a.user_id=b.user_id
            WHERE a.post_datetime>=STR_TO_DATE( 
                        CONCAT_WS('-', %s, 1, 1),'%Y-%m-%d')
            ORDER BY a.post_datetime DESC
        """
    results: list = fetch_query(sql_query=sql_query,
                                variables=(from_year,))
    for row_dict in results:
        if row_dict['me_too'] is not None:
            row_dict['me_too'] = json.loads(row_dict['me_too'])

    usernames: list = list(set([x['username'] for x in results]))
    # create list of me_too users
    print('#' * 100)
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
            if row_dict['username'] == username:
                print(row_dict['post_datetime'])


if __name__ == '__main__':
    all_claims()
    exit(0)

    chart_monthly_claims()
    exit(0)

    chart_yearly_claims()
    exit(0)
