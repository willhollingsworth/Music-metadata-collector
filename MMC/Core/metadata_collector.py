"""Overall metadata collection logic."""

from MMC.Services import deezer, spotify
from MMC.Util.cache import delete_cache


def get_current_track_details() -> None:
    """Grab current playing spotify track and return details from multiple services."""
    delete_cache()
    spotify_current_id = spotify.current_playing()
    # spotify
    if spotify_current_id:
        spotify_track = spotify.lookup_track_detailed(spotify_current_id)
        playing_track: str = spotify_track['track name']
        playing_artist: str = spotify_track['artist name']
        playing_genres: str = spotify_track['artist genres']
        print(f'Spotify currently playing :{playing_track} by {playing_artist}')
        print()
        print(f'Spotify results:      artist genres :{playing_genres}')
        # deezer
        dez_search = deezer.search_track(
            track=playing_track,
            artist=playing_artist,
            )
        dez_details = deezer.lookup_track_detailed(dez_search['track id'])
        track: str = dez_details['track name']
        artist: str = dez_details['artist name']
        album_genres: str = dez_details['album genres']
        print(
            f'deezer results for {track} by {artist}',
            f'album genres : {album_genres}',
        )


if __name__ == '__main__':
    get_current_track_details()
