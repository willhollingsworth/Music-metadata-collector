"""MusicBrainz lookups for artists, albums, and tracks."""

from mmc.models.music_brainz_models import (
    MusicBrainzAlbum,
    MusicBrainzArtist,
    MusicBrainzTrack,
)
from mmc.services.music_brainz.api_requests import request_lookup


def lookup_artist(id_value: str) -> MusicBrainzArtist:
    """Lookup an artist by its ID."""
    # https://musicbrainz.org/doc/MusicBrainz_API#Lookups
    json = request_lookup("artist", id_value)
    return MusicBrainzArtist.from_dict(json)


def lookup_album(id_value: str) -> MusicBrainzAlbum:
    """Lookup an album aka release by its ID."""
    json = request_lookup("album", id_value)
    return MusicBrainzAlbum.from_dict(json)


def lookup_track(id_value: str) -> MusicBrainzTrack:
    """Lookup a track aka recording by its ID."""
    json = request_lookup("track", id_value)
    return MusicBrainzTrack.from_dict(json)


if __name__ == "__main__":
    print("Running MusicBrainz lookups module...", end="\n\n")
    track_id = "a9bdcdd0-e18b-4890-8b9c-b56aaa0792ab"
    print("track lookup for: ", track_id)
    print(lookup_track(track_id), end="\n\n")
    artist_id = "aba439cf-cc1a-412e-bb46-a5e57a24d880"
    print("artist lookup for: ", artist_id)
    print(lookup_artist(artist_id), end="\n\n")
    album_id = "e73e0fa9-97d6-4c38-97a0-2d60240f3a32"
    print("album lookup for: ", album_id)
    print(lookup_album(album_id), end="\n\n")
    print("All lookups completed")
