"""MusicBrainz searches for artists, albums, and tracks."""

from typing import Any

from mmc.services.music_brainz.api_requests import request_search


def search_artist(artist: str) -> dict[str, Any]:
    # https://musicbrainz.org/doc/MusicBrainz_API/Search
    results = request_search("artist?query=" + artist)
    return results["artists"][0]


def search_track(
    track: str,
    artist: str = "",
) -> dict[str, Any] | str:
    if not artist:
        url = f'recording?query="{track}"'
    else:
        url = f'recording?query="{track}" AND artist:"{artist}"'
    out_dict = {}
    result = request_search(url)
    if result["count"] == 0:
        return "no results"
    result = result["recordings"][0]
    out_dict["track"] = result["title"]
    out_dict["artist"] = result["artist-credit"][0]["name"]
    out_dict["id"] = result["id"]
    if "tags" in result.keys():
        out_dict["genres"] = [g["name"] for g in result["tags"]]
    else:
        out_dict["genres"] = ["none"]
    return out_dict


if __name__ == "__main__":
    artist = "Joris Delacroix"
    print("search for artist :", artist, end=": ")
    search_artist(artist)
    print()
    track, track_artist = ("satisfaction", "benny benassi")
    print("search for track:", track, "by artist:", track_artist, end=": ")
    st_results = search_track(track, track_artist)
    print(st_results)
