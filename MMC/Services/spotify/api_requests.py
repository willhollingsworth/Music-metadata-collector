"""Spotify API Requests."""

from typing import Any

import requests

from mmc.constants import SPOTIFY_AUTH_URL
from mmc.utils.credentials import load_credentials
from mmc.utils.http_client import download_json
from mmc.utils.url_builder import ApiUrlBuilder

SERVCIE_NAME = "spotify"


def create_client_headers() -> dict[str, str]:
    """Create headers for spotify api requests."""
    credentials = load_credentials("spotify")
    auth_response = requests.post(
        SPOTIFY_AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"],
        },
    )
    auth_response_data = auth_response.json()
    access_token = auth_response_data["access_token"]
    return {
        "Authorization": f"Bearer {access_token}",
    }


def request_lookup(request_type: str, request_args: str) -> dict[str, Any]:
    """Redirect to universal request function."""
    return spotify_request("lookup", request_type, request_args)


def spotify_request(
    request_type: str,
    resource_type: str,
    request_args: str | list[str],
) -> dict[str, Any]:
    """Lookup data from the Spotify API.

    Args:
        request_type (str): The type of request to make (search or lookup).
        resource_type (str): The type of resource to lookup (artist, album, track).
        request_args (str): The ID to lookup.

    Raises:
        TypeError: If the request_type is not valid.
        ValueError: If no data is found for the given request_args.

    """
    headers = create_client_headers()
    full_url = ApiUrlBuilder(
        SERVCIE_NAME,
        request_type,
        resource_type,
        request_args,
    ).full_url
    result = download_json(full_url, headers)
    if not result:
        msg = f"No data found for {request_type}:{resource_type} with ID {request_args}"
        raise ValueError(msg)
    if isinstance(result, list):
        msg = (
            f"Multiple results found for {request_type}:{resource_type} "
            f"with ID {request_args}"
        )
        raise TypeError(msg)
    if "error" in result:
        error_message = result["error"].get("message", "Unknown error")
        msg = f"Error from Spotify API: {error_message}"
        raise ValueError(msg)
    return result


if __name__ == "__main__":
    print("Running Spotify API requests module...")
    track_id = "6xZZM6GDxTKsLjF3TNDREL"
    api_response = request_lookup("track", track_id)
    print("API response for track lookup:", api_response)
