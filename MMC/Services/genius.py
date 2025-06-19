from collections import Counter

from MMC.Util.credentials import load_credentials
from MMC.Util.http_client import download_json

# the genius api supports several types of data collecting but not genres (they call them tags)
# you can scrape their web pages to get this but needs to be done per song.

# official docs https://docs.genius.com/
# example https://melaniewalsh.github.io/Intro-Cultural-Analytics/04-Data-Collection/07-Genius-API.html



def genius_download_data(input):
    credentials = load_credentials('genius')
    if '?' in input:
        cred_arg = '&access_token=' + credentials['access_token']
    else:
        cred_arg = '?access_token=' + credentials['access_token']
    genius_api_url = 'https://api.genius.com/'
    full_url = genius_api_url + input + cred_arg

    return download_json(full_url)

def search(track):
    arg = 'search?q='
    return genius_download_data(arg + track)['response']['hits']

def format_search_results(results):
    out = []
    for i in results:
        out.append('{} by {}'.format(i['result']['title'],i['result']['artist_names']))
    return out

def lookup_artist(artist_id):
    arg = 'artists/'
    return genius_download_data(arg + artist_id)

def get_artist_songs(artist_id,page=1,songs_only=True):
    per_arg = 'artists/'
    post_arg = '/songs?per_page=50&page=' + str(page)
    # return genius_download_data(arg + artist_id +'/songs?per_page=50')
    if songs_only:
        return genius_download_data(per_arg + artist_id + post_arg )['response']['songs']
    else:
        return genius_download_data(per_arg + artist_id + post_arg )

def get_all_songs(artist_id):
    page = 1
    songs = []
    while True:
        response = get_artist_songs(artist_id,page,songs_only=False)
        songs += response['response']['songs']
        if response['response']['next_page'] == None:
            break
        page += 1
    return songs

def lookup_song(song_id):
    arg = 'songs/'
    return genius_download_data(arg + song_id)


def run_tests():
    # run search
    search_string = 'lane 8'
    results = search(search_string)
    print('searching for string \"{}\", found {} results'.format(search_string,len(results)))
    # pprint(format_search_results(results)) # show results 
    # list artist ids from search    
    print('artist ids of results :',dict(Counter([x['result']['primary_artist']['id'] for x in results])))
    # lists all songs from artist id
    results = get_all_songs(artist_id='582604')
    print('get all songs: found {} songs by {}'.format(len(results),results[0]['artist_names']))
    # print(['{} by {}'.format(song['title'],song['artist_names']) for song in results])
    lookup_song('3477832')

if __name__ == '__main__':
    run_tests()
    # results = search('sub focus')
    # pprint(get_artist('100291'))
    # results = get_all_songs(artist_id='100291')
    # print(type(results),len(results))
    # print(['{} by {}'.format(song['title'],song['artist_names']) for song in results])
    # print(results.keys())
    # print(format_search_results(results))
    # utility_functions.print_structure(results[0])
    # pprint(results[3]['result']['primary_artist']['id'])

