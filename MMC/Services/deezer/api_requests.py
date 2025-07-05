"""Deezer API requests module."""

from typing import Any

from mmc.utils.http_client import download_json

# deezer's api docs are behind a login wall
# some public api docs https://apieco.ir/docs/deezer#api-Search-search
# also examples of use here https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py

DEEZER_API_URL = "https://api.deezer.com/"
SERVCIE_NAME = "deezer"


def request_lookup(
    request_type: str,
    id_number: str,
) -> dict[str, Any] | list[Any]:
    """Run a Deezer API lookup.

    Raises:
        TypeError: If the request_type is not supported.

    """
    request_types: dict[str, str] = {
        "album": "album/",
        "artist": "artist/",
        "track": "track/",
    }
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        raise TypeError(request_type)
    full_url = DEEZER_API_URL + request_url + id_number
    return download_json(full_url)
