"""MusicBrainz API requests."""

from typing import Any

from mmc.constants import MUSIC_BRAINZ_API_URL
from mmc.utils.http_client import download_json


def request_lookup(url_args: str) -> dict[str, Any]:
    """Run a MusicBrainz API lookup.

    Raises:
        ValueError: If the MusicBrainz API returns an error.

    """
    separator = "&" if "?" in url_args else "?"
    formatted_url = f"{MUSIC_BRAINZ_API_URL}{url_args}{separator}fmt=json"
    response = download_json(formatted_url)
    if "error" in response:
        msg = f"error on url arg: {url_args}, msg: {response['error']}"
        raise ValueError(msg)
    return response


def request_search(url_args: str) -> dict[str, Any]:
    """Run a MusicBrainz API search."""
    separator = "&" if "?" in url_args else "?"
    formatted_url = f"{MUSIC_BRAINZ_API_URL}{url_args}{separator}fmt=json"
    return download_json(formatted_url)
