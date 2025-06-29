"""Last.fm API lookups for tracks, artists, and albums.

Looks are done by exact strings rather than an id
TODO(Will): add mbid lookups
"""

from typing import Any

from mmc.services.last_fm.api_request import request_lookup


def track_lookup(track: str, artist: str) -> dict[str, Any]:
    """Lookup track information by track name and artist."""
    # https://www.last.fm/api/show/track.getInfo
    search_args = f"track={track}&artist={artist}"
    return request_lookup("track.getInfo", search_args)


def track_lookup_mbid(mbid: str) -> dict[str, Any]:
    """Lookup track information by MusicBrainz ID."""
    return request_lookup("track.getInfo", f"mbid={mbid}")


def artist_lookup(artist: str) -> dict[str, Any]:
    """Lookup artist information by artist name."""
    return request_lookup("artist.getInfo", "artist=" + artist)


def album_lookup(album: str, artist: str) -> dict[str, Any]:
    """Lookup artist information by artist name."""
    search_args = f"album={album}&artist={artist}"
    return request_lookup("album.getInfo", search_args)


if __name__ == "__main__":
    track_name, artist_name = "Starlings", "NTO"
    album_name = "Starlings - Single"
    track_response = track_lookup(track_name, artist_name)
    print(f"Track Lookup for '{track_name}' by '{artist_name}':")
    print(
        "found track:",
        track_response["track"]["name"],
        " by",
        track_response["track"]["artist"]["name"],
    )
    print(
        f"listeners: {track_response['track']['listeners']}, "
        f"playcount: {track_response['track']['playcount']}",
    )
    print()
    artist_response = artist_lookup(artist_name)
    print(f"Artist Lookup for '{artist_name}':")
    print("found artist:", artist_response["artist"]["name"])
    print(
        f"listeners: {artist_response['artist']['stats']['listeners']}, "
        f"playcount: {artist_response['artist']['stats']['playcount']}",
    )
    print()

    album_response = album_lookup(album_name, artist_name)
    print(f"Album Lookup for '{album_name}' by '{artist_name}':")
    print(
        "found album:",
        album_response["album"]["name"],
        "by",
        album_response["album"]["artist"],
    )
    print(
        f"listeners: {album_response['album']['listeners']}, "
        f"playcount: {album_response['album']['playcount']}",
    )
