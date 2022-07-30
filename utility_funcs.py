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


def download_data(input, url, cache_folder):
    folder_path = 'cache/' + cache_folder
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    full_path = folder_path + '/' + input + '.json'
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            r = json.load(f)
    else:
        r = requests.get(url).json()
        if 'data' in r:
            r = r['data']
        with open(full_path, 'w') as f:
            f.write(json.dumps(r))
    return r