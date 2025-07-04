from mmc.utils.http_client import download_json


def download_data(request_type, id):
    public_url = "https://api.t4ils.dev/"
    # no longer working as the publix api has been shut down
    # could explore running it locally via
    # https://github.com/entriphy/sp-playcount-librespot
    if request_type == "album_playcount":
        request_url = "albumPlayCount?albumid="
    elif request_type == "artist_info":
        request_url = "artistInfo?artistid="
    else:
        raise Exception("wrong type selected", locals())
    full_url = public_url + request_url + id
    return download_json(full_url)


def list_tracks_from_album(album_id):
    output_list = []
    data = download_data("album_playcount", album_id)

    for disc in data["discs"]:
        for track in disc["tracks"]:
            output_list.append({
                "Track Name": track["name"],
                "Track Playcount": track["playcount"],
            })
    return output_list


def list_albums_from_artist(artist_id):
    output_list = []
    r = download_data("artist_info", artist_id)
    albums = r["releases"]
    full_albums = albums["albums"]["releases"]
    for album in full_albums:
        album_uri = album["uri"].replace("spotify:album:", "")

        if "discs" in album.keys():
            discs = len(album["discs"])
        else:
            discs = 0
        output_list.append({
            "Album Name": album["name"],
            "Album URI": album_uri,
            "Discs": discs,
        })

    return output_list


if __name__ == "__main__":
    print(list_albums_from_artist("4aEnNH9PuU1HF3TsZTru54"))
    print(list_tracks_from_album("4UrHb1pIbKLFev4nuxMFUY"))
