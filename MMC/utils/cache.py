"""Cache utilities."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import quote, urlparse

from mmc.constants import CACHE_FOLDER


def read_cache(url: str) -> dict[str, Any] | None:
    """Check if a url is cached and return the contents if it exists."""
    processed_cache_name = url_to_filename(url)
    cache_path = CACHE_FOLDER / f"{processed_cache_name}.json"
    if not cache_path.exists():
        return None
    with cache_path.open(encoding="utf-8") as file:
        return json.load(file)


def write_cache(cache_data: dict[str, Any], url: str) -> None:
    """Write data to a cache file."""
    processed_cache_name = url_to_filename(url)
    cache_path = CACHE_FOLDER / f"{processed_cache_name}.json"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("w", encoding="utf-8") as file:
        file.write(json.dumps(cache_data, indent=4))


def delete_cache() -> None:
    """Delete all files in the cache folder."""
    if CACHE_FOLDER.exists():
        for file_path in CACHE_FOLDER.iterdir():
            if file_path.is_file():
                file_path.unlink()


def url_to_filename(
    url: str,
) -> str:
    """Process URL into appropriate filename."""
    parsed_url = urlparse(url)
    filename = parsed_url.netloc + parsed_url.path
    if parsed_url.query:
        filename += "?" + parsed_url.query
    return quote(filename)


if __name__ == "__main__":
    test_url = "https://api.example.com/data?query=example&sort=asc"
    print(f"Original URL: {test_url}")
    print(f"Processed Cache Filename: {url_to_filename(test_url)}")
