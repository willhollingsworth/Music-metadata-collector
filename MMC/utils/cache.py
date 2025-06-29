"""Cache utilities."""

from __future__ import annotations

import json
from typing import Any

from mmc.constants import CACHE_FOLDER


def check_cache(url: str, file_type: str = "json") -> str | dict[str, Any] | None:
    """Check if a url is cached and return the contents if it exists."""
    CACHE_FOLDER.mkdir(exist_ok=True)
    processed_url = process_cache_url(url)
    full_path = CACHE_FOLDER / f"{processed_url}.{file_type}"
    if not full_path.exists():
        return None
    with full_path.open(encoding="utf-8") as file:
        if file_type == "json":
            return json.load(file)
        return file.read()


def write_cache(
    url: str,
    file_type: str,
    data: str | dict[str, Any] | list[Any],
) -> None:
    """Write data to a cache file."""
    CACHE_FOLDER.mkdir(exist_ok=True)
    processed_url = process_cache_url(url)
    full_path = CACHE_FOLDER / f"{processed_url}.{file_type}"
    with full_path.open("w", encoding="utf-8") as file:
        if file_type == "json":
            file.write(json.dumps(data, indent=4))
        else:
            file.write(str(data))


def process_cache_url(url: str) -> str:
    """Process a URL to create a valid cache filename."""
    striped_characters: str = r':/\|?"'
    processed_url: str = url
    for char in striped_characters:
        processed_url = processed_url.replace(char, "_")
    return processed_url


def delete_cache() -> None:
    """Delete all files in the cache folder."""
    if CACHE_FOLDER.exists():
        for file_path in CACHE_FOLDER.iterdir():
            if file_path.is_file():
                file_path.unlink()


def proccess_search_string(search_string: str) -> str:
    """Process a search string to ensure it is valid for searching."""
    result = ""
    result = search_string.replace("_", "")
    result = result.lower()
    return result


def load_cache_file(
    service: str,
    id_value: str = "",
) -> dict[str, Any]:
    """Search cache files for a single file of specific service and ID.

    Raises:
        ValueError: If anything but 1 exact file is found.

    """
    proceesed_service_name = proccess_search_string(service)
    cache_files = CACHE_FOLDER.iterdir()
    matching_file = [
        f
        for f in cache_files
        if f.is_file() and proceesed_service_name in f.name and id_value in f.name
    ]
    if len(matching_file) != 1:
        msg = (
            f"Multiple cache files found for service '{service}' and ID '{id_value}'. "
            "Please refine your search criteria."
        )
        raise ValueError(msg)
    with matching_file[0].open("r", encoding="utf-8") as f:
        return json.load(f)
