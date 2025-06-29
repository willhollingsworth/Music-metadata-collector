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
    formatted_url = f"artist/{id_value}"
    json = request_lookup(formatted_url)
    return MusicBrainzArtist.from_dict(json)


def lookup_album(id_value: str) -> MusicBrainzAlbum:
    """Lookup an album aka release by its ID."""
    formatted_url = f"release/{id_value}?inc=artists+recordings"
    json = request_lookup(formatted_url)
    return MusicBrainzAlbum.from_dict(json)


def lookup_track(id_value: str) -> MusicBrainzTrack:
    """Lookup a track aka recording by its ID."""
    formatted_url = f"recording/{id_value}?inc=artists+releases"
    json = request_lookup(formatted_url)
    return MusicBrainzTrack.from_dict(json)


if __name__ == "__main__":
    from mmc.utils.cache import delete_cache

    delete_cache()
    track_id = "a9bdcdd0-e18b-4890-8b9c-b56aaa0792ab"
    print("track lookup for: ", lookup_track(track_id))
    artist_id = "aba439cf-cc1a-412e-bb46-a5e57a24d880"
    print("artist lookup for ", lookup_artist(artist_id))
    album_id = "e73e0fa9-97d6-4c38-97a0-2d60240f3a32"
    print("album lookup for: ", lookup_album(album_id))
