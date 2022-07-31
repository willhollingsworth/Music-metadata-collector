import json
import requests
import utility_functions


def create_auth_token():
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
    return access_token


def spotify_download_data(request_type, input):
    # todo - use utility downloader to allow for local caching

    # https://developer.spotify.com/documentation/web-api/reference/#/
    access_token = create_auth_token()
    # generate header
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    spotify_url = 'https://api.spotify.com/v1/'
    request_types = {'artists': 'artists/',
                     'albums': 'albums/',
                     'tracks': 'tracks/',
                     'search_artist': 'search?type=artist&q='}
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        raise Exception('wrong type selected', locals())
    full_url = spotify_url + request_url + input
    r = requests.get(full_url, headers=headers)
    return r.json()


if __name__ == '__main__':

    print('artist example')
    artists = spotify_download_data('artists', '3tSvlEzeDnVbQJBTkIA6nO')
    utility_funcs.print_dict_keys(
        artists, ['name', ['followers', 'total'], 'genres'])

    print('album example')
    albums = spotify_download_data('albums', '392RA8UhAIoBzpbn3bPy3Q')
    utility_funcs.print_dict_keys(
        albums, ['name', 'genres', 'uri'])

    print('track example')
    track = spotify_download_data('tracks', '6xZZM6GDxTKsLjF3TNDREL')
    print(track['name'], '-', track['artists'][0]['name'], track['popularity'])

    print('search artist example')
    search_artist = spotify_download_data('search_artist', 'artist:pendulum')
    print('show first 5 results - columns: name,followers,popularity,genres')
    for x in search_artist['artists']['items'][:5]:
        print(x['name'], x['followers']['total'], x['popularity'], x['genres'])
