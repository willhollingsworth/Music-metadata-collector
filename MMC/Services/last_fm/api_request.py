from typing import Any

from mmc.utils.credentials import load_credentials
from mmc.utils.http_client import download_json

SERVICE_NAME = "last_fm"


def request_lookup(lookup_type: str, lookup_values: list[str]) -> dict[str, Any]:
    """Run a last.fm lookup request."""
    credentials = load_credentials("last_fm")
    api_key = credentials["api_key"]
    last_fm_url = "http://ws.audioscrobbler.com/2.0/"

    # search_args = f"track={track}&artist={artist}"
    # track_response = request_lookup("track.getInfo", search_args)

    # artist_response = request_lookup("artist.getInfo", "artist=" + artist)

    # search_args = f"album={album}&artist={artist}"
    # album_response = request_lookup("album.getInfo", search_args)
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
    return download_json(final_url, SERVICE_NAME, lookup_type, lookup_values_str)


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
