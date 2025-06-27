"""Searches using Deezer API."""

from typing import Any

from mmc.models.deezer_models import Track
from mmc.services.deezer.api_requests import request_search
from mmc.services.deezer.utils import get_first_track


def build_search_args(
    search_string: str = "",
    artist: str = "",
    track: str = "",
) -> str:
    """Build the search arguments for Deezer."""
    search_items: list[str] = []
    if bool(search_string):
        search_items.append(search_string)
    if bool(artist):
        search_items.append(f'artist:"{artist}"')
    if bool(track):
        search_items.append(f'track:"{track}"')
    return " ".join(search_items)


def search_deezer(
    search_string: str = "",
    artist: str = "",
    track: str = "",
) -> dict[str, Any]:
    """Search for a track on Deezer using a string.

    Raises:
        TypeError: If the search result is not a dictionary.

    """
    search_string_final = build_search_args(search_string, artist, track)
    search_data = request_search(search_string_final)
    if isinstance(search_data, list):
        search_data = search_data[0]
    if isinstance(search_data, dict):
        return search_data
    msg = f"Expected a dict, got {type(search_data)}"
    raise TypeError(msg)


def search_track(
    search_string: str = "",
    artist: str = "",
    track: str = "",
) -> Track:
    """Search for a track on Deezer and return its details."""
    result = search_deezer(search_string, artist, track)
    return Track.from_dict(get_first_track(result))


if __name__ == "__main__":
    """Run the deezer examples."""
    print("Running Deezer examples...")
    print()
    track = "la danza"
    print("string search for track:", track, end=", result =  ")
    print(search_track(track))
    print()
