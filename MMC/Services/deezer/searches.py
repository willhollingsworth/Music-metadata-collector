"""Searches using Deezer API."""

from mmc.constants import DEEZER_API_URL
from mmc.models.deezer_models import Track
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
        self.search_url = self.build_search_url()

    def build_search_url(self) -> None:
        """Build the search arguments for Deezer."""
        search_items: list[str] = []
        if self.artist:
            search_items.append(f'artist:"{self.artist}"')
        if self.track:
            search_items.append(f'track:"{self.track}"')
        if self.album:
            search_items.append(f'album:"{self.album}"')
        self.search_string = " ".join(search_items)

    def run(self) -> Track:
        """Run the search and return the results.

        Raises:
            ValueError: If the search type is not supported.

        """
        search_url = DEEZER_API_URL + "search?q=" + self.search_string
        result = download_json(search_url, SERVICE_NAME, "search", self.search_string)
        if isinstance(result, list):
            result = find_first_matching_dict(
                result,
                "type",
                self.search_type,
            )
        if self.search_type == "track":
            return Track.from_dict(result)
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


if __name__ == "__main__":
    search_track_examples()
