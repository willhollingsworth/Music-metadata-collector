import spotify_functions
import deezer_functions
from pprint import pprint
import utility_functions as utils

if __name__ == '__main__':
    spotify_playing = spotify_functions.current_playing(print_results=True)['item']
    current_playing_track = spotify_playing['name']
    current_playing_artist = spotify_playing['artists'][0]['name']
    print(current_playing_track,' by ',current_playing_artist)
    d_search = deezer_functions.search(track=current_playing_track,artist=current_playing_artist,detailed=True)
    print("deezer album genres",d_search['genres'])
    # print(s_playing['currently_playing']['item'].keys())
    # utils.dump_json(s_playing)