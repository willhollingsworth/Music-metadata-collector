import spotify_functions
import deezer_functions
import music_brainz_functions
from pprint import pprint
import utility_functions as utils

if __name__ == '__main__':
    spotify_current_id = spotify_functions.current_playing()
    #spotify
    spotify_track = spotify_functions.lookup_track_detailed(spotify_current_id)
    current_playing_track,current_playing_artist = spotify_track['track name'],spotify_track['artist name']
    print('Spotify currently playing :', current_playing_track,'by',current_playing_artist)
    print('Spotify artist genres :',spotify_track['artist genres'])
    #Music brainz
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
    #deezer
    dez_track = deezer_functions.search(track=current_playing_track,artist=current_playing_artist,detailed=True)
    # print(len(dez_track['genres']))
    if len(dez_track['genres']) > 1:
        print('Deezer album genres :',dez_track['genres'])
    else:
        print('Deezer found no genres')
