from data import database


def test_database_creation():
    database_creation = database.initialize_database("test_file/test_database.db")
    assert database_creation

def test_database_entries():
    expected_colunms = ["id", "location", "username", "ciphertext",
                        "nonce", "authentication_tag", "created_at", "updated_at"]

    connection = database.open_connection("test_file/test_database.db")
    cursor = connection.cursor()
    info = cursor.execute("PRAGMA table_info('entries')").fetchall()
    database.close_connection(connection)

    columns_name = [line["name"] for line in info]
    assert expected_colunms == columns_name