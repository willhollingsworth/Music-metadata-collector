import requests
import utility_functions
import json
'''
    https://musicbrainz.org/doc/MusicBrainz_API
    https://musicbrainz.org/doc/MusicBrainz_API/Examples
'''


def music_brainz_download_data(url_args, overwrite=0, debug=0):
    base_url = 'https://musicbrainz.org/ws/2/'
    url_args += '&fmt=json'
    return utility_functions.download_data(base_url + url_args)


def search_artist(artist):
    # https://musicbrainz.org/doc/MusicBrainz_API/Search
    return music_brainz_download_data('artist?query='+artist)


def search_track(track, artist=''):
    if not artist:
        url = 'recording?query="{}"'.format(track)
    else:
        url = 'recording?query="{}" AND artist:"{}"'.format(track, artist)
    return music_brainz_download_data(url)


def run_examples():
    artist = 'dynoro'
    print('search for artist:', artist)
    artists = search_artist(artist)
    print([a['name']+' ' + a['type']+' ' + a['id']
          for a in (artists)['artists']])

    track, track_artist = ('satisfaction', 'benny benassi')
    print('search for track:', track, 'by artist:', track_artist)
    tracks = search_track(track, track_artist)
    print(tracks['recordings'][0]['title'], 'by',
          tracks['recordings'][0]['artist-credit'][0]['name'])

    # utility_functions.save_to_file(
    #     json.dumps(tracks, indent=1), 'response.json')


if __name__ == '__main__':
    run_examples()
