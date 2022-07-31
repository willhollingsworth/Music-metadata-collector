import requests
import json
import os
import utility_functions
# deezer's api docs are behind a login wall
# some public api docs https://apieco.ir/docs/deezer#api-Search-search
# also examples of use here https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py


def download_deezer_data(request_type, input):
    deezer_url = "https://api.deezer.com/"
    request_types = {'search': 'search?q=',
                     'album': 'album/',
                     'track': 'track/'}
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        raise Exception('wrong type selected', locals())
    url = deezer_url + request_url + input
    cache_folder = 'deezer/' + request_type
    return utility_funcs.download_data(input, url, cache_folder)


def search(search_string, print_keys='', limit=0):
    search_data = download_deezer_data('search', search_string)
    if not limit:
        limit = len(search_data)
    if print_keys:
        for result in search_data[:limit]:
            utility_funcs.print_dict_keys(result, print_keys)
    return search_data[:limit]


def album_lookup(album_id, print_keys=''):
    album_data = download_deezer_data('album', album_id)
    if print_keys:
        utility_funcs.print_dict_keys(album_data, print_keys)
    return album_data


def track_lookup(track_id, print_keys=''):
    track_data = download_deezer_data('track', track_id)
    if print_keys:
        utility_funcs.print_dict_keys(track_data, print_keys)
    return track_data


if __name__ == '__main__':
    print('string search example:')
    search_keys = ['title', ['artist', 'name'], [
        'album', 'title'], ['album', 'id'], 'type', 'id']
    search_data = search('caribou', search_keys, 2)

    print('track id lookup example:')
    track_keys = ['title', ['album', 'title'],
                  'duration', 'rank', 'bpm', 'gain', 'id']
    track_data = track_lookup('395141722', track_keys)

    print('album lookup example')
    album_keys = ['title', ['artist', 'name'], ['artist', 'id'],
                  'fans',  'id']
    album_data = album_lookup('46371952', album_keys)
