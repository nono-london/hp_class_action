import pandas as pd
import json
from hp_class_action.hp_database.hp_forum_issue import execute_query

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def read_local_data():
    result_df = pd.read_csv('hp_hinges_issues.csv',
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


if __name__ == '__main__':
    my_result_df = read_local_data()
    upload_data(my_result_df)
