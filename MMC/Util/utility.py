"""Utility functions and classes for music metadata collection."""

from __future__ import annotations

import json
import os
from typing import Any

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


def check_cache(url: str, file_type: str = 'json') -> str | None:
    """Check if a url is cached and return the contents if it exists."""
    cache_folder = 'cache/'
    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)
    processed_url = process_cache_url(url)
    full_path = f'{cache_folder}{processed_url}.{file_type}'
    if not os.path.exists(full_path):
        return None
    with open(full_path) as file:
        if file_type == 'json':
            return json.load(file)
        return file.read()


def write_cache(url: str, file_type: str, data: Any) -> None:
    """Write data to a cache file."""
    cache_folder = 'cache/'
    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)
    processed_url = process_cache_url(url)
    full_path = f'{cache_folder}{processed_url}.{file_type}'
    with open(full_path, 'w') as file:
        if file_type == 'json':
            file.write(json.dumps(data, indent=4))
        else:
            file.write(data)


def process_cache_url(url: str) -> str:
    """Process a URL to create a valid cache filename."""
    striped_characters: str = ':/\|?"'
    processed_url: str = url
    for char in striped_characters:
        processed_url = processed_url.replace(char, '_')
    return processed_url


def download_json(
        url: str,
        headers: dict[str, str] | None = None,
        overwrite: bool = False,
        debug: bool = False,
        ):
    """Download data from a URL and cache it locally."""
    file_type = 'json'
    if headers is None:
        headers = {}
    processed_url = url
    data = check_cache(url, file_type)
    if data is not None and not overwrite:
        if debug:
            print(f'Using cached data from {processed_url}')
    else:
        data = requests.get(url, headers=headers).json()
        if 'data' in data:
            data = data['data']
        if len(data) < 1:
            msg = f'Error, response too small: {data}'
            raise ValueError(msg)
        write_cache(url, file_type, data)
    if debug:
        print(data['tracks'].keys())
    return data


def download_html(
        url: str,
        headers: dict[str, str] | None = None,
        overwrite: bool = False,
        debug: bool = False,
        ):
    """Download data from a URL and cache it locally."""
    cache_folder = 'cache/'
    file_type = 'html'
    if headers is None:
        headers = {}
    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)
    striped_characters = ':/\|?"'
    processed_url = url
    for char in striped_characters:
        processed_url = processed_url.replace(char, '_')
    full_path = f'{cache_folder}{processed_url}.{file_type}'
    if os.path.exists(full_path) and not overwrite:
        with open(full_path, 'r') as file:
            response = file
    else:
        response = requests.get(url, headers=headers)
        if debug:
            print(response['tracks'].keys())
        if 'data' in response:
            response = response['data']
        if len(response) < 1:
            print('error, response too small', response)
            exit()
        with open(full_path, 'w') as file:
            file.write(response)
    return response

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
