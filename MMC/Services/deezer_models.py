"""Models for the Deezer service."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Track:
    """A Deezer track model."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize a Track instance from a dictionary."""
        self.track_name: str = data["title"]
        self.track_id: int = data["id"]
        self.artist_name: str = data["artist"]["name"]
        self.artist_id: int = data["artist"]["id"]
        self.album_name: str = data["album"]["title"]
        self.album_id: int = data["album"]["id"]

    def __str__(self) -> str:
        """Return a string representation of the track."""
        return ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())


@dataclass
class Album:
    """A Deezer album model."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize a album instance from a dictionary."""
        self.album_name: str = data["title"]
        self.album_id: int = data["id"]
        self.artist_name: str = data["artist"]["name"]
        self.artist_id: int = data["artist"]["id"]
        self.track_count: int = data["nb_tracks"]
        self.fans: int = data["fans"]
        self.release_date: str = data["release_date"]
        self.link: str = data["link"]
        self.genres: list[str] = [
            genre["name"] for genre in data.get("genres", {}).get("data", [])
        ]

    def __str__(self) -> str:
        """Return a string representation of the album."""
        return ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())


@dataclass
class Artist:
    """A Deezer artist model."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize a artist instance from a dictionary."""
        self.artist_name: str = data["name"]
        self.artist_id: int = data["id"]
        self.track_count: int = data["nb_album"]
        self.fans_count: int = data["nb_fan"]
        self.link: str = data["link"]

    def __str__(self) -> str:
        """Return a string representation of the artist."""
        return ", ".join(f"{k}:{v}" for k, v in self.__dict__.items())
