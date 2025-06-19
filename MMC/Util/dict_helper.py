from typing import Any


def map_dict_keys(
    input_dict: dict[str, Any],
    mapping_rules: list[tuple[str, str | list[str]]],
) -> dict[str, str]:
    """Map and transform dictionary keys based on provided rules.

    rule format is (new key, old key)
    if old key is a list then it will traverse the input dict
    """
    output_dict: dict[str, str] = {}
    for new_key, old_key_path in mapping_rules:
        if not isinstance(old_key_path, list):
            value = input_dict[old_key_path]
        else:
            value = input_dict
            for key in old_key_path:
                value = value[key]
        output_dict[new_key] = value
    return output_dict

if __name__ == "__main__":
    mapping_rules = [
        ('track name', 'title'),
        ('track id', 'id'),
        ('artist name', ['artist', 'name']),
        ('artist id', ['artist', 'id']),
        ('album name', ['album', 'title']),
        ('album id', ['album', 'id']),
    ]
    test_dict = {
        'title': 'Test Song',
        'id': '1',
        'artist': {
            'name': 'Test Artist',
            'id': '2'},
        'album': {
            'title': 'Test Album',
            'id': '3',
        },
    }
    result = map_dict_keys(test_dict, mapping_rules)
    print(result)
