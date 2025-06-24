from pprint import pprint

from mmc.utils.cache import delete_cache
from mmc.utils.http_client import download_json

"""
    https://musicbrainz.org/doc/MusicBrainz_API
    https://musicbrainz.org/doc/MusicBrainz_API/Examples
"""


def music_brainz_download_data(url_args, overwrite=0, debug=0):
    base_url = "https://musicbrainz.org/ws/2/"
    if "?" in url_args:
        url_args += "&fmt=json"
    else:
        url_args += "?fmt=json"
    return download_json(base_url + url_args)


def search_artist(artist, print_results=False):
    # https://musicbrainz.org/doc/MusicBrainz_API/Search
    results = music_brainz_download_data("artist?query=" + artist)
    if print_results:
        formatted_artists = [
            f"name: {a['name']}, id: {a['id']}, score: {a['score']}"
            for a in (results)["artists"]
        ]
        for x in formatted_artists[:1]:
            print(x)
    return results["artists"][0]


def search_track(track, artist=""):
    if not artist:
        url = f'recording?query="{track}"'
    else:
        url = f'recording?query="{track}" AND artist:"{artist}"'
    out_dict = {}
    result = music_brainz_download_data(url)
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


def lookup_artist(id):
    # https://musicbrainz.org/doc/MusicBrainz_API#Lookups
    return music_brainz_download_data("artist/" + id)


def lookup_album(id):
    # example url https://musicbrainz.org/ws/2/release?artist=f2c454ec-69a2-49a7-a79c-eaabef25ba44&inc=release-groups
    return music_brainz_download_data(f"release?release={id}")


def lookup_track(id):
    return music_brainz_download_data(f"recording/{id}?inc=artists+releases")


def examples():
    # searches
    artist = "Joris Delacroix"
    print("search for artist :", artist, end=": ")
    search_artist(artist, print_results=True)
    track, track_artist = ("satisfaction", "benny benassi")
    print("search for track:", track, "by artist:", track_artist, end=": ")
    st_results = search_track(track, track_artist)
    print(st_results)
    # utility_functions.save_to_file(
    #     json.dumps(tracks, indent=1), 'response.json')


def run_chain_example(artist):
    results = search_artist(artist)
    artist_id = results["artists"][0]["id"]
    print(artist_id)
    artist_details = lookup_artist(artist_id)
    # print()
    releases = lookup_album(artist_id)
    # pprint(releases)
    release_details = [
        f"{r['title']} - {r['release-group']['primary-type']}"
        for r in releases["releases"]
    ]
    pprint(release_details)


if __name__ == "__main__":
    delete_cache()
    # examples()
    # lookups
    track_id = "4e0be2ce-4672-423e-ba35-6ce49773d1ab"
    track = lookup_track(track_id)
    for release in track["releases"]:
        print(release["title"])
    # pprint(track)
    # run_chain_example('Joris Delacroix')
