"""Models for the Deezer service."""

from dataclasses import dataclass
from typing import Any

from MMC.Util.dict_helper import get_nested


@dataclass
class Track:
    """A Deezer track model."""

    track_name: str
    track_id: int
    artist_name: str
    artist_id: int
    album_name: str
    album_id: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Track":
        """Create a Track instance from a dictionary."""
        fields: list[tuple[str, str | list[str], type]] = [
            ("track_name", "title", str),
            ("track_id", "id", int),
            ("artist_name", ["artist", "name"], str),
            ("artist_id", ["artist", "id"], int),
            ("album_name", ["album", "title"], str),
            ("album_id", ["album", "id"], int),
        ]
        values = {name: caster(get_nested(data, key)) for name, key, caster in fields}
        return cls(**values)


@dataclass
class Album:
    """A Deezer album model."""

    album_name: str
    album_id: int
    artist_name: str
    artist_name: str
    artist_id: int
    track_count: int
    fans: int
    release_date: str
    link: str
    genres: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Album":
        """Create a album instance from a dictionary."""
        fields: list[tuple[str, str | list[str], type]] = [
            ("album_name", "title", str),
            ("album_id", "id", int),
            ("artist_name", ["artist", "name"], str),
            ("artist_id", ["artist", "id"], int),
            ("track_count", "nb_tracks", int),
            ("fans", "fans", int),
            ("release_date", "release_date", str),
            ("link", "link", str),
            ("genres", ["genres", "data"], list),
        ]
        values = {name: caster(get_nested(data, key)) for name, key, caster in fields}
        values["genres"] = [genre["name"] for genre in values["genres"]]
        return cls(**values)


@dataclass
class Artist:
    """A Deezer artist model."""

    artist_name: str
    artist_id: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Artist":
        """Create an Artist instance from a dictionary."""
        fields: list[tuple[str, str | list[str], type]] = [
            ("artist_name", "name", str),
            ("artist_id", "id", int),
        ]
        values = {name: caster(get_nested(data, key)) for name, key, caster in fields}
        return cls(**values)
