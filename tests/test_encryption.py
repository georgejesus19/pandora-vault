import pytest
import secrets
import src.crypto.kfd as kfd
import src.crypto.encryption as encryption
from cryptography.exceptions import InvalidTag

DEFAULT_MEMORY_COST = kfd.DEFAULT_MEMORY_COST
DEFAULT_TIME_COST = kfd.DEFAULT_TIME_COST
DEFAULT_PARALLELISM = kfd.DEFAULT_PARALLELISM
SALT_LENGTH = kfd.SALT_LENGTH
NONCE_LENGTH = encryption.NONCE_LENGTH

def test_encrypt_returns_expected_types():
    salt = secrets.token_bytes(SALT_LENGTH)

    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    encrypted_data = encryption.encrypt(key, b'Test data')

    assert isinstance(encrypted_data, dict)
    assert isinstance(encrypted_data['ciphertext'], bytes)
    assert isinstance(encrypted_data['nonce'], bytes)
    assert isinstance(encrypted_data['authentication_tag'], bytes)

def test_encrypt_generates_new_nonce():
    salt = secrets.token_bytes(SALT_LENGTH)

    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    encrypted_data1 = encryption.encrypt(key, b'Test data')
    encrypted_data2 = encryption.encrypt(key, b'Test data')

    assert encrypted_data1['nonce'] != encrypted_data2['nonce']
    assert encrypted_data1['ciphertext'] != encrypted_data2['ciphertext']

def test_encrypt_decrypt_round_trip():
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    plaintext = b'Test data'

    encrypted_data = encryption.encrypt(key, plaintext)
    decrypted_data = encryption.decrypt(key, encrypted_data['nonce'], encrypted_data['ciphertext'], encrypted_data['authentication_tag'])

    assert plaintext == decrypted_data

def test_decrypt_rejects_wrong_key():
    salt = secrets.token_bytes(SALT_LENGTH)
    key1 = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    key2 = kfd.derive_key("MyPassword1234@", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    plaintext = b'Test data'

    encrypted_data = encryption.encrypt(key1, plaintext)

    with pytest.raises(InvalidTag) as exc_info:
        decrypted_data = encryption.decrypt(key2, encrypted_data['nonce'], encrypted_data['ciphertext'],
        encrypted_data['authentication_tag'])

def test_decrypt_rejects_modified_ciphertext():
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                          DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                          DEFAULT_PARALLELISM)

    plaintext = b'Test data'

    encrypted_data = encryption.encrypt(key, plaintext)

    encrypted_data['ciphertext'] = bytearray(encrypted_data['ciphertext'])
    encrypted_data['ciphertext'][0] ^= 1
    encrypted_data['ciphertext'] = bytearray(encrypted_data['ciphertext'])

    with pytest.raises(InvalidTag):
        decrypted_data = encryption.decrypt(key, encrypted_data['nonce'], encrypted_data['ciphertext'],
        encrypted_data['authentication_tag'])

def test_decrypt_rejects_modified_tag():
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    plaintext = b'Test data'

    encrypted_data = encryption.encrypt(key, plaintext)

    encrypted_data['authentication_tag'] = bytearray(encrypted_data['authentication_tag'])
    encrypted_data['authentication_tag'][0] ^= 1
    encrypted_data['authentication_tag'] = bytearray(encrypted_data['authentication_tag'])

    with pytest.raises(InvalidTag):
        decrypted_data = encryption.decrypt(key, encrypted_data['nonce'], encrypted_data['ciphertext'],
        encrypted_data['authentication_tag'])

def test_decrypt_rejects_modified_nonce():
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    plaintext = b'Test data'

    encrypted_data = encryption.encrypt(key, plaintext)

    encrypted_data['nonce'] = bytearray(encrypted_data['nonce'])
    encrypted_data['nonce'][0] ^= 1
    encrypted_data['nonce'] = bytearray(encrypted_data['nonce'])

    with pytest.raises(InvalidTag):
        decrypted_data = encryption.decrypt(key, encrypted_data['nonce'], encrypted_data['ciphertext'],
        encrypted_data['authentication_tag'])

def test_nonce_length():
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    plaintext = b'Test data'
    encrypted_data = encryption.encrypt(key, plaintext)

    assert len(encrypted_data['nonce']) == 12

def test_authentication_tag_length():
    salt = secrets.token_bytes(SALT_LENGTH)
    key = kfd.derive_key("MyPassword1234", salt,
                         DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                         DEFAULT_PARALLELISM)

    plaintext = b'Test data'
    encrypted_data = encryption.encrypt(key, plaintext)

    assert len(encrypted_data['authentication_tag']) == 16