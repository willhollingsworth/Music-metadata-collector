"""Cache utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def check_cache(url: str, file_type: str = 'json') -> str | dict[str, Any] | None:
    """Check if a url is cached and return the contents if it exists."""
    cache_folder = Path('cache')
    cache_folder.mkdir(exist_ok=True)
    processed_url = process_cache_url(url)
    full_path = cache_folder / f'{processed_url}.{file_type}'
    if not full_path.exists():
        return None
    with full_path.open(encoding='utf-8') as file:
        if file_type == 'json':
            return json.load(file)
        return file.read()


def write_cache(
    url: str, file_type: str, data: str | dict[str, Any] | list[Any],
) -> None:
    """Write data to a cache file."""
    cache_folder = Path('cache')
    cache_folder.mkdir(exist_ok=True)
    processed_url = process_cache_url(url)
    full_path = cache_folder / f'{processed_url}.{file_type}'
    with full_path.open('w', encoding='utf-8') as file:
        if file_type == 'json':
            file.write(json.dumps(data, indent=4))
        else:
            file.write(str(data))


def process_cache_url(url: str) -> str:
    """Process a URL to create a valid cache filename."""
    striped_characters: str = r':/\|?"'
    processed_url: str = url
    for char in striped_characters:
        processed_url = processed_url.replace(char, '_')
    return processed_url


def delete_cache() -> None:
    """Delete all files in the cache folder."""
    cache_folder = Path('cache')
    if cache_folder.exists():
        for file_path in cache_folder.iterdir():
            if file_path.is_file():
                file_path.unlink()
