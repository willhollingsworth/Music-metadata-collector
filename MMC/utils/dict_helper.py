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


def get_nested(
    nested_dict: dict[str, Any],
    keys: list[str | int] | str,
) -> str | list[Any] | dict[str, Any]:
    """Traverse nested dictionaries using a key or keys.

    Keys can be a single string, list of strings or a string with dot notation.
    nested dict can contain lists which require digit indexing.
    """
    processed_data: dict[str, Any] | list[Any] = nested_dict
    if isinstance(keys, str):
        if "." in keys:
            # allows for nested keys in a string format
            keys = list(keys.split("."))
        else:
            # adds support for non nested keys
            return nested_dict[keys]
    for key in keys:
        processed_key: str | int = key
        if isinstance(key, str) and key.isdigit():
            processed_key = int(key)
        processed_data = get_nested_value(processed_data, processed_key)
    return processed_data


def get_nested_value(
    nested_data: dict[str, Any] | list[Any],
    key: str | int,
) -> dict[str, Any] | list[Any]:
    """Get a value from a nested dictionary or list using a key.

    Raises:
        TypeError: If the nested_data is not a dict or list.
        KeyError: If the key is not found in the dictionary.

    """
    if isinstance(nested_data, dict) and isinstance(key, str):
        if key in nested_data:
            return nested_data[key]
        msg = f"Key '{key}' not found in the dictionary."
        raise KeyError(msg)
    if isinstance(nested_data, list) and isinstance(key, int):
        return nested_data[key]
    msg = f"Unsupported type for nested_data: {type(nested_data)} with key: {key}"
    raise TypeError(msg)


def test_mapping():
    mapping_rules: list[Any] = [
        ("track name", "title"),
        ("track id", "id"),
        ("artist name", ["artist", "name"]),
        ("artist id", ["artist", "id"]),
        ("album name", ["album", "title"]),
        ("album id", ["album", "id"]),
    ]
    test_dict: dict[str, Any] = {
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


def test_get_nested() -> None:
    test_dict: dict[str, Any] = {
        "a": [
            {"b": "value1"},
        ],
    }
    result = get_nested(test_dict, "a.0.b")
    print(result)


if __name__ == "__main__":
    # test_mapping()
    test_get_nested()
