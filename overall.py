import spotify_functions
import deezer_functions
import music_brainz_functions
from pprint import pprint
import utility_functions as utils

if __name__ == '__main__':
    spotify_playing = spotify_functions.current_playing()['item']
    current_playing_track = spotify_playing['name']
    current_playing_artist = spotify_playing['artists'][0]['name']
    print('Spotify currently playing :', current_playing_track,'by',current_playing_artist)
    dez_track = deezer_functions.search(track=current_playing_track,artist=current_playing_artist,detailed=True)
    print('Deezer album genres :',dez_track['genres'])
    mb_track = music_brainz_functions.search_track(current_playing_track,current_playing_artist)
    if 'genres' in mb_track.keys():
        print('Music Brainz genres :',mb_track['genres'])
    else:
        print('Music Brainz found no genres')
