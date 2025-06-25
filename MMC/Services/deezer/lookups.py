"""Lookup functions for Deezer API."""

from mmc.models.deezer_models import Album, Artist, Track
from mmc.services.deezer.api_requests import download_deezer_data


def lookup_album(album_id: int) -> Album:
    """Lookup an album on Deezer.

    Raises:
        TypeError: If the album data is not a dictionary.

    """
    json = download_deezer_data("album", str(album_id))
    if not isinstance(json, dict):
        msg = f"Album needs to be a dict, got {type(json)}"
        raise TypeError(msg)
    return Album.from_dict(json)


def lookup_artist(artist_id: int) -> Artist:
    """Lookup an artist on Deezer.

    Raises:
        TypeError: If the artist data is not a dictionary.

    """
    json = download_deezer_data("artist", str(artist_id))
    if not isinstance(json, dict):
        msg = f"Artist needs to be a dict, got {type(json)}"
        raise TypeError(msg)
    return Artist.from_dict(json)


def lookup_track(track_id: int) -> Track:
    """Lookup a track on Deezer.

    Raises:
        TypeError: If the track data is not a dictionary.

    """
    json = download_deezer_data("track", str(track_id))
    if not isinstance(json, dict):
        msg = f"track needs to be a dict, got {type(json)}"
        raise TypeError(msg)
    return Track.from_dict(json)


def lookup_track_genres(track_id: int) -> list[str]:
    """Retrieve detailed information on a track including album genres."""
    album_id = lookup_track(track_id).album_id
    return lookup_album(album_id).genres


def lookup_artist_genres(artist_id: int) -> list[str]:
    """Retrieve detailed information on an artist including genres."""
    "TODO: Implement this function to retrieve artist genres."


if __name__ == "__main__":
    track_id = 395141722
    print("track id lookup:", track_id)
    print(lookup_track(track_id))
    print()
    print("track id lookup with genres:", track_id)
    print(lookup_track_genres(track_id))
    print()
    artist_id = 12170972
    print("artist id lookup:", artist_id)
    print(lookup_artist(artist_id))
    print()
    album_id = 46371952
    print("album id lookup:", album_id)
    album_data = lookup_album(album_id)
    print(album_data)
