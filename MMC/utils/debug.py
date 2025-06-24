"""Debugging and other misc utility functions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def print_dict_keys(
    input_dict: dict[str, Any],
    keys: list[str | list[str]] | None = None,
) -> None:
    """Print specified keys from a dictionary in a nicer way.

    A list containing string or lists are accepted as keys.
    If a list is provided, it will be used to traverse the dictionary.
    """
    if keys is None or len(keys) < 1:  # if no keys specified then print all
        keys = input_dict.keys()
    for key in keys:
        if isinstance(key, str):
            print(key, ':', input_dict[key], end=', ')
        elif isinstance(key, list):
            print('-'.join(map(str, key)), end='')
            temp_dict = input_dict
            for i in key:
                temp_dict = temp_dict[i]
            print(' :', temp_dict, end=', ')
    print()


def save_to_file(data: str, filename: str) -> None:
    """Save data to a file."""
    file_path = Path(filename)
    with file_path.open('w', encoding='utf-8') as f:
        f.write(data)


def show_structure(var: Any, indent: int = 0) -> str:
    """Recursively show the structure of a variable."""
    if isinstance(var, dict):
        result = '{\n'
        for k, v in var.items():
            result += ' ' * (indent + 4) + f'{k}: {show_structure(v, indent + 4)},\n'
        result += ' ' * indent + '}'
        return result
    elif isinstance(var, list):
        result = '[\n'
        for v in var:
            result += ' ' * (indent + 4) + f'{show_structure(v, indent + 4)},\n'
        result += ' ' * indent + ']'
        return result
    else:
        return '...'


def print_structure(var: Any) -> None:
    """Print the structure of a variable."""
    print(show_structure(var))


def dump_json(json_data: dict[str, Any] | list[Any]) -> None:
    """Dump JSON data to a temp file."""
    temp_file = Path('temp.json')
    with temp_file.open('w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, indent=4))
