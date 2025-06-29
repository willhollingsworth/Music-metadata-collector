from mmc.services.last_fm.api_request import request_search


def search_tracks(track):
    # https://www.last.fm/api/show/track.search
    return request_search("track.search", "track=" + track)
