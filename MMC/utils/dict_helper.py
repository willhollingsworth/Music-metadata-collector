"""Dictionary helper functions."""

from typing import Any


def map_dict_keys(
    input_dict: dict[str, Any],
    mapping_rules: list[tuple[str, str | list[str]]],
) -> dict[str, Any]:
    """Map and transform dictionary keys based on provided rules.

    rule format is (new key, old key)
    if old key is a list then it will traverse the input dict
    """
    output_dict: dict[str, Any] = {}
    for new_key, old_key_path in mapping_rules:
        if not isinstance(old_key_path, list):
            value = input_dict[old_key_path]
        else:
            value = input_dict
            for key in old_key_path:
                value = value[key]
        output_dict[new_key] = value
    return output_dict


def get_nested(nested_dict: dict[str, Any], keys: list[str] | str) -> Any:
    """Traverse nested dictionaries using a list of keys."""
    if isinstance(keys, str):
        if "." in keys:
            # allows for nested keys in a string format
            keys = keys.split(".")
        else:
            # adds support for non nested keys
            return nested_dict[keys]
    for key in keys:
        nested_dict = nested_dict[key]
    return nested_dict


if __name__ == "__main__":
    mapping_rules = [
        ("track name", "title"),
        ("track id", "id"),
        ("artist name", ["artist", "name"]),
        ("artist id", ["artist", "id"]),
        ("album name", ["album", "title"]),
        ("album id", ["album", "id"]),
    ]
    test_dict = {
        "title": "Test Song",
        "id": "1",
        "artist": {"name": "Test Artist", "id": "2"},
        "album": {
            "title": "Test Album",
            "id": "3",
        },
    }
    result = map_dict_keys(test_dict, mapping_rules)
    print(result)
