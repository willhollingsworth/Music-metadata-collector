"""Models for the Deezer service."""

from dataclasses import dataclass, field

from .base_models import BaseModel


@dataclass
class SpotifyTrack(BaseModel):
    """A spotify track model."""

    # TODO(Will): multiple artists support
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

    # TODO(Will): add genres and multiple artists
    album_name: str = field(metadata={"key": "name"})
    album_id: int = field(metadata={"key": "id"})
    popularity: int = field(metadata={"key": "popularity"})
    artist_name: str = field(metadata={"key": "artists.0.name"})
    artist_id: int = field(metadata={"key": "artists.0.id"})
    release_date: str = field(metadata={"key": "release_date"})
    album_type: str = field(metadata={"key": "album_type"})
    track_count: int = field(metadata={"key": "tracks.total"})


@dataclass
class SpotifyArtist(BaseModel):
    """A spotify artist model."""

    artist_name: str = field(metadata={"key": "name"})
    artist_id: int = field(metadata={"key": "id"})
    followers: int = field(metadata={"key": "followers.total"})
    popularity: int = field(metadata={"key": "popularity"})
