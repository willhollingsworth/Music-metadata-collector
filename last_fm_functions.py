import requests
import utility_functions
import json


def last_fm_download_data(method, search, overwrite=0, debug=0):
    # https://developer.spotify.com/documentation/web-api/reference/#/
    credentials = utility_functions.load_credentials('last_fm')
    api_key = credentials['api_key']
    last_fm_url = 'http://ws.audioscrobbler.com/2.0/'
    url_args_format = '?method={}&{}&api_key={}&format=json'
    url_args_full = url_args_format.format(method, search, api_key)
    return utility_functions.download_data(last_fm_url + url_args_full)


def search_artists(string):
    return last_fm_download_data('artist.getInfo', 'artist='+string)


def search_tracks(string):
    return last_fm_download_data('track.search', 'track='+string)


def track_lookup(track, artist):
    # issue with most tracks not returning tags despite their being tags on the website
    # example: why why why by dynoro
    search_args = 'track={}&artist={}'.format(track, artist)
    return last_fm_download_data('track.getInfo', search_args)


def track_tags_lookup(track, artist):
    search_args = 'track={}&artist={}'.format(track, artist)
    return last_fm_download_data('track.getTopTags', search_args, overwrite=1)


if __name__ == '__main__':
    response = track_lookup('why why why', 'dynoro')
    # response = track_lookup('believe', 'cher')
    utility_functions.save_to_file(json.dumps(response), 'response.json')
