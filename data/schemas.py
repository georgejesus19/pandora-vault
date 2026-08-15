from datetime import datetime
from contextlib import suppress

def validate_entry(entry):
    """
    :param entry: A dict data structure that represents a vault entry
    :return: True if the entry is valid, False otherwise
    """

    if not isinstance(entry, dict):
        return False

    if entry.get("id") is None:
        return False

    if isinstance(entry.get("id"), int):
        if isinstance(entry.get("id"), bool):
            return False
        else:
            if entry.get("id") < 1:
                return False
    else:
        return False

    if entry.get("location") is None:
        return False

    if not isinstance(entry.get("location"), str):
        return False
    if entry.get("location").strip() == "":
        return False

    if not isinstance(entry.get("username"), str) and \
        entry.get("username") is not None:
        return False

    if entry.get("password") is None:
        return False

    if not isinstance(entry.get("password"), str):
        return False
    if entry.get("password").strip() == "" :
        return False

    if entry.get("created_at") is None:
        return False

    if not isinstance(entry.get("created_at"), str):
        return False

    data_created_at = None
    with suppress (ValueError):
        data_created_at = datetime.fromisoformat(entry.get("created_at"))
    if data_created_at is None:
        return False

    if entry.get("updated_at") is None:
        return False

    if not isinstance(entry.get("updated_at"), str):
        return False

    data_updated_at = None
    with suppress(ValueError):
        data_updated_at = datetime.fromisoformat(entry.get("updated_at"))
    if data_updated_at is None:
        return False

    return True