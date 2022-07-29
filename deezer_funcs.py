import requests
import json
import os
# deezer's api docs are behind a login wall
# some public api docs https://apieco.ir/docs/deezer#api-Search-search
# also examples of use here https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py


deezer_url = "https://api.deezer.com/"


def download_data(request_type, id):

    request_types = {'search': 'search?q=',
                     'album': 'album/',
                     'track': 'track/'}
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        raise Exception('wrong type selected', locals())

    folder_path = 'cache/deezer/' + request_type
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    full_path = folder_path + '/' + id + '.json'
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            r = json.load(f)
    else:
        full_url = deezer_url + request_url + id
        r = requests.get(full_url).json()
        if 'data' in r:
            r = r['data']
        with open(full_path, 'w') as f:
            f.write(json.dumps(r))
    return r


def print_dict_keys(input_dict, keys):
    for key in keys:
        if isinstance(key, str):
            print(key, ':', input_dict[key], end=', ')
        elif isinstance(key, list):
            if len(key) == 2:
                print(key[0], key[1], ':',
                      input_dict[key[0]][key[1]], end=', ')
    print()
    return


def search(search_string, print_keys=''):
    search_data = download_data('search', search_string)
    if print_keys:
        for result in search_data:
            print_dict_keys(result, print_keys)
    return search_data


def album_lookup(album_id, print_keys=''):
    album_data = download_data('album', album_id)
    if print_keys:
        print_dict_keys(album_data, print_keys)
    return album_data


def track_lookup(track_id, print_keys=''):
    track_data = download_data('track', track_id)
    if print_keys:
        print_dict_keys(track_data, print_keys)
    return track_data


if __name__ == '__main__':
    print('string search example:')
    search_keys = ['title', ['artist', 'name'], [
        'album', 'title'], ['album', 'id'], 'type', 'id']
    search_data = search('caribou', search_keys)

    print('track id lookup example:')
    track_keys = ['title', ['album', 'title'],
                  'duration', 'rank', 'bpm', 'gain', 'id']
    track_data = track_lookup('395141722', track_keys)

    print('album lookup example')
    album_keys = ['title', ['artist', 'name'], ['artist', 'id'],
                  'fans',  'id']
    album_data = album_lookup('46371952', album_keys)
