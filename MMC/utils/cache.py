"""Cache utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mmc.constants import CACHE_FOLDER


def read_cache(cache_folder: Path, args: str) -> dict[str, Any] | None:
    """Check if a url is cached and return the contents if it exists."""
    cache_folder.mkdir(parents=True, exist_ok=True)
    full_path = cache_folder / f"{args}.json"
    if not full_path.exists():
        return None
    with full_path.open(encoding="utf-8") as file:
        return json.load(file)


def write_cache(
    cache_data: dict[str, Any],
    cache_folder: Path,
    args: str,
) -> None:
    """Write data to a cache file."""
    cache_folder.mkdir(parents=True, exist_ok=True)
    full_path = cache_folder / f"{args}.json"
    with full_path.open("w", encoding="utf-8") as file:
        file.write(json.dumps(cache_data, indent=4))


def delete_cache() -> None:
    """Delete all files in the cache folder."""
    if CACHE_FOLDER.exists():
        for file_path in CACHE_FOLDER.iterdir():
            if file_path.is_file():
                file_path.unlink()
