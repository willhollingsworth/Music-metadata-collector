"""Models for the Deezer service."""

from dataclasses import dataclass

from MMC.models.base_models import BaseModel


@dataclass
class Album(BaseModel):
    """A spotify album model."""

    album_name: str
    album_id: int


@dataclass
class Artist(BaseModel):
    """A spotify artist model."""

    artist_name: str
    artist_id: int
