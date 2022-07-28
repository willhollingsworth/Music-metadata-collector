import requests
import pandas as pd
import sp_playcount_funcs as spp

public_url = 'https://api.t4ils.dev/'


tracks = spp.list_tracks_from_album('4UrHb1pIbKLFev4nuxMFUY')
df = pd.DataFrame(data=tracks)
print('rows, columns :', df.shape)
print(df)
