"""Lookups for Spotify data using the Spotify API."""

from mmc.models.spotify_models import SpotifyAlbum, SpotifyArtist, SpotifyTrack
from mmc.services.spotify.api_requests import request_lookup


def lookup_track(track_id: str) -> SpotifyTrack:
    """Lookup a track on Spotify."""
    return SpotifyTrack.from_dict(request_lookup("track", track_id))


def lookup_album(album_id: str) -> SpotifyAlbum:
    """Lookup an album on Spotify."""
    return SpotifyAlbum.from_dict(request_lookup("album", album_id))


def lookup_artist(artist_id: str) -> SpotifyArtist:
    """Lookup an artist on Spotify."""
    return SpotifyArtist.from_dict(request_lookup("artist", artist_id))


if __name__ == "__main__":
    print("Running Spotify lookups...")

    track_id: str = "6xZZM6GDxTKsLjF3TNDREL"
    print("track lookup", track_id, end=": ")
    print(lookup_track(track_id))

    artist_id: str = "3tSvlEzeDnVbQJBTkIA6nO"
    print("artist lookup with id", artist_id, end=": ")
    print(lookup_artist(artist_id))

    album_id: str = "2dIGnmEIy1WZIcZCFSj6i8"
    print("album lookup with id", album_id, end=": ")
    print(lookup_album(album_id))
