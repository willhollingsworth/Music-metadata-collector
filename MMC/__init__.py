"""Music Metadata Collector (mmc) package."""

from mmc.services.deezer.lookups import lookup_album as deezer_lookup_album
from mmc.services.deezer.lookups import lookup_artist as deezer_lookup_artist
from mmc.services.deezer.lookups import lookup_track as deezer_lookup_track
from mmc.services.spotify.lookups import lookup_album as spotify_lookup_album
from mmc.services.spotify.lookups import lookup_artist as spotify_lookup_artist
from mmc.services.spotify.lookups import lookup_track as spotify_lookup_track
from mmc.services.spotify.status import current_playing as spotify_current_playing
from mmc.utils.cache import delete_cache

__all__ = [
    "deezer_lookup_album",
    "deezer_lookup_artist",
    "deezer_lookup_track",
    "delete_cache",
    "spotify_current_playing",
    "spotify_lookup_album",
    "spotify_lookup_artist",
    "spotify_lookup_track",
]
