"""Models for the Deezer service."""

from dataclasses import dataclass, field
from typing import Any, cast

from mmc.models.base_models import BaseModel

# TODO(Will): change names from Track to DeezerTrack Etc..


@dataclass
class Track(BaseModel):
    """A Deezer track model."""

    # TODO(Will): multiple artists support
    track_name: str = field(metadata={"key": "title"})
    track_id: int = field(metadata={"key": "id"})
    artist_name: str = field(metadata={"key": "artist.name"})
    artist_id: int = field(metadata={"key": "artist.id"})
    album_name: str = field(metadata={"key": "album.title"})
    album_id: int = field(metadata={"key": "album.id"})


@dataclass
class Album(BaseModel):
    """A Deezer album model."""

    # TODO(Will): multiple artists support

    album_name: str = field(metadata={"key": "title"})
    album_id: int = field(metadata={"key": "id"})
    artist_name: str = field(metadata={"key": "artist.name"})
    artist_id: int = field(metadata={"key": "artist.id"})
    track_count: int = field(metadata={"key": "nb_tracks"})
    fans: int = field(metadata={"key": "fans", "required": False})
    release_date: str = field(metadata={"key": "release_date", "required": False})
    link: str = field(metadata={"key": "link"})
    genres: list[Any] = field(metadata={"key": "genres.data", "required": False})

    def __post_init__(self) -> None:
        """Post-initialization to handle genres."""
        if self.genres:
            proceed_genres: list[str] = [
                cast("str", genre.get("name", "")) for genre in self.genres
            ]
            self.genres = proceed_genres


@dataclass
class Artist(BaseModel):
    """A Deezer artist model."""

    artist_name: str = field(metadata={"key": "name"})
    artist_id: int = field(metadata={"key": "id"})
    track_count: int = field(metadata={"key": "nb_album"})
    fans_count: int = field(metadata={"key": "nb_fan"})
    link: str = field(metadata={"key": "link"})
