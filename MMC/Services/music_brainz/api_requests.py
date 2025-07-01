"""MusicBrainz API requests."""

from typing import Any

from mmc.constants import MUSIC_BRAINZ_API_URL
from mmc.utils.http_client import download_json

SERVCIE_NAME = "music_brainz"


def request_lookup(request_type: str, id_value: str) -> dict[str, Any]:
    """Run a MusicBrainz API lookup.

    Raises:
        ValueError: If the MusicBrainz API returns an error.

    """
    url_mapper = {
        "artist": f"artist/{id_value}?fmt=json",
        "track": f"recording/{id_value}?inc=artists+releases&fmt=json",
        "album": f"release/{id_value}?inc=artists+recordings&fmt=json",
    }

    formatted_url = f"{MUSIC_BRAINZ_API_URL}{url_mapper[request_type]}"
    response = download_json(formatted_url, SERVCIE_NAME, request_type, id_value)
    if "error" in response:
        msg = f"error on url arg: {formatted_url}, msg: {response['error']}"
        raise ValueError(msg)
    return response


def request_search(url_args: str) -> dict[str, Any]:
    """Run a MusicBrainz API search."""
    separator = "&" if "?" in url_args else "?"
    formatted_url = f"{MUSIC_BRAINZ_API_URL}{url_args}{separator}fmt=json"
    return download_json(formatted_url)
