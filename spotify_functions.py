import json
import requests
import utility_functions


def create_headers():
    '''' load credentials via json'''
    with open('credentials.json', 'r') as r:
        credentials = json.load(r)
    ''' generate auth token and headers'''
    AUTH_URL = 'https://accounts.spotify.com/api/token'
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
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    return headers


def spotify_download_data(request_type, input):
    # https://developer.spotify.com/documentation/web-api/reference/#/
    headers = create_headers()
    spotify_url = 'https://api.spotify.com/v1/'
    request_types = {'artists': 'artists/',
                     'albums': 'albums/',
                     'tracks': 'tracks/'}
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
    full_url = spotify_url + request_url + input
    return utility_functions.download_data(full_url, headers)


def artist_lookup(id):
    return spotify_download_data('artists', id)


def album_lookup(id):
    return spotify_download_data('albums', id)


def track_lookup(id):
    return spotify_download_data('tracks', id)


def search_artists(string):
    return spotify_download_data('search_artist', string)


def search_tracks(string, results=1):
    if results == 1:
        return spotify_download_data('search_track', string)['tracks']['items'][0]
    else:
        return spotify_download_data('search_track', string)['tracks']['items'][:results]


def search_albums(string):
    return spotify_download_data('search_album', string)


def return_track_details(search_string):
    output_dict = {}
    track_results = search_tracks(search_string)
    output_dict['track name'] = track_results['name']
    output_dict['track type'] = track_results['type']
    output_dict['track id'] = track_results['id']
    output_dict['artist name'] = track_results['artists'][0]['name']
    output_dict['artist id'] = track_results['artists'][0]['id']
    output_dict['album name'] = track_results['album']['name']
    output_dict['album id'] = track_results['album']['id']
    artist_results = artist_lookup(output_dict['artist id'])
    output_dict['artist genres'] = artist_results['genres']
    return output_dict


def example_uses():
    print('artist example')
    artists = artist_lookup('3tSvlEzeDnVbQJBTkIA6nO')
    utility_functions.print_dict_keys(
        artists, ['name', ['followers', 'total'], 'genres'])

    print('album example')
    albums = album_lookup('2dIGnmEIy1WZIcZCFSj6i8')
    print(albums.keys())
    utility_functions.print_dict_keys(
        albums, ['name', 'genres', 'uri'])

    print('track example')
    track = track_lookup('6xZZM6GDxTKsLjF3TNDREL')
    print(track['name'], '-', track['artists'][0]['name'], track['popularity'])

    print('search artist example')
    artist_results = search_artists('pendulum')
    print('show first 5 results - columns: name,followers,popularity,genres')
    for x in artist_results['artists']['items'][:5]:
        print(x['name'], x['followers']['total'], x['popularity'], x['genres'])

    search_track_results = search_tracks('la danza')
    utility_functions.print_dict_keys(search_track_results,
                                      ['name', 'type', 'id'])


if __name__ == '__main__':

    testing = (return_track_details('loud pipes'))
    print(testing)
    example_uses()
