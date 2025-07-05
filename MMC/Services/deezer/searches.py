"""Searches using Deezer API."""

from mmc.constants import DEEZER_API_URL
from mmc.models import deezer_models
from mmc.types.deezer_types import DeezerEntity
from mmc.utils.http_client import download_json
from mmc.utils.list_helper import find_first_matching_dict

SERVICE_NAME = "deezer"


class Search:
    """Performs searches using the Deezer API for tracks, artists, or albums."""

    def __init__(
        self,
        search_type: str = "",
        artist: str = "",
        track: str = "",
        album: str = "",
    ) -> None:
        """Initialize the search with the given parameters."""
        self.search_type = search_type
        self.artist = artist
        self.track = track
        self.album = album
        self.service_name = SERVICE_NAME
        self.search_args = self.build_search_args()
        self.search_url = self.build_search_url()

    def build_search_args(self) -> None:
        """Build the search arguments for Deezer."""
        search_items: list[str] = []
        if self.artist:
            search_items.append(f'artist:"{self.artist}"')
        if self.track:
            search_items.append(f'track:"{self.track}"')
        if self.album:
            search_items.append(f'album:"{self.album}"')
        self.search_string = " ".join(search_items)

    def build_search_url(self) -> str:
        """Build the search URL for Deezer."""
        search_url_entries = [
            DEEZER_API_URL,
            f"search/{self.search_type}?q=",
            self.search_string,
        ]

        return "".join(search_url_entries)

    def run(self) -> DeezerEntity:
        """Run the search and return the results.

        Raises:
            ValueError: If the search type is not supported.

        """
        result = download_json(self.search_url)

        if isinstance(result, list):
            result = find_first_matching_dict(
                result,
                "type",
                self.search_type,
            )
        class_name = self.search_type.capitalize()
        return_class = getattr(deezer_models, class_name, None)
        if return_class is not None:
            return return_class.from_dict(result)
        msg = f"Search type {self.search_type} is not supported."
        raise ValueError(msg)


def search_track_examples() -> None:
    """Run some search examples."""
    print("Running Deezer search examples...")
    track = "no freedom"
    print(f"searching {track=}")
    print(Search(search_type="track", track=track).run())
    artist = "angara"
    print()
    print(f"searching {track=}, {artist=}")
    print(Search(search_type="track", track=track, artist=artist).run())
    print()
    album = "prove"
    print(f"searching {track=}, {album=}")
    print(Search(search_type="track", track=track, album=album).run())
    print()


def search_artist_examples() -> None:
    """Run some search examples for artists."""
    print("Running Deezer artist search examples...")
    artist = "angara"
    print(f"searching {artist=}")
    print(Search(search_type="artist", artist=artist).run())
    artist = "funkin matt"
    print()
    print(f"searching {artist=}")
    print(Search(search_type="artist", artist=artist).run())
    print()


def search_album_examples() -> None:
    """Run some search examples for albums."""
    print("Running Deezer album search examples...")
    album, artist = "isles", "bicep"
    print(f"searching {album=} by {artist=}")
    print(Search(search_type="album", album=album, artist=artist).run())
    print()
    album, artist = "shelby", "ron flatter"
    print(f"searching {album=} by {artist=}")
    print(Search(search_type="album", album=album, artist=artist).run())
    print()


if __name__ == "__main__":
    search_track_examples()
    search_artist_examples()
    search_album_examples()
