import requests
import utility_functions
import json
from pprint import pprint
'''
    https://musicbrainz.org/doc/MusicBrainz_API
    https://musicbrainz.org/doc/MusicBrainz_API/Examples
'''


def music_brainz_download_data(url_args, overwrite=0, debug=0):
    base_url = 'https://musicbrainz.org/ws/2/'
    if '?' in url_args:
       url_args += '&fmt=json'
    else:
        url_args += '?fmt=json'
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

def lookup_artist_id(id):
    # https://musicbrainz.org/doc/MusicBrainz_API/Search
    return music_brainz_download_data('artist/'+id)

def lookup_releases(id):
    # example url https://musicbrainz.org/ws/2/release?artist=f2c454ec-69a2-49a7-a79c-eaabef25ba44&inc=release-groups
    return music_brainz_download_data(f'release?artist={id}&inc=release-groups')



def run_search_examples():
    artist = 'Joris Delacroix'
    print('search for artist:', artist)
    artists = search_artist(artist)

    results = ([f"name: {a['name']}, id: {a['id']}, score: {a['score']}"
          for a in (artists)['artists']])
    for x in results[:1]:
        print(x)
    track, track_artist = ('satisfaction', 'benny benassi')
    print('search for track:', track, 'by artist:', track_artist)
    tracks = search_track(track, track_artist)
    recording = tracks['recordings'][0]
    print(recording['title'], 'by',
          recording['artist-credit'][0]['name'])

    # utility_functions.save_to_file(
    #     json.dumps(tracks, indent=1), 'response.json')

def run_chain_example(artist):
    results = search_artist(artist)
    artist_id = results['artists'][0]['id']
    print(artist_id)
    artist_details = lookup_artist_id(artist_id)
    # print()
    releases = lookup_releases(artist_id)
    # pprint(releases)
    release_details = [f"{r['title']} - {r['release-group']['primary-type']}" for r in releases['releases']]
    pprint(release_details)

    return
if __name__ == '__main__':
    # run_search_examples()
    run_chain_example('Joris Delacroix')