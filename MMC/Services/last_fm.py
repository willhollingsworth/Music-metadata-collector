import requests
import MMC.Util.utility as utility
import json
'''
    https://www.last.fm/api/intro

    issue with most tracks not returning tags despite their being tags on the website
    it doesn't seem to be defaults to album or artist tags either
    example: why why why by dynoro
'''


def last_fm_download_data(method, search, overwrite=0, debug=0):
    # https://developer.spotify.com/documentation/web-api/reference/#/
    credentials = utility.load_credentials('last_fm')
    api_key = credentials['api_key']
    last_fm_url = 'http://ws.audioscrobbler.com/2.0/'
    url_args_format = '?method={}&{}&api_key={}&format=json'
    url_args_full = url_args_format.format(method, search, api_key)
    return utility.download_json(last_fm_url + url_args_full)


def search_tracks(track):
    # https://www.last.fm/api/show/track.search
    return last_fm_download_data('track.search', 'track='+track)


def artist_lookup(artist):
    return last_fm_download_data('artist.getInfo', 'artist='+artist)


def artist_top_tracks_lookup(artist):
    # https://www.last.fm/api/show/artist.getTopTracks
    return last_fm_download_data('artist.getTopTracks', 'artist=' + artist)


def track_lookup(track, artist):
    # https://www.last.fm/api/show/track.getInfo
    search_args = 'track={}&artist={}'.format(track, artist)
    return last_fm_download_data('track.getInfo', search_args)


def track_lookup_mbid(mbid):
    return last_fm_download_data('track.getInfo', 'mbid={}'.format(mbid))


def track_tags_lookup(track, artist):
    search_args = 'track={}&artist={}'.format(track, artist)
    return last_fm_download_data('track.getTopTags', search_args, overwrite=1)


def testing_broken_tags():
    searches = [
        ['why why why', 'dynoro'],
        ['monsters', 'dynoro'],
        ['yournotdead', 'feynman'],
        ['believe', 'cher']]
    for search in searches:
        response = track_lookup(search[0], search[1])
        print_name_artist_tag(response)


def print_name_artist_tag(in_data):
    print('name:', in_data['track']['name'], end=', ')
    print('artist:', in_data['track']['artist']['name'], end=', ')
    tags = [tag['name'] for tag in in_data['track']['toptags']['tag']]
    print('tags:', tags, end=', ')
    # print('keys:', response['track'].keys())
    print()


if __name__ == '__main__':
    # print(json.dumps(artist_top_tracks_lookup('dynoro'), indent=2))

    '''
    mbid lookup not working, look at pulling it from the musicbrainz api
    '''
    print(json.dumps(track_lookup_mbid(
        '8bbcbc5a-6ce0-4cd1-8824-16ba4796a8a1'), indent=2))

    # testing_broken_tags()

    # utility_functions.save_to_file(json.dumps(response,indent=2), 'response.json')
