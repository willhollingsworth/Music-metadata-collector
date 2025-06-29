from typing import Any

from mmc.utils.credentials import load_credentials
from mmc.utils.http_client import download_json


def request_lookup(method: str, search: str) -> dict[str, Any]:
    """Run a last.fm lookup request.

    https://developer.spotify.com/documentation/web-api/reference/#/
    """
    credentials = load_credentials("last_fm")
    api_key = credentials["api_key"]
    last_fm_url = "http://ws.audioscrobbler.com/2.0/"
    url_args_format = "?method={}&{}&api_key={}&format=json"
    url_args_full = url_args_format.format(method, search, api_key)
    return download_json(last_fm_url + url_args_full)


def request_search(method: str, search: str) -> dict[str, Any]:
    """Run a last.fm search request.

    https://developer.spotify.com/documentation/web-api/reference/#/
    """
    credentials = load_credentials("last_fm")
    api_key = credentials["api_key"]
    last_fm_url = "http://ws.audioscrobbler.com/2.0/"
    url_args_format = "?method={}&{}&api_key={}&format=json"
    url_args_full = url_args_format.format(method, search, api_key)
    return download_json(last_fm_url + url_args_full)
