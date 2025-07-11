"""Music Metadata Collector (mmc) package."""

from mmc.services.deezer.lookups import lookup_album as deezer_lookup_album
from mmc.services.deezer.lookups import lookup_artist as deezer_lookup_artist
from mmc.services.deezer.lookups import lookup_track as deezer_lookup_track
from mmc.services.last_fm.lookups import lookup_album as last_fm_lookup_album
from mmc.services.last_fm.lookups import lookup_artist as last_fm_lookup_artist
from mmc.services.last_fm.lookups import lookup_track as last_fm_lookup_track
from mmc.services.music_brainz.lookups import lookup_album as music_brainz_lookup_album
from mmc.services.music_brainz.lookups import (
    lookup_artist as music_brainz_lookup_artist,
)
from mmc.services.music_brainz.lookups import lookup_track as music_brainz_lookup_track
from mmc.services.spotify.lookups import lookup_album as spotify_lookup_album
from mmc.services.spotify.lookups import lookup_artist as spotify_lookup_artist
from mmc.services.spotify.lookups import lookup_track as spotify_lookup_track
from mmc.services.spotify.status import current_playing as spotify_current_playing
from mmc.services.spotify.searches import search as spotify_search
from mmc.services.deezer.searches import search as deezer_search
from mmc.utils.cache import delete_cache

__all__ = [
    "deezer_lookup_album",
    "deezer_lookup_artist",
    "deezer_lookup_track",
    "delete_cache",
    "last_fm_lookup_album",
    "last_fm_lookup_artist",
    "last_fm_lookup_track",
    "music_brainz_lookup_album",
    "music_brainz_lookup_artist",
    "music_brainz_lookup_track",
    "spotify_current_playing",
    "spotify_lookup_album",
    "spotify_lookup_artist",
    "spotify_lookup_track",
    "spotify_search",
    "deezer_search",
]
