from typing import Any

import requests

from mmc.constants import SPOTIFY_API_URL, SPOTIFY_AUTH_URL
from mmc.utils.credentials import load_credentials
from mmc.utils.http_client import download_json


def create_client_headers() -> dict[str, str]:
    """Create headers for spotify api requests."""
    credentials = load_credentials("spotify")
    # generate auth token and headers
    # POST
    auth_response = requests.post(
        SPOTIFY_AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"],
        },
    )
    # convert the response to JSON
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data["access_token"]
    return {
        "Authorization": f"Bearer {access_token}",
    }


def lookup_data(request_type: str, input_value: str) -> dict[str, Any]:
    """Lookup data from the Spotify API."""
    headers = create_client_headers()
    request_types = {
        "artists": "artists/",
        "albums": "albums/",
        "tracks": "tracks/",
    }
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        msg = f"wrong type selected, {request_type} is not allowed"
        raise TypeError(msg)
    full_url = SPOTIFY_API_URL + request_url + input_value
    return download_json(full_url, headers)


def search_data(
    request_type: str,
    input_value: str | dict[str, str],
) -> dict[str, Any]:
    """Download data from the Spotify API."""
    # https://developer.spotify.com/documentation/web-api/reference/#/
    headers = create_client_headers()
    request_types = {
        "artists": "artists/",
        "albums": "albums/",
        "tracks": "tracks/",
    }
    valid_search_types = ["artist", "track", "album", "genre"]
    if request_type in request_types:
        request_url = request_types[request_type]
    elif request_type.split("_")[0] == "search":
        search_type = request_type.split("_")[1]
        if search_type in valid_search_types:
            request_url = f"search?type={search_type}&q={search_type}:"
        else:
            raise Exception(
                "wrong search selected, only the following are valid",
                valid_search_types,
                locals(),
            )
    else:
        raise Exception("wrong type selected", locals())
    processed_input = ""
    if isinstance(input_value, dict):
        for key in input_value:
            if key == search_type:
                processed_input += input_value[key]
            else:
                processed_input += "&" + key + ":" + input_value[key]
    else:
        processed_input = input_value

    full_url = SPOTIFY_API_URL + request_url + processed_input
    return download_json(full_url, headers)


if __name__ == "__main__":
    print("Running Spotify API requests module...")
    track_id = "6xZZM6GDxTKsLjF3TNDREL"
    api_response = lookup_data("tracks", track_id)
    print("API response for track lookup:", api_response)
