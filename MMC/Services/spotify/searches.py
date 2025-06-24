from typing import Any

from mmc.services.spotify.api_requests import spotify_download_data


def search_artists(string):
    """Search for an artist on Spotify."""
    results = spotify_download_data("search_artist", string)
    if False:
        print_dict_keys(
            results["artists"]["items"][0],
            ["name", ["followers", "total"], "popularity", "genres"],
        )
    return results


def multi_search(track, artist):
    """Search for a track and artist on Spotify."""
    results = spotify_download_data("multi", {"track": track, "artist": "artist"})
    return results


def search_tracks(search_string: str, results: int = 1) -> list[dict[str, Any]]:
    """Search for a track on Spotify."""
    if results == 1:
        return spotify_download_data("search_track", search_string)["tracks"]["items"][
            0
        ]
    return spotify_download_data("search_track", search_string)["tracks"]["items"][
        :results
    ]


def search_albums(string: str) -> dict[str, Any]:
    """Search for an album on Spotify."""
    return spotify_download_data("search_album", string)


if __name__ == "__main__":
    artist_string = "pendulum"
    print('artist search with string "', artist_string, '"', end=" : ")
    first_result = search_artists(artist_string)["artists"]["items"][0]
    print(first_result)
