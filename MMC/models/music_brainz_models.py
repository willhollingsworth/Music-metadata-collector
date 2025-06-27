"""Models for the MusicBrainz service."""

from dataclasses import dataclass, field

from mmc.models.base_models import BaseModel


@dataclass
class MusicBrainzTrack(BaseModel):
    """A MusicBrainz track model."""

    # TODO(Will): add support for multiple artists and albums, currently just grabs first one
    track_name: str = field(metadata={"key": "title"})
    track_id: str = field(metadata={"key": "id"})
    artist_name: str = field(metadata={"key": "artist-credit.0.artist.name"})
    artist_id: str = field(metadata={"key": "artist-credit.0.artist.id"})
    album_name: str = field(metadata={"key": "releases.0.title"})
    album_id: str = field(metadata={"key": "releases.0.id"})


@dataclass
class MusicBrainzAlbum(BaseModel):
    """A MusicBrainz album model."""

    # TODO(Will): multiple artists support
    # TODO(Will): add track listing on media.0.tracks.xx.title

    album_name: str = field(metadata={"key": "title"})
    album_id: int = field(metadata={"key": "id"})
    status: str = field(metadata={"key": "status"})
    artist_name: str = field(metadata={"key": "artist-credit.0.artist.name"})
    artist_id: int = field(metadata={"key": "artist-credit.0.artist.id"})
    track_count: int = field(metadata={"key": "media.0.track-count"})


@dataclass
class MusicBrainzArtist(BaseModel):
    """A MusicBrainz artist model."""

    artist_name: str = field(metadata={"key": "name"})
    artist_id: int = field(metadata={"key": "id"})
    type: str = field(metadata={"key": "type"})
