"""Last.fm API lookups for tracks, artists, and albums.

Looks are done by exact strings rather than an id
TODO(Will): add mbid lookups
"""

from mmc.models.last_fm_models import LastFmAlbum, LastFmArtist, LastFmTrack
from mmc.services.last_fm.api_request import request_lookup


def track_lookup(track: str, artist: str) -> LastFmTrack:
    """Lookup track information by track name and artist."""
    # https://www.last.fm/api/show/track.getInfo
    search_args = f"track={track}&artist={artist}"
    track_response = request_lookup("track.getInfo", search_args)
    return LastFmTrack.from_dict(track_response)


def track_lookup_mbid(mbid: str) -> LastFmTrack:
    """Lookup track information by MusicBrainz ID."""
    track_response = request_lookup("track.getInfo", f"mbid={mbid}")
    return LastFmTrack.from_dict(track_response)


def artist_lookup(artist: str) -> LastFmArtist:
    """Lookup artist information by artist name."""
    artist_response = request_lookup("artist.getInfo", "artist=" + artist)
    return LastFmArtist.from_dict(artist_response)


def album_lookup(album: str, artist: str) -> LastFmAlbum:
    """Lookup artist information by artist name."""
    search_args = f"album={album}&artist={artist}"
    album_response = request_lookup("album.getInfo", search_args)
    return LastFmAlbum.from_dict(album_response)


if __name__ == "__main__":
    track_name, artist_name = "Starlings", "NTO"
    album_name = "Starlings - Single"
    track_response = track_lookup(track_name, artist_name)
    print(f"Track Lookup for '{track_name}' by '{artist_name}':")
    print(track_response)
    print()
    artist_response = artist_lookup(artist_name)
    print(f"Artist Lookup for '{artist_name}':")
    print(artist_response)
    print()
    album_response = album_lookup(album_name, artist_name)
    print(f"Album Lookup for '{album_name}' by '{artist_name}':")
    print(album_response)
