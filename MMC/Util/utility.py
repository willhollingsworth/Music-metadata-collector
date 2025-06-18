"""Utility functions and classes for music metadata collection."""

from __future__ import annotations

import json
import os
from typing import Any, Optional

import requests


def print_dict_keys(
    input_dict: dict[str, Any],
    keys: list[str | list[str]] | None = None,
) -> None:
    """Print specified keys from a dictionary in a nicer way."""
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


def download_data(
        url: str,
        headers: dict[str, str] | None = None,
        overwrite: bool = False,
        debug: bool = False,
        file_type: str = 'json',
        ):
    """Download data from a URL and cache it locally."""
    cache_folder = 'cache/'
    if headers is None:
        headers = {}
    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)
    striped_characters = ':/\|?"'
    processed_url = url
    for char in striped_characters:
        processed_url = processed_url.replace(char, '_')

    full_path = cache_folder + processed_url
    if file_type == 'json':
        full_path += '.json'
    if file_type == 'html':
        full_path += '.html'
    if os.path.exists(full_path) and not overwrite:
        with open(full_path, 'r') as f:
            r = json.load(f) if file_type == 'json' else f
    else:
        r = requests.get(url, headers=headers)
        if file_type == 'json':
            r = r.json()
        if debug:
            print(r['tracks'].keys())
        if 'data' in r:
            r = r['data']
        if len(r) < 1:
            print('error, response too small', r)
            exit()
        with open(full_path, 'w') as f:
            if file_type == 'json':
                f.write(json.dumps(r, indent=4))
            else:
                f.write(r)
    return r


class InvalidServiceException(Exception):
    """Custom exception for invalid service selection."""
    pass


def load_credentials(service: str) -> dict[str, str]:
    """Load credentials for a given service from a JSON file.

    Args:
        service (str): The name of the service to load credentials for.

    Returns:
        dict: The credentials for the specified service.

    Raises:
        InvalidServiceException: If the specified service is not valid.

    """
    valid_services = ['spotify', 'last_fm', 'genius']
    if service not in valid_services:
        msg = (
            f"Invalid service: {service}. "
            f"Please choose from the following valid services: {valid_services}."
        )
        raise InvalidServiceException(msg)
    # load credentials via json
    with open('credentials.json', encoding='utf-8') as r:
        return json.load(r)[service]


def save_to_file(data, filename) -> None:
    """Save data to a file."""
    with open(filename, 'w') as f:
        f.write(data)


def show_structure(var, indent=0):
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


def print_structure(var) -> None:
    """Print the structure of a variable."""
    print(show_structure(var))


def dump_json(json_data):
    """Dump JSON data to a temp file."""
    with open('temp.json', 'w') as f:
        f.write(json.dumps(json_data, indent=4))


def delete_cache():
    """Delete all files in the cache folder."""
    cache_folder = 'cache/'
    for file in os.listdir(cache_folder):
        os.remove(cache_folder + file)
