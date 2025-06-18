from __future__ import annotations
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

from MMC.Util import utility

# having issues with track search being inaccurate
# attempting to search track + artist but doesn't appear to be working
# maybe try looking through search results and do a string match on track and artist names?

AUTH_URL = 'https://accounts.spotify.com/api/token'


def create_client_headers() -> dict[str, str]:
    """Create headers for spotify api requests."""
    credentials = utility.load_credentials('spotify')
    # generate auth token and headers
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': credentials['client_id'],
        'client_secret': credentials['client_secret'],
    })
    # convert the response to JSON
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']
    return {
        'Authorization': f'Bearer {access_token}',
    }


def spotify_download_data(
        request_type: str,
        input_value: str | dict[str, str],
        overwrite: bool = False,
        debug: bool = False,
        ) -> dict:
    """Download data from the Spotify API."""
    # https://developer.spotify.com/documentation/web-api/reference/#/
    headers = create_client_headers()
    spotify_url = 'https://api.spotify.com/v1/'
    request_types = {
        'artists': 'artists/',
        'albums': 'albums/',
        'tracks': 'tracks/',
    }
    valid_search_types = ['artist', 'track', 'album', 'genre']
    if request_type in request_types:
        request_url = request_types[request_type]
    elif request_type.split('_')[0] == 'search':
        search_type = request_type.split('_')[1]
        if search_type in valid_search_types:
            request_url = 'search?type={0}&q={0}:'.format(search_type)
        else:
            raise Exception(
                'wrong search selected, only the following are valid', valid_search_types, locals())
    else:
        raise Exception('wrong type selected', locals())
    processed_input = ''
    if isinstance(input_value, dict):
        for key in input_value:
            if key == search_type:
                processed_input += input_value[key]
            else:
                processed_input += '&' + key + ':' + input_value[key]
    else:
        processed_input = input_value

    full_url = spotify_url + request_url + processed_input
    return utility.download_json(full_url, headers, overwrite, debug)


def lookup_artist(id,print_results=False):
    """Lookup an artist on Spotify."""
    results = spotify_download_data('artists', id)
    if print_results:
        utility.print_dict_keys(
        results, ['name', ['followers', 'total'], 'genres'])
    return results


def lookup_album(id, print_results=False):
    """Lookup an album on Spotify."""
    results = spotify_download_data('albums', id)
    if print_results:
        utility.print_dict_keys(
        results, ['name', 'genres', 'uri'])
    return results


def lookup_track(id, print_results=False):
    """Lookup a track on Spotify."""
    results = spotify_download_data('tracks', id)

    if print_results:
        utility.print_dict_keys(
        results, ['name', ['artists', 0, 'name'], 'popularity'])
    return results


def lookup_track_detailed(id, print_results=False):
    """Lookup a track on Spotify with detailed information."""
    output_dict = {}
    track = lookup_track(id)
    # print(utility.print_dict_keys(track))
    output_dict['track name'] = track['name']
    output_dict['track type'] = track['type']
    output_dict['track id'] = track['id']
    if isinstance(track['artists'], list):
        output_dict['artist name'] = track['artists'][0]['name']
        output_dict['artist id'] = track['artists'][0]['id']
    else:
        output_dict['artist name'] = track['artists']
        output_dict['artist id'] = track['artists']
    output_dict['album name'] = track['album']['name']
    output_dict['album id'] = track['album']['id']
    artist_results = lookup_artist(output_dict['artist id'])
    output_dict['artist genres'] = artist_results['genres']
    if print_results:
        utility.print_dict_keys(
        output_dict, ['track name', 'artist name', 'album name', 'artist genres'])
    return output_dict


def search_artists(string, print_results=False):
    """Search for an artist on Spotify."""
    results = spotify_download_data('search_artist', string)
    if print_results:
        utility.print_dict_keys(
        results['artists']['items'][0], ['name', ['followers','total'], 'popularity','genres'])
    # print(first_result['name'],', followers:',first_result['followers']['total'],', popularity',first_result['popularity'],', genres',first_result['genres'])
    return results


def multi_search(track, artist):
    """Search for a track and artist on Spotify."""
    results = spotify_download_data(
        'multi', {'track': track, 'artist': 'artist'})
    return results


def search_tracks(search_string, results=1, overwrite=0, debug=0):
    """Search for a track on Spotify."""
    if results == 1:
        return spotify_download_data('search_track', search_string, overwrite, debug)['tracks']['items'][0]
    else:
        return spotify_download_data('search_track', search_string, overwrite, debug)['tracks']['items'][:results]


def search_albums(string):
    """Search for an album on Spotify."""
    return spotify_download_data('search_album', string)


def current_playing(print_results=False):
    """Get the currently playing track on Spotify."""
    load_dotenv()
    scope = 'user-read-playback-state'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    current_playback = sp.current_playback()
    if not current_playback:
        print('spotify is not currently playing anything')
        return
    if print_results:
        utility.print_dict_keys(
        current_playback['item'], ['name',['artists',0,'name'], ['album','name'],'id'])
    return current_playback['item']['id']


def current_playing_detailed(print_results=False):
    """Get the currently playing track on Spotify with detailed information."""
    track_id = current_playing()
    track_details = lookup_track_detailed(track_id,print_results)
    return track_details


def examples():
    print('running spotify api examples')

    # lookups
    artist_id = '3tSvlEzeDnVbQJBTkIA6nO'
    print('artist lookup with id', artist_id, end=": ")
    lookup_artist(artist_id, print_results=True)

    album_id = '2dIGnmEIy1WZIcZCFSj6i8'
    print('album lookup with id', album_id, end=": ")
    lookup_album(album_id, print_results=True)

    track_id = current_playing() # can use currently playing instead
    track_id = '6xZZM6GDxTKsLjF3TNDREL'
    print('track lookup', track_id, end=": ")
    lookup_track(track_id, print_results=True)

    print('detailed track lookup', end=": ")
    # lookup_track_detailed(track_id, print_results=True)

    # #searches
    artist_string = 'pendulum'
    print('artist search with string \"',artist_string,'"', end=" : ")
    first_result = search_artists(artist_string, print_results=True)['artists']['items'][0]

    # print('show first 5 results - columns: name,followers,popularity,genres')
    # for x in artist_results['artists']['items'][:5]:
    #     print(x['name'], x['followers']['total'], x['popularity'], x['genres'])

    # search_track_results = search_tracks('la danza')
    # utility_functions.print_dict_keys(search_track_results,
    #                                   ['name', 'type', 'id'])


if __name__ == '__main__':
    print('running spotify.py as main')
    examples()
    # current_playing_detailed(print_results=True)
    # pprint(lookup_track_detailed(current_playing()))

    # current_playing_detailed()
    # lookup_track_detailed('7v0umDmPFMzmkBT1uWSYIL')


    # pprint(artist_results.keys())
    # pprint(results)
    # examples()


    # album_id = '2dIGnmEIy1WZIcZCFSj6i8'
    # print('album lookup with id',album_id, end=": ")
    # albums = lookup_album(album_id)
    # print(str(albums).encode(encoding="utf-8"))
    
    # url = 'https://api.spotify.com/v1/' + \
    #     'search?type=track&q=track:' + 'elecktor' + '&artist:'
    # headers = create_headers()
    # print(utility_functions.download_data(
    #     url, headers).keys())

    # for string in ["another life", ["another life", "afrojack"]]:
    #     track_details = return_track_details(string)
    #     for details in ['track name', 'artist name', 'album name', 'artist genres']:
    #         print(details, ':', track_details[details], end=', ')
    #     print()

    # print(return_track_details('another life'))
    # print(return_track_details(["another life", "afrojack"]))
    # multi_search(["Bla Bla Bla", "Gigi D'Agostino"])
    # print(testing)
