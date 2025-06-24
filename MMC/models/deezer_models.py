"""Models for the Deezer service."""

# TODO(Will): Move to mmc/model
from dataclasses import dataclass, field
from typing import Any, Self, TypeVar, cast

from mmc.utils.dict_helper import get_nested

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    """Base model for Deezer data models."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create an instance of the model from a dictionary."""
        field_values = {}
        for data_field in cls.__dataclass_fields__:
            dict_key = cls.__dataclass_fields__[data_field].metadata["key"]
            dict_value = get_nested(data, dict_key)
            field_values[data_field] = dict_value
        return cls(**field_values)

    def __str__(self) -> str:
        """Return a string representation of the track."""
        return ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())


@dataclass
class Track(BaseModel):
    """A Deezer track model."""

    track_name: str = field(metadata={"key": "title"})
    track_id: int = field(metadata={"key": "id"})
    artist_name: str = field(metadata={"key": "artist.name"})
    artist_id: int = field(metadata={"key": "artist.id"})
    album_name: str = field(metadata={"key": "album.title"})
    album_id: int = field(metadata={"key": "album.id"})


@dataclass
class Album(BaseModel):
    """A Deezer album model."""

    album_name: str = field(metadata={"key": "title"})
    album_id: int = field(metadata={"key": "id"})
    artist_name: str = field(metadata={"key": "artist.name"})
    artist_id: int = field(metadata={"key": "artist.id"})
    track_count: int = field(metadata={"key": "nb_tracks"})
    fans: int = field(metadata={"key": "fans"})
    release_date: str = field(metadata={"key": "release_date"})
    link: str = field(metadata={"key": "link"})
    genres: list[Any] = field(metadata={"key": "genres.data"})

    def __post_init__(self) -> None:
        """Post-initialization to handle genres."""
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
