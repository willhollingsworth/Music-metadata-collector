import requests
import os


def list_tracks_from_album(album_id):
    # add caching to reduce api load + decrease repeated processing time
    # save data locally
    output_list = []
    public_url = 'https://api.t4ils.dev/'
    url = public_url + 'albumPlayCount?albumid=' + album_id
    r = requests.get(url)
    r = r.json()['data']
    for disc in r['discs']:
        for track in disc['tracks']:
            output_list.append(
                {'Track Name': track['name'], 'Track Playcount': track['playcount']})
    return output_list


def list_albums_from_artist(artist_id):
    public_url = 'https://api.t4ils.dev/'
    url = public_url + 'artistInfo?artistid=' + artist_id
    r = requests.get(url)
    r = r.json()
    output_list = []

    albums = r['data']['releases']
    full_albums = albums['albums']['releases']
    for album in full_albums:
        album_uri = album['uri'].replace('spotify:album:', '')
        output_list.append(
            {'Album Name': album['name'], 'Album URI': album_uri})
        # print(album['name'],album['uri'].replace('spotify:album:',''))
        # track_list = tracks_list + (grab_tracks_from_album(album_uri))
        # print(album.keys())
        # if len(album['discs']) == 0:
        #     print(album)
        #     continue
        # for disc in album['discs']:
        #     for track in disc['tracks']:
        #         tracks_list.append(track['name'])
    return output_list


if __name__ == '__main__':
    print(list_albums_from_artist('4aEnNH9PuU1HF3TsZTru54'))
    # print(list_tracks_from_album('4UrHb1pIbKLFev4nuxMFUY'))
