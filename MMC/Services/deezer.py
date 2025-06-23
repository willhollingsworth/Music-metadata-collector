"""Module to interact with Deezer's API."""

from typing import Any

from MMC.Services.deezer_models import Album, Artist, Track
from MMC.Util.http_client import download_json

# deezer's api docs are behind a login wall
# some public api docs https://apieco.ir/docs/deezer#api-Search-search
# also examples of use here https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py

DEEZER_API_URL = "https://api.deezer.com/"


def download_deezer_data(
    request_type: str,
    input_string: str,
) -> dict[str, Any] | list[Any]:
    """Download data from the Deezer API.

    Raises:
        TypeError: If the request_type is not supported.

    """
    request_types: dict[str, str] = {
        "search": "search?q=",
        "album": "album/",
        "artist": "artist/",
        "track": "track/",
    }
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        raise TypeError(request_type)
    url = DEEZER_API_URL + request_url + str(input_string)
    return download_json(url)


def build_search_args(
    search_string: str = "",
    artist: str = "",
    track: str = "",
) -> str:
    """Build the search arguments for Deezer."""
    search_items: list[str] = []
    if bool(search_string):
        search_items.append(search_string)
    if bool(artist):
        search_items.append(f'artist:"{artist}"')
    if bool(track):
        search_items.append(f'track:"{track}"')
    return " ".join(search_items)


def search_deezer(
    search_string: str = "",
    artist: str = "",
    track: str = "",
) -> dict[str, Any]:
    """Search for a track on Deezer using a string."""
    search_string_final = build_search_args(search_string, artist, track)
    search_data = download_deezer_data("search", search_string_final)
    if isinstance(search_data, list):
        search_data = search_data[0]
    return search_data


def search_track(
    search_string: str = "",
    artist: str = "",
    track: str = "",
) -> Track:
    """Search for a track on Deezer and return its details."""
    result = search_deezer(search_string, artist, track)
    return Track.from_dict(get_first_track(result))


def lookup_album(album_id: int) -> Album:
    """Lookup an album on Deezer.

    Raises:
        TypeError: If the album data is not a dictionary.

    """
    album_json = download_deezer_data("album", str(album_id))
    if not isinstance(album_json, dict):
        msg = f"Album needs to be a dict, got {type(album_json)}"
        raise TypeError(msg)
    return Album.from_dict(album_json)


def lookup_artist(artist_id: int) -> Artist:
    """Lookup an artist on Deezer.

    Raises:
        TypeError: If the artist data is not a dictionary.

    """
    artist = download_deezer_data("artist", str(artist_id))
    if not isinstance(artist, dict):
        msg = f"Artist needs to be a dict, got {type(artist)}"
        raise TypeError(msg)
    return Artist.from_dict(artist)


def lookup_track(track_id: int) -> Track:
    """Lookup a track on Deezer."""
    track = download_deezer_data("track", str(track_id))
    if isinstance(track, list):
        track = get_first_track(track)
    return Track.from_dict(track)


def lookup_track_genres(track_id: int) -> list[str]:
    """Retrieve detailed information on a track including album genres."""
    album_id = lookup_track(track_id).album_id
    return lookup_album(album_id).genres


def get_first_track(track_results: dict[str, Any] | list[Any]) -> dict[str, Any]:
    """Get the first track from a Deezer track search result.

    Raises:
        TypeError: If track_results is not a dict or list.

    """
    if isinstance(track_results, list):
        for track in track_results:
            if track["type"] == "track":
                return track
    if not isinstance(track_results, dict):
        msg = f"Expected a dict or list, got {type(track_results)}"
        raise TypeError(msg)
    return track_results


def examples() -> None:
    """Run the deezer examples."""
    print("Running Deezer examples...")
    print()
    track = "la danza"
    print("string search for track:", track, end=", result =  ")
    print(search_track(track))
    print()
    track_id = 395141722
    print("track id lookup:", track_id, end=", result =  ")
    print(lookup_track(track_id))
    print()
    print("track id lookup with genres:", track_id, end=", result =  ")
    print(lookup_track_genres(track_id))
    print()
    artist_id = 12170972
    print("artist id lookup:", artist_id, end=", result =  ")
    print(lookup_artist(artist_id))
    print()
    album_id = 46371952
    print("album id lookup:", album_id, end=", result =  ")
    album_data = lookup_album(album_id)
    print(album_data)


if __name__ == "__main__":
    # delete_cache()
    examples()
    # track_id = "395141722"
    # print("track id lookup:", track_id, end=", result =  ")
    # print(lookup_track(track_id))

    # track_id = '395141722'
    # print('track id lookup with genres:', track_id, end=", result =  ")
    # print(lookup_track_genres(track_id))

    # print('string search example:')
    # search_keys = ['title', ['artist', 'name'], [
    #     'album', 'title'], ['album', 'id'], 'type', 'id']
    # search_data = search('peking duk')
    # utility_functions.print_dict_keys(search_data[0], search_keys)

    # print('track id lookup example:')
    # track_keys = ['title', ['album', 'title'],
    #               'duration', 'rank', 'bpm', 'gain', 'id']
    # track_data = lookup_track('395141722')
    # utility_functions.print_dict_keys(track_data, track_keys)

    # print('album lookup example')
    # album_keys = ['title', ['artist', 'name'], ['artist', 'id'],
    #               'fans',  'id']
    # album_data = lookup_album('46371952', album_keys)
    # utility_functions.print_dict_keys(album_data, album_keys)
