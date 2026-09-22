import secrets
import pytest
from data import database
import src.crypto.kfd as kfd
import src.crypto.encryption as encryption

DEFAULT_MEMORY_COST = kfd.DEFAULT_MEMORY_COST
DEFAULT_TIME_COST = kfd.DEFAULT_TIME_COST
DEFAULT_PARALLELISM = kfd.DEFAULT_PARALLELISM
SALT_LENGTH = kfd.SALT_LENGTH
NONCE_LENGTH = encryption.NONCE_LENGTH

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

def test_create_entry():
    database.initialize_database("test_file/test_database.db")
    salt =  secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)
    encrypted_data = encryption.encrypt(key, b'Test data')
    entry = database.create_entry("github", "georgehebo", encrypted_data["ciphertext"],
                                  encrypted_data["nonce"], encrypted_data["authentication_tag"],
                                  "test_file/test_database.db")
    assert entry

def test_create_entry_data(tmp_path):
    db_path = tmp_path / "test_database.db"
    database.initialize_database(str(db_path))
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)
    encrypted_data = encryption.encrypt(key, b'Test data')
    database.create_entry("github", "georgehebo", encrypted_data["ciphertext"],
                                  encrypted_data["nonce"], encrypted_data["authentication_tag"],
                                  str(db_path))
    connection = database.open_connection(str(db_path))
    cursor = connection.cursor()
    query = "SELECT * FROM entries"
    entry = cursor.execute(query).fetchone()
    database.close_connection(connection)

    assert entry["created_at"]
    assert entry["updated_at"]
    assert entry["location"] == "github"
    assert entry["username"] == "georgehebo"
    assert entry["ciphertext"] == encrypted_data["ciphertext"]
    assert entry["nonce"] == encrypted_data["nonce"]
    assert entry["authentication_tag"] == encrypted_data["authentication_tag"]

def test_create_entry_invalid_db_path():
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)
    encrypted_data = encryption.encrypt(key, b'Test data')
    entry = database.create_entry("github", "georgehebo", encrypted_data["ciphertext"],
                          encrypted_data["nonce"], encrypted_data["authentication_tag"],
                          "invalid/path/database.db")
    assert not entry