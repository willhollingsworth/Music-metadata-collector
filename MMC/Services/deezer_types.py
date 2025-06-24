"""Type alias for Deezer entities."""

from mmc.models.deezer_models import Album, Artist, Track

DeezerEntity = Track | Album | Artist
