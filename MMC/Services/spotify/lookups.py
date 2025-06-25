"""Lookups for Spotify data using the Spotify API."""

from typing import Any

from mmc.models.spotify_models import SpotifyAlbum, SpotifyArtist, SpotifyTrack
from mmc.services.spotify.api_requests import lookup_data


def lookup_track(track_id: str) -> SpotifyTrack:
    """Lookup a track on Spotify."""
    results = lookup_data("tracks", track_id)
    # print_dict_keys(results, ["name", ["artists", 0, "name"], "popularity"])
    return SpotifyTrack.from_dict(results)


def lookup_album(album_id: str) -> SpotifyAlbum:
    """Lookup an album on Spotify."""
    # print_dict_keys(results, ["name", "genres", "uri"])
    return SpotifyAlbum.from_dict(lookup_data("albums", album_id))


def lookup_artist(artist_id: str) -> SpotifyArtist:
    """Lookup an artist on Spotify."""
    # print_dict_keys(results, ["name", ["followers", "total"], "genres"])
    return SpotifyArtist.from_dict(lookup_data("artists", artist_id))


def lookup_track_detailed(id: str) -> dict[str, Any]:
    """Lookup a track on Spotify with detailed information."""
    output_dict = {}
    track = lookup_track(id)
    output_dict["track name"] = track["name"]
    output_dict["track type"] = track["type"]
    output_dict["track id"] = track["id"]
    if isinstance(track["artists"], list):
        output_dict["artist name"] = track["artists"][0]["name"]
        output_dict["artist id"] = track["artists"][0]["id"]
    else:
        output_dict["artist name"] = track["artists"]
        output_dict["artist id"] = track["artists"]
    output_dict["album name"] = track["album"]["name"]
    output_dict["album id"] = track["album"]["id"]
    artist_results = lookup_artist(output_dict["artist id"])
    output_dict["artist genres"] = artist_results["genres"]
    #     ["track name", "artist name", "album name", "artist genres"],
    return output_dict


if __name__ == "__main__":
    print("Running Spotify lookups...")

    track_id: str = "6xZZM6GDxTKsLjF3TNDREL"
    print("track lookup", track_id, end=": ")
    print(lookup_track(track_id))

    # artist_id: str = "3tSvlEzeDnVbQJBTkIA6nO"
    # print("artist lookup with id", artist_id, end=": ")
    # print(lookup_artist(artist_id))

    # album_id: str = "2dIGnmEIy1WZIcZCFSj6i8"
    # print("album lookup with id", album_id, end=": ")
    # print(lookup_album(album_id))

    # print("detailed track lookup", end=": ")
    # print(lookup_track_detailed(track_id))
