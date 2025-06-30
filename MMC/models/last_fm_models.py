"""Models for the Last FM service."""

from dataclasses import dataclass, field

from mmc.models.base_models import BaseModel


@dataclass
class LastFmTrack(BaseModel):
    """A LastFm track model."""

    # TODO(Will): add support for multiple artists and albums
    track_name: str = field(metadata={"key": "track.name"})
    url: str = field(metadata={"key": "track.url"})
    artist_name: str = field(metadata={"key": "track.artist.name"})
    artist_url: str = field(metadata={"key": "track.artist.url"})
    album_name: str = field(metadata={"key": "track.album.title"})
    album_url: str = field(metadata={"key": "track.album.url"})


@dataclass
class LastFmAlbum(BaseModel):
    """A LastFm album model."""

    # TODO(Will): multiple artists support
    # TODO(Will): add track listing and track count

    album_name: str = field(metadata={"key": "album.name"})
    album_url: str = field(metadata={"key": "album.url"})
    listeners: str = field(metadata={"key": "album.listeners"})
    playcount: str = field(metadata={"key": "album.playcount"})
    artist_name: str = field(metadata={"key": "album.artist"})


@dataclass
class LastFmArtist(BaseModel):
    """A LastFm artist model."""

    # TODO(Will): add similar artists and tags
    artist_name: str = field(metadata={"key": "artist.name"})
    artist_url: str = field(metadata={"key": "artist.url"})
    listeners: int = field(metadata={"key": "artist.stats.listeners"})
    playcount: int = field(metadata={"key": "artist.stats.playcount"})
