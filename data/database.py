import os
import sqlite3

def open_connection(path):
    try:
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        return None

def close_connection(connection):
    if connection:
        try:
            connection.close()
        except Exception:
            pass

def initialize_database(path=""):
    if path.strip() == "":
        base_path = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_path, "vault.db")
        connection = open_connection(db_path)
    else:
        connection = open_connection(path)
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
            id                  INTEGER PRIMARY KEY,
            location            TEXT NOT NULL,
            username            TEXT,
            ciphertext          BLOB NOT NULL,
            nonce               BLOB NOT NULL,
            authentication_tag  BLOB NOT NULL,
            created_at          TEXT NOT NULL,
            updated_at          TEXT NOT NULL)
            """)
        connection.commit()
        return True
    except Exception:
        return False
    finally:
        close_connection(connection)