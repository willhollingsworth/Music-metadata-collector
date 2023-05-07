import utility_functions
from pprint import pprint

# example https://melaniewalsh.github.io/Intro-Cultural-Analytics/04-Data-Collection/07-Genius-API.html


def genius_download_data(input):
    credentials = utility_functions.load_credentials('genius')
    cred_arg = '&access_token=' + credentials['access_token']
    genius_api_url = 'https://api.genius.com/'

    full_url = genius_api_url + input + cred_arg
    return utility_functions.download_data(full_url)

def search(track):
    # https://www.last.fm/api/show/track.search
    arg = 'search?q='
    return genius_download_data(arg + track)['response']['hits']

def format_search_results(results):
    out = []
    for i in results:
        out.append('{} by {}'.format(i['result']['title'],i['result']['artist_names']))
    return out
if __name__ == '__main__':
    # print(utility_functions.show_structure(search('dynoro')[0]))
    results = search('rock it by sub focus')
    results = format_search_results(results)
    pprint(results)
    # print('{} by {}'.format(result['title'],result['primary_artist']['name']))