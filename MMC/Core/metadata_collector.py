"""Overall metadata collection logic."""

from mmc import delete_cache, spotify_current_playing, spotify_lookup_track


def get_current_track_details() -> None:
    """Grab current playing spotify track and return details from multiple services."""
    delete_cache()
    spotify_current_id = spotify_current_playing()
    # spotify
    if spotify_current_id:
        spotify_track = spotify_lookup_track(spotify_current_id)

        print(
            f"Spotify currently playing : {spotify_track.track_name}",
            f"by {spotify_track.artist_name}",
        )
        print()
        # print(f"Spotify results:      artist genres :{playing_genres}")
        # deezer
        # dez_search = deezer.search_track(
        #     track=playing_track,
        #     artist=playing_artist,
        # )
        # track: str = dez_search["track name"]
        # artist: str = dez_search["artist name"]

        # album_genres: list[str] = deezer.lookup_track_genres(dez_search["track id"])
        # print(
        #     f"deezer results for {track} by {artist}",
        #     f"album genres : {album_genres}",
        # )


if __name__ == "__main__":
    get_current_track_details()
