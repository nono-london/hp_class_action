from hp_class_action.hp_database.hp_forum_issue_bis import (fetch_query)

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

if __name__ == '__main__':
    compare_users_with_old_data()