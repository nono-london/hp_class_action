from hp_class_action.hp_database.mdb_handlers import (fetch_query,
                                                      get_connection)


def test_connection():
    conn = get_connection()
    print(f'is mdb connected: {conn.is_connected()}')
    conn.disconnect()
    conn.close()
    print(f'is mdb connected: {conn.is_connected()}')


def test_fetch_data():
    sql_query = """
    SELECT *
    FROM hp_forum_issues
    LIMIT 5
    """
    print(fetch_query(sql_query=sql_query))


if __name__ == '__main__':
    test_connection()
    test_fetch_data()
