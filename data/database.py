import os
import sqlite3
import datetime

base_path = os.path.dirname(os.path.abspath(__file__))
VAULT_DB_PATH = os.path.join(base_path, "vault.db")

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

def create_entry(location, username, ciphertext, nonce, authentication_tag,path=""):
    connection = None
    created_at = updated_at = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        query = """
                INSERT INTO entries (location, username, ciphertext, 
                nonce, authentication_tag, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                 """
        if path.strip() == "":
            connection = open_connection(VAULT_DB_PATH)
        else:
            connection = open_connection(path)
        if not connection:
            return False
        cursor = connection.cursor()
        cursor.execute(query, (location, username, ciphertext,
                               nonce, authentication_tag, created_at, updated_at))
        connection.commit()
        return True
    except Exception:
        return False
    finally:
        close_connection(connection)

def initialize_database(path=""):
    if path.strip() == "":
        connection = open_connection(VAULT_DB_PATH)
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