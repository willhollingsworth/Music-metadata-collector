import os
import requests
import json


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


def download_data(url, headers='', overwrite=0, debug=0):
    cache_folder = 'cache/'
    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)
    striped_characters = ':/\|?'
    processed_url = url
    for char in striped_characters:
        processed_url = processed_url.replace(char, '_')

    full_path = cache_folder + processed_url + '.json'
    if os.path.exists(full_path) and not overwrite:
        with open(full_path, 'r') as f:
            r = json.load(f)
    else:
        r = requests.get(url, headers=headers).json()
        if debug:
            print(r['tracks'].keys())
        if 'data' in r:
            r = r['data']
        with open(full_path, 'w') as f:
            f.write(json.dumps(r))
    return r


def load_credentials(service):
    valid_services = ['spotify', 'last_fm']
    # add check for credentials file, if false create a blank one in the right format with appropriate error msg
    if not service in valid_services:
        raise Exception('chosen service: ', service,
                        ' is not a valid service, only the following are allowed', valid_services)
    '''' load credentials via json'''
    with open('credentials.json', 'r') as r:
        credentials = json.load(r)[service]
    return credentials
