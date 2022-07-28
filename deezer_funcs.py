import requests
import json
import os
# using code from https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py
# deezer's api docs are behind a login wall

deezer_url = "https://api.deezer.com/"


def download_data(request_type, id):

    if request_type == 'search':
        request_url = 'search?q='
    else:
        raise Exception('wrong type selected', locals())
    full_path = 'cache/deezer/'+request_type+'/'+id+'.json'
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            r = json.load(f)
    else:
        full_url = deezer_url + request_url + id
        r = requests.get(full_url)
        r = r.json()['data']
        with open(full_path, 'w') as f:
            f.write(json.dumps(r))
    return r


def search(search_string):
    if not search_string:
        search_string = 'daft punk'
    data = download_data('search', search_string)
    return data


if __name__ == '__main__':
    search_data = search('caribou')
    print(list(x['title'] + ' by ' + x['artist']['name'] +
          ' type:' + x['type'] for x in search_data))
