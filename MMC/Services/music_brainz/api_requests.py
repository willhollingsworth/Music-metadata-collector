"""MusicBrainz API requests."""

from typing import Any

from mmc.constants import MUSIC_BRAINZ_API_URL
from mmc.utils.http_client import download_json
from mmc.utils.url_builder import ApiUrlBuilder

SERVCIE_NAME = "music_brainz"


def request_lookup(request_type: str, id_value: str) -> dict[str, Any]:
    """Run a MusicBrainz API lookup.

    Raises:
        TypeError: If the response is not a dictionary.
        ValueError: If the MusicBrainz API returns an error.

    """
    full_url = ApiUrlBuilder(
        SERVCIE_NAME,
        "lookup",
        request_type,
        id_value,
    ).full_url
    response = download_json(full_url)
    if not isinstance(response, dict):
        msg = f"Expected dict response, got {type(response).__name__}: {response}"
        raise TypeError(msg)
    if "error" in response:
        msg = f"error on url arg: {full_url}, msg: {response.get('error')}"
        raise ValueError(msg)
    return response


def request_search(url_args: str) -> dict[str, Any]:
    """Run a MusicBrainz API search.

    Raises:
        TypeError: If the response is not a dictionary.

    """
    separator = "&" if "?" in url_args else "?"
    formatted_url = f"{MUSIC_BRAINZ_API_URL}{url_args}{separator}fmt=json"
    response = download_json(formatted_url)
    if not isinstance(response, dict):
        msg = f"Expected dict response, got {type(response).__name__}: {response}"
        raise TypeError(msg)
    return response
