from data import schemas

valid_entry = {
    "id": 1,
    "location": "Github.com",
    "username": "ArthurTepes",
    "password": "Polkadot2024@",
    "created_at": "2026-08-15T13:42:31+00:00",
    "updated_at": "2026-08-15T13:42:31+00:00",
    }

def test_valid_entry():
    assert schemas.validate_entry(valid_entry)

def test_valid_entry_without_username():
    valid_entry = {
        "id": 1,
        "location": "Github.com",
        "username": None,
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }
    assert schemas.validate_entry(valid_entry)

def test_invalid_entry_type():
    assert not schemas.validate_entry("Test String")

def test_invalid_id():
    invalid_entry = {
        "location": "Github.com",
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry1 = {
        "id": [],
        "location": "Github.com",
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry2 = {
        "id": True,
        "location": "Github.com",
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry3 = {
        "id": "abc",
        "location": "Github.com",
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry4 = {
        "id": -1,
        "location": "Github.com",
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    assert not schemas.validate_entry(invalid_entry)
    assert not schemas.validate_entry(invalid_entry1)
    assert not schemas.validate_entry(invalid_entry2)
    assert not schemas.validate_entry(invalid_entry3)
    assert not schemas.validate_entry(invalid_entry4)

def test_invalid_location():
    invalid_entry = {
        "id": 1,
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry1 = {
        "id": 1,
        "location": [],
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry2 = {
        "id": 1,
        "location": "   ",
        "username": "ArthurTepes",
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    assert not schemas.validate_entry(invalid_entry)
    assert not schemas.validate_entry(invalid_entry1)
    assert not schemas.validate_entry(invalid_entry2)

def test_invalid_username_type():
    invalid_entry = {
        "id": 1,
        "location": "Teams",
        "username": (),
        "password": "Polkadot2024@",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    assert not schemas.validate_entry(invalid_entry)

def test_invalid_password():
    invalid_entry = {
        "id": 1,
        "location": "NetBeans",
        "username": "ArthurTepes",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry1 = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": {},
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry2 = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": "  ",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    assert not schemas.validate_entry(invalid_entry)
    assert not schemas.validate_entry(invalid_entry1)
    assert not schemas.validate_entry(invalid_entry2)

def test_invalid_created_at_date():
    invalid_entry = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": "Polk@dot2024",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry1 = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": "Polk@dot2024",
        "created_at": 12344,
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry2 = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": "Polk@dot2024",
        "created_at": "18/12/2005",
        "updated_at": "2026-08-15T13:42:31+00:00",
    }

    assert not schemas.validate_entry(invalid_entry)
    assert not schemas.validate_entry(invalid_entry1)
    assert not schemas.validate_entry(invalid_entry2)

def test_invalid_updated_at_date():
    invalid_entry = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": "Polk@dot2024",
        "created_at": "2026-08-15T13:42:31+00:00",
    }

    invalid_entry1 = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": "Polk@dot2024",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": 1234,
    }

    invalid_entry2 = {
        "id": 1,
        "location": "Teams",
        "username": "ArthurTeoes",
        "password": "Polk@dot2024",
        "created_at": "2026-08-15T13:42:31+00:00",
        "updated_at": "18/12/2005",
    }

    assert not schemas.validate_entry(invalid_entry)
    assert not schemas.validate_entry(invalid_entry1)
    assert not schemas.validate_entry(invalid_entry2)