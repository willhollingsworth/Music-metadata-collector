"""Searches using Deezer API."""

from mmc.models import deezer_models
from mmc.types.deezer_types import DeezerEntity
from mmc.utils.http_client import download_json
from mmc.utils.list_helper import find_first_matching_dict
from mmc.utils.url_builder import ApiUrlBuilder

SERVICE_NAME = "deezer"


def search(search_type: str, search_args: list[str] | str) -> DeezerEntity:
    """Perform a search using the Deezer API.

    Args:
        search_type (str): The type of resource to search for ('track', 'artist', 'album').
        search_args (list[str] | str): The arguments for the search query.

    Returns:
        DeezerEntity: The result of the search.

    """
    full_url = ApiUrlBuilder(
        service_name=SERVICE_NAME,
        request_type="search",
        request_resource=search_type,
        url_args=search_args,
    ).full_url
    result = download_json(full_url)

    if isinstance(result, list):
        result = find_first_matching_dict(
            result,
            "type",
            search_type,
        )
    return cast_to_deezer_entity(search_type, result)


def cast_to_deezer_entity(search_type: str, result: dict[str, str]) -> DeezerEntity:
    """Cast the search result dictionary to the appropriate DeezerEntity model.

    Args:
        search_type (str): The type of entity to cast to ('track', 'artist', 'album').
        result (dict[str, str]): The dictionary containing the search result data.

    Returns:
        DeezerEntity: An instance of the corresponding DeezerEntity subclass.

    Raises:
        ValueError: If the search_type is not supported.

    """
    class_name = search_type.capitalize()
    return_class = getattr(deezer_models, class_name, None)
    if return_class is None:
        msg = f"Search type {search_type} is not supported."
        raise ValueError(msg)
    return return_class.from_dict(result)


if __name__ == "__main__":
    """Run some search examples."""

    def search_track_examples() -> None:
        """Run some search examples for tracks."""
        print("Running Deezer search examples...")
        track = "safe"
        artist = "monkey safari"
        print()
        print(f"searching {track=}, {artist=}")
        print(search("track", [track, artist]))
        print()
        track = "these things will come to be"
        artist = "DJ Seinfeld"
        print()
        print(f"searching {track=}, {artist=}")
        print(search("track", [track, artist]))
        print()

    def search_artist_examples() -> None:
        """Run some search examples for artists."""
        print("Running Deezer artist search examples...")
        artist = "Angara"
        print(f"searching {artist=}")
        print(search("artist", artist))
        artist = "Bicep"
        print()
        print(f"searching {artist=}")
        print(search("artist", artist))
        print()

    def search_album_examples() -> None:
        """Run some search examples for albums."""
        print("Running Deezer album search examples...")
        album, artist = "isles", "bicep"
        print(f"searching {album=} by {artist=}")
        print(search("album", [album, artist]))
        print()
        album, artist = "Shelby", "Ron flatter"
        print(f"searching {album=} by {artist=}")
        print(search("album", [album, artist]))
        print()

    search_track_examples()
    search_artist_examples()
    search_album_examples()
