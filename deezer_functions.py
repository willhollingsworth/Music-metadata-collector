import requests
import json
import os
import utility_functions
from pprint import pprint
# deezer's api docs are behind a login wall
# some public api docs https://apieco.ir/docs/deezer#api-Search-search
# also examples of use here https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py


def download_deezer_data(request_type, input):
    deezer_url = "https://api.deezer.com/"
    request_types = {'search': 'search?q=',
                     'album': 'album/',
                     'artist': 'artist/',
                     'track': 'track/'}
    if request_type in request_types:
        request_url = request_types[request_type]
    else:
        raise Exception('wrong type selected', locals())
    url = deezer_url + request_url + str(input)
    return utility_functions.download_data(url)


def search(search_string='',detailed=False,artist='',track=''):
    search_items = []
    if bool(search_string):
        search_items.append(search_string)
    if bool(artist):
        search_items.append('artist:"{}"'.format(artist))
    if bool(track):
        search_items.append('track:"{}"'.format(track))
    search_string_final = " ".join(search_items)
    search_data = download_deezer_data('search', search_string_final)
    if detailed:
        search_data = {'search_data':search_data[0]}
        album_id = search_data['search_data']['album']['id']
        search_data['lookup_album'] = lookup_album(album_id)
        artist_id = search_data['search_data']['artist']['id']
        search_data['lookup_artist'] = lookup_artist(artist_id)
        track_id = search_data['search_data']['id']
        search_data['lookup_track'] = lookup_track(track_id)
        genres = []
        for genre in search_data['lookup_album']['genres']['data']:
            genres.append(genre['name'])
        search_data['genres'] = genres
    if isinstance(search_data,list):
        return search_data[0]
    else:
        return search_data

def lookup_album(album_id, print_keys=''):
    return download_deezer_data('album', album_id)

def lookup_artist(artist_id, print_keys=''):
    return download_deezer_data('artist', artist_id)

def lookup_track(track_id, print_keys=''):
    return download_deezer_data('track', track_id)

def format_track_details(track_results):
    # input is a track search result
    #  output a better formatted dictionary 
    output_dict = {}
    for track in track_results:
        if track['type'] == 'track':
            track_results = track
            break
    output_dict['track name'] = track_results['title']
    output_dict['track type'] = track_results['type']
    output_dict['track id'] = track_results['id']
    output_dict['artist name'] = track_results['artist']['name']
    output_dict['artist id'] = track_results['artist']['id']
    output_dict['album name'] = track_results['album']['title']
    output_dict['album id'] = track_results['album']['id']
    album_results = lookup_album(output_dict['album id'])

    output_dict['album genres'] = [genre['name']
                                   for genre in album_results['genres']['data']]

    return output_dict


if __name__ == '__main__':
    # results = search('Need Your Attention Joris Delacroix',detailed=True)
    # results = search(artist='Joris Delacroix',track='Need Your Attention',detailed=True)
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
