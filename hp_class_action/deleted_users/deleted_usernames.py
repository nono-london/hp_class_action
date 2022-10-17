from hp_class_action.hp_database.mdb_handlers import (fetch_query)


def compare_users_with_old_data():
    """compare usrnames between table: hp_forum_issues(old) and hp_posts(new)"""
    sql_query_old_usernames = """
        SELECT distinct(username)
        FROM hp_trial.hp_forum_issues
        ORDER BY username 
        """
    old_usernames = fetch_query(sql_query=sql_query_old_usernames)
    old_usernames = [username['username'] for username in old_usernames]

    sql_query_new_usernames = """
            SELECT distinct(username)
            FROM hp_trial.hp_users
            ORDER BY username 
            """
    new_usernames = fetch_query(sql_query=sql_query_new_usernames)
    new_usernames = [username['username'] for username in new_usernames]

    print(f'Old usernames size: {len(old_usernames)}')
    print(f'New usernames size: {len(new_usernames)}')

    deleted_usernames = list(set(old_usernames) - set(new_usernames))
    print(f'Deleted usernames size: {len(deleted_usernames)}')

    # check if deleted users are in new database=> then logic problem

    sql_query = """SELECT username FROM hp_users WHERE username=%s"""
    tested_users = []
    for deleted_user in deleted_usernames:
        fetch_result = fetch_query(sql_query=sql_query,
                                   variables=(deleted_user,))
        if len(fetch_result) > 0:
            tested_users.append(fetch_result, )

    print(f'Logic problem size:{len(tested_users)}')

    sql_query = """SELECT post_url FROM hp_forum_issues WHERE username=%s"""

    for deleted_user in deleted_usernames:
        fetch_deleted_posts = fetch_query(sql_query=sql_query,
                                          variables=(deleted_user,))
        print(fetch_deleted_posts)

    print(len(deleted_usernames))


if __name__ == '__main__':
    compare_users_with_old_data()
