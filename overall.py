import spotify_functions
import deezer_functions
import music_brainz_functions
from pprint import pprint
import utility_functions as utils

if __name__ == '__main__':
    # utils.delete_cache()
    spotify_current_id = spotify_functions.current_playing()
    #spotify
    spotify_track = spotify_functions.lookup_track_detailed(spotify_current_id)
    current_playing_track,current_playing_artist = spotify_track['track name'],spotify_track['artist name']
    print('Spotify currently playing :', current_playing_track,'by',current_playing_artist)
    print('Spotify artist genres :',spotify_track['artist genres'])
    #deezer
    dez_search = deezer_functions.search_track(track=current_playing_track,artist=current_playing_artist)
    dez_details = deezer_functions.lookup_track_detailed(dez_search['track id'])
    print(  f'deezer results for {dez_details["track name"]} by {dez_details["artist name"]}',
            f'album genres : {dez_details["album genres"]}',
    )
    # print(len(dez_track['genres']))
    # if len(dez_track['genres']) > 1:
    #     print('Deezer album genres :',dez_track['genres'])
    # else:
    #     print('Deezer found no genres')
