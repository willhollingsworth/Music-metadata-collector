"""Module to interact with Deezer's API."""
from typing import Any

from MMC.Util.cache import delete_cache
from MMC.Util.debug import print_dict_keys
from MMC.Util.http_client import download_json
from MMC.Util.dict_helper import map_dict_keys

# deezer's api docs are behind a login wall
# some public api docs https://apieco.ir/docs/deezer#api-Search-search
# also examples of use here https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py

DEEZER_API_URL = "https://api.deezer.com/"


class InvalidRequestType(Exception):
    """Exception raised for invalid request types."""


def download_deezer_data(
    request_type: str, input_string: str
) -> dict[str, Any] | list[Any]:
    """Download data from the Deezer API."""
    request_types: dict[str, str] = {
        'search': 'search?q=',
        'album': 'album/',
        'artist': 'artist/',
        'track': 'track/',
        }
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        raise InvalidRequestType(request_type)
    url = DEEZER_API_URL + request_url + str(input_string)
    return download_json(url)


def build_search_args(
        search_string: str = '',
        artist: str = '',
        track: str = '',
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
    search_string: str = '',
    artist: str = '',
    track: str = '',
    ) -> dict[str, Any]:
    """Search for a track on Deezer using a string."""
    search_string_final = build_search_args(search_string, artist, track)
    search_data = download_deezer_data('search', search_string_final)
    if isinstance(search_data, list):
        search_data = search_data[0]
    return search_data


def search_track(
    search_string: str = '',
    artist: str = '',
    track: str = '',
    ) -> dict[str, str]:
    """Search for a track on Deezer and return its details."""
    result = search_deezer(search_string, artist, track)
    result = format_track_details(result)
    return result


def lookup_album(album_id: str) -> dict[str, str | list[str]]:
    """Lookup an album on Deezer."""
    album_json = download_deezer_data('album', album_id)
    album = format_album_details(album_json)
    return album


def lookup_artist(artist_id: str) -> dict[str, Any]:
    """Lookup an artist on Deezer."""
    return download_deezer_data('artist', artist_id)


def lookup_track(track_id: str) -> dict[str, str]:
    """Lookup a track on Deezer."""
    track = download_deezer_data('track', track_id)
    if isinstance(track, list):
        track = get_first_track(track)
    track = format_track_details(track)
    return track


def lookup_track_genres(track_id: str, print_results: bool = False) -> dict[str, str]:
    """Retrieve detailed information on a track including album genres."""
    output_dict: dict[str, str] = {}
    output_dict = lookup_track(track_id)
    album_results = lookup_album(output_dict['album id'])
    output_dict['album genres'] = ', '.join([genre['name']
                                   for genre in album_results['genres']['data']])
    return output_dict


def get_first_track(track_results: dict[str, Any] | list[Any]) -> dict[str, Any]:
    """Get the first track from a Deezer track search result."""
    if isinstance(track_results, list):
        for track in track_results:
            if track['type'] == 'track':
                return track
    return track_results


def format_track_details(track_results: dict[str, Any]) -> dict[str, str]:
    """Format track details from a Deezer track search result."""
    output_dict: dict[str, str] = {}
    track_results = get_first_track(track_results)
    output_dict = map_dict_keys(
        track_results,
        [
            ('track name', 'title'),
            ('track id', 'id'),
            ('artist name', ['artist', 'name']),
            ('artist id', ['artist', 'id']),
            ('album name', ['album', 'title']),
            ('album id', ['album', 'id']),
        ])
    return output_dict

def format_album_details(track_results: dict[str, Any]) -> dict[str, str | list[str]]:
    """Format track details from a Deezer track search result."""
    output_dict = {}
    track_results = get_first_track(track_results)
    output_dict = map_dict_keys(
        track_results,
        [
            ('album name', 'title'),
            ('album id', 'id'),
            ('artist name', ['artist', 'name']),
            ('artist id', ['artist', 'id']),
            ('track count', 'nb_tracks'),
            ('fans', 'fans'),
            ('release date', 'release_date'),
            ('link', 'link'),
        ])
    output_dict['genres'] = [genre['name'] for genre in track_results['genres']['data']]
    return output_dict


def examples() -> None:
    """Run the deezer examples."""
    print('Running Deezer examples...')
    print()
    track = 'la danza'
    print('string search for track:', track, end=", result =  ")
    print(search_track(track))
    print()
    track_id = '395141722'
    print('track id lookup:', track_id, end=", result =  ")
    print(lookup_track(track_id))
    print()
    print('track id lookup with genres:', track_id, end=", result =  ")
    print(lookup_track_genres(track_id))
    print()
    artist_id = '12170972'
    print('artist id lookup:', artist_id, end=", result =  ")
    print(lookup_artist(artist_id))
    print()
    album_id = '46371952'
    print('album id lookup:', album_id, end=", result =  ")
    album_data = lookup_album(album_id)
    print_dict_keys(album_data, ['title', ['artist', 'name'], ['artist', 'id'],
                    'fans', 'id'])


if __name__ == '__main__':
    # delete_cache()
    examples()

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
