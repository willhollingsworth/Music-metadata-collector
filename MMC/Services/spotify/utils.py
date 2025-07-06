"""Utils for Spotify."""

from mmc.models import spotify_models
from mmc.types.types import SpotifyEntity

SERVICE_NAME = "spotify"


def cast_to_spotify_entity(search_type: str, result: dict[str, str]) -> SpotifyEntity:
    """Cast the search result dictionary to the appropriate Spotify model.

    Args:
        search_type (str): The type of entity to cast to ('track', 'artist', 'album').
        result (dict[str, str]): The dictionary containing the search result data.

    Returns:
        Spotify model.: An instance of the corresponding Spotify model.

    Raises:
        ValueError: If the search_type is not supported.

    """
    class_name = SERVICE_NAME.capitalize() + search_type.capitalize()
    return_class = getattr(spotify_models, class_name, None)
    if return_class is None:
        msg = f"Search type {search_type} is not supported."
        raise ValueError(msg)
    return return_class.from_dict(result)
