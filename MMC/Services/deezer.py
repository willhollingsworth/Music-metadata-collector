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
    ) -> dict[str, Any]:
    """Search for a track on Deezer and return its details."""
    output_dict: dict[str, Any] = {}
    result = search_deezer(search_string, artist, track)
    output_dict['track name'] = result['title']
    output_dict['track id'] = result['id']
    output_dict['artist name'] = result['artist']['name']
    output_dict['artist id'] = result['artist']['id']
    output_dict['album name'] = result['album']['title']
    output_dict['album id'] = result['album']['id']
    return output_dict


def lookup_album(album_id: str) -> dict[str, Any]:
    """Lookup an album on Deezer."""
    return download_deezer_data('album', album_id)


def lookup_artist(artist_id: str) -> dict[str, Any]:
    """Lookup an artist on Deezer."""
    return download_deezer_data('artist', artist_id)


def lookup_track(track_id: str) -> dict[str, Any]:
    """Lookup a track on Deezer."""
    return download_deezer_data('track', track_id)


def lookup_track_detailed(track_id: str, print_results: bool = False) -> dict[str, Any]:
    """Retrieve detailed information about a track from Deezer."""
    output_dict: dict[str, str] = {}
    track = lookup_track(track_id)
    if isinstance(track, list):
        for t in track:
            if t['type'] == 'track':
                track = t
                break
    output_dict = map_dict_keys(
        track,
        [
            ('track name', 'title'),
            ('track id', 'id'),
            ('artist name', ['artist', 'name']),
            ('artist id', ['artist', 'id']),
            ('album name', ['album', 'title']),
            ('album id', ['album', 'id']),
        ])
    album_results = lookup_album(output_dict['album id'])
    output_dict['album genres'] = ', '.join([genre['name']
                                   for genre in album_results['genres']['data']])
    if print_results:
        print_dict_keys(output_dict)
    return output_dict


def format_track_details(track_results: dict[str, Any]) -> dict[str, str]:
    """Format track details from a Deezer track search result."""
    output_dict: dict[str, str] = {}
    if isinstance(track_results, list):
        for track in track_results:
            if track['type'] == 'track':
                track_results = track
                break
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
    album_results = lookup_album(output_dict['album id'])
    output_dict['album genres'] = ', '.join([genre['name']
                                   for genre in album_results['genres']['data']])
    return output_dict


def examples() -> None:
    """Run the deezer examples."""
    track = 'la danza'

    print('string search for track:', track, end=", result =  ")
    track_data = search_deezer(track)
    better_format = format_track_details(track_data)
    print_dict_keys(better_format)

    track_id = '395141722'
    print('track id lookup:', track_id, end=", result =  ")
    track_data = lookup_track(track_id)
    print_dict_keys(track_data, ['title', ['album', 'title'],
                    'duration', 'rank', 'bpm', 'gain', 'id'])

    album_id = '46371952'
    print('album id lookup:', album_id, end=", result =  ")
    album_data = lookup_album(album_id)
    print_dict_keys(album_data, ['title', ['artist', 'name'], ['artist', 'id'],
                    'fans', 'id'])


if __name__ == '__main__':
    # delete_cache()
    # lookup_track_detailed(395141722, print_results=True)
    # examples()
    # print(search_track('la danza'))
    print(format_track_details(lookup_track('395141722')))
    print(lookup_track_detailed('395141722'))
    # results = search('Need Your Attention Joris Delacroix',detailed=True)
    # print(search_track(artist='Joris Delacroix',track='Need Your Attention'))
    # utility_functions.dump_json(results)
    # print(utility_functions.print_dict_keys(format_track_details(results)))

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
