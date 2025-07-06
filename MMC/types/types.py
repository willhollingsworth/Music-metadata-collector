"""Type alias for  entities."""

from mmc.models.deezer_models import Album, Artist, Track
from mmc.models.spotify_models import SpotifyAlbum, SpotifyArtist, SpotifyTrack

DeezerEntity = Track | Album | Artist
SpotifyEntity = SpotifyTrack | SpotifyAlbum | SpotifyArtist
