"""Models for the Deezer service."""

from dataclasses import dataclass, field

from .base_models import BaseModel


@dataclass
class SpotifyTrack(BaseModel):
    """A spotify track model."""

    # TODO(Will): add support for multiple artists
    track_name: str = field(metadata={"key": "name"})
    track_id: str = field(metadata={"key": "id"})
    popularity: int = field(metadata={"key": "popularity"})
    artist_name: str = field(metadata={"key": "artists.0.name"})
    artist_id: str = field(metadata={"key": "artists.0.id"})
    album_name: str = field(metadata={"key": "album.name"})
    album_id: str = field(metadata={"key": "album.id"})


@dataclass
class SpotifyAlbum(BaseModel):
    """A spotify album model."""

    album_name: str
    album_id: int


@dataclass
class SpotifyArtist(BaseModel):
    """A spotify artist model."""

    artist_name: str
    artist_id: int
