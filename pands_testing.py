import requests
import pandas as pd
import sp_playcount_funcs as spp

public_url = 'https://api.t4ils.dev/'


def build_df(in_data):
    df = pd.DataFrame(data=in_data)
    print('rows, columns :', df.shape)
    print(df)


if __name__ == '__main__':
    build_df(spp.list_tracks_from_album('4UrHb1pIbKLFev4nuxMFUY'))
