from hp_class_action.hp_database.backup_mdb import (backup_mdb_to_csv, read_csv_backup)


def test_backup_csv():
    print(backup_mdb_to_csv())


def test_read_backup():
    print(read_csv_backup())


if __name__ == '__main__':
    test_backup_csv()
    test_read_backup()
