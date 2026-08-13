import secrets
import src.crypto.kfd

DEFAULT_MEMORY_COST = src.crypto.kfd.DEFAULT_MEMORY_COST
DEFAULT_TIME_COST = src.crypto.kfd.DEFAULT_TIME_COST
DEFAULT_PARALLELISM = src.crypto.kfd.DEFAULT_PARALLELISM
SALT_LENGTH = src.crypto.kfd.SALT_LENGTH

def test_same_derived_keys():
    salt = secrets.token_bytes(SALT_LENGTH)

    derived_key1 = src.crypto.kfd.derive_key("MyPassword1234", salt,
                                             DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                             DEFAULT_PARALLELISM)

    derived_key2 = src.crypto.kfd.derive_key("MyPassword1234", salt,
                                             DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                             DEFAULT_PARALLELISM)

    assert derived_key1 == derived_key2

def test_different_derived_keys_from_salt():
    salt = secrets.token_bytes(16)
    salt1 = secrets.token_bytes(16)

    derived_key1 = src.crypto.kfd.derive_key("MyPassword1234", salt,
                                             DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                             DEFAULT_PARALLELISM)

    derived_key2 = src.crypto.kfd.derive_key("MyPassword1234", salt1,
                                             DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                             DEFAULT_PARALLELISM)

    assert derived_key1 != derived_key2

def test_different_derived_keys_from_password():
    salt = secrets.token_bytes(16)

    derived_key1 = src.crypto.kfd.derive_key("MyPassword1234", salt,
                                             DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                             DEFAULT_PARALLELISM)

    derived_key2 = src.crypto.kfd.derive_key("MyPassword1234@", salt,
                                             DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                             DEFAULT_PARALLELISM)

    assert derived_key1 != derived_key2

def test_derived_key_length():
    salt = secrets.token_bytes(16)
    derived_key = src.crypto.kfd.derive_key("MyPassword1234", salt,
                                             DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                             DEFAULT_PARALLELISM)
    assert len(derived_key) == 32

def test_derived_key_type():
    salt = secrets.token_bytes(16)
    derived_key = src.crypto.kfd.derive_key("MyPassword1234", salt,
                                            DEFAULT_MEMORY_COST, DEFAULT_TIME_COST,
                                            DEFAULT_PARALLELISM)
    assert isinstance(derived_key, bytes)