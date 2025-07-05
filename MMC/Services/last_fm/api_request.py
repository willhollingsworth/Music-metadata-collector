from typing import Any

from mmc.utils.credentials import load_credentials
from mmc.utils.http_client import download_json

SERVICE_NAME = "last_fm"


def request_lookup(lookup_type: str, lookup_values: list[str]) -> dict[str, Any]:
    """Run a last.fm lookup request.

    Raises:
        TypeError: If the lookup_type is unsupported or the API response is not a dict.

    """
    credentials = load_credentials("last_fm")
    api_key = credentials["api_key"]
    last_fm_url = "http://ws.audioscrobbler.com/2.0/"

    url_mapper = {
        "track": "?method=track.getInfo&track={}&artist={}",
        "artist": "?method=artist.getInfo&artist={}",
        "album": "?method=album.getInfo&album={}&artist={}",
    }
    if lookup_type in url_mapper:
        url_format = url_mapper[lookup_type]
    else:
        msg = f"Unsupported lookup type: {lookup_type}"
        raise TypeError(msg)
    final_url = (
        last_fm_url
        + url_format.format(*lookup_values)
        + f"&api_key={api_key}&format=json"
    )
    lookup_values_str = "_".join(lookup_values)
    results = download_json(final_url)
    if not isinstance(results, dict):
        msg = (
            f"Last.fm API did not return a dict for lookup type '{lookup_type}' "
            f"with values '{lookup_values_str}'."
        )
        raise TypeError(msg)
    return results


def request_search(method: str, search: str) -> dict[str, Any]:
    """Run a last.fm search request.

    https://developer.spotify.com/documentation/web-api/reference/#/

    Raises:
        TypeError: If the API response is not a dict.

    """
    credentials = load_credentials("last_fm")
    api_key = credentials["api_key"]
    last_fm_url = "http://ws.audioscrobbler.com/2.0/"
    url_args_format = "?method={}&{}&api_key={}&format=json"
    url_args_full = url_args_format.format(method, search, api_key)
    result = download_json(last_fm_url + url_args_full)
    if not isinstance(result, dict):
        msg = f"Last.fm API did not return a dict for method '{method}' with search '{search}'."
        raise TypeError(msg)
    return result
