import spotify_functions
import deezer_functions
import music_brainz_functions
from pprint import pprint
import utility_functions as utils

def grab_current_track_artist():
    spotify_playing = spotify_functions.current_playing()['item']
    out_dict ={}
    out_dict['track'] = spotify_playing['name']
    out_dict['artist'] = spotify_playing['artists'][0]['name']

    return out_dict


if __name__ == '__main__':
    spotify_results = grab_current_track_artist()
    current_playing_track,current_playing_artist = spotify_results['track'],spotify_results['artist']
    # current_playing_track,current_playing_artist = ('Trouble','Robby East')
    print('Spotify currently playing :', current_playing_track,'by',current_playing_artist)

    
    print()
    mb_track = music_brainz_functions.search_track(current_playing_track,current_playing_artist)
    if not isinstance(mb_track, dict):
        print('Music Brainz found no results')
    else:
        if 'genres' in mb_track.keys():
            if mb_track['genres'][0] != 'none':
                print('Music Brainz genres :',mb_track['genres'])
            else: 
                print('Music Brainz found no genres')
        else:
            print('Music Brainz found no genres')
    dez_track = deezer_functions.search(track=current_playing_track,artist=current_playing_artist,detailed=True)
    # print(len(dez_track['genres']))
    if len(dez_track['genres']) > 1:
        print('Deezer album genres :',dez_track['genres'])
    else:
        print('Deezer found no genres')
