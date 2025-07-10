import json
import random
import string
from typing import Any

from mmc.constants import TEST_FIXTURE_DIR


def write_json_fixture(data: dict[str, Any] | list[Any], path: str) -> None:
    """Write a JSON fixture to a file."""
    fixture_folder = TEST_FIXTURE_DIR / path
    fixture_folder.parent.mkdir(parents=True, exist_ok=True)
    with fixture_folder.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def random_string(length: int = 8) -> str:
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choices(letters, k=length))
