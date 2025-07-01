"""Cache utilities."""

from __future__ import annotations

import json
from pathlib import Path
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


def proccess_search_string(service_name: str, search_string: str) -> str:
    """Process a search string to ensure it is valid for searching."""
    proccessed = search_string
    if service_name == "music_brainz":
        proccessed = process_search_string_musicbrainz(search_string)
    if service_name == "last_fm":
        proccessed = process_search_string_last_fm(search_string)
    return proccessed.replace("_", "").lower()


def process_search_string_musicbrainz(search_string: str) -> str:
    """Process a search string for MusicBrainz to ensure it is valid for searching.

    handles mapping of search strings to MusicBrainz identifiers.
    """
    result = search_string
    if search_string == "track":
        result = "recording"
    elif search_string == "album":
        result = "release"
    return result


def process_search_string_last_fm(search_string: str) -> str:
    """Process a search string for lastfm to ensure it is valid for searching."""
    result = search_string
    if search_string == "last_fm":
        result = "audioscrobbler"
    return result


def filter_filenames(filenames: list[Path], search_string: str) -> list[Path]:
    """Filter a list of filenames based on a search string."""
    return [
        filename for filename in filenames if search_string in filename.name.lower()
    ]


def load_cache_file(
    service_name: str,
    search_strings: list[str],
) -> dict[str, Any]:
    """Load a cache file using a service name and a series of search strings.

    Raises:
        ValueError: If anything but exactly 1 file is found.

    """
    cache_files: list[Path] = list(CACHE_FOLDER.iterdir())

    processed_search_strings = [proccess_search_string(service_name, service_name)]
    processed_search_strings.extend(
        proccess_search_string(service_name, search_string)
        for search_string in search_strings
    )

    for filter_string in processed_search_strings:
        cache_files = filter_filenames(cache_files, filter_string)
    if len(cache_files) > 1:
        msg = (
            f"Multiple cache files found: {len(cache_files)}, "
            f"for search string '{processed_search_strings}'. "
            "Please refine your search criteria."
        )
        raise ValueError(msg)
    if len(cache_files) == 0:
        msg = (
            f"No cache files found for search string '{search_strings}'. "
            f"for service '{service_name}'. Please check the search criteria."
        )
        raise ValueError(msg)
    with cache_files[0].open("r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    """Main function to delete the cache folder."""
    search_restult = load_cache_file(
        service_name="music_brainz",
        search_strings=["track", "a9bdcdd0-e18b-4890-8b9c-b56aaa0792ab"],
    )
    print(search_restult)
