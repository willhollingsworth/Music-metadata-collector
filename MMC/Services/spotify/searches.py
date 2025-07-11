from typing import Any

from mmc.services.spotify.api_requests import spotify_request
from mmc.services.spotify.utils import cast_to_spotify_entity
from mmc.types.types import SpotifyEntity

SERVICE_NAME = "spotify"


def search(search_type: str, search_arg: str) -> SpotifyEntity:
    """Perform a search using the Deezer API.

    Args:
        search_type (str): The type to search for ('track', 'artist', 'album').
        search_arg (list[str] | str): The arguments for the search query.

    Returns:
        DeezerEntity: The result of the search.

    Raises:
        ValueError: If no results are found for the given search_type and search_arg.

    """
    result: dict[str, Any] = spotify_request("search", search_type, search_arg)
    search_term_plural = search_type + "s"
    if search_term_plural not in result:
        msg = f"No results found for {search_type} with argument {search_arg}."
        raise ValueError(msg)
    result = result.get(search_term_plural, [])["items"][0]
    return cast_to_spotify_entity(search_type, result)


if __name__ == "__main__":
    artist_string = "pendulum"
    track_string = "watercolour"
    album_string = "in silico"
    print(f"Searching for {artist_string}")
    print(search("artist", artist_string))
    print(f"Searching for {track_string} by {artist_string}")
    print(search("track", [track_string, artist_string]))
    print(f"Searching for {album_string} by {artist_string}")
    print(search("album", [album_string, artist_string]))
