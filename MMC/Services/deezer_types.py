"""Type alias for Deezer entities."""

from MMC.Services.deezer_models import Album, Artist, Track

DeezerEntity = Track | Album | Artist
