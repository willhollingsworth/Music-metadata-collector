from mmc.utils.http_client import download_json

# api key request link is currently broken
# could use web scraping
# api workaround example : https://github.com/Samik081/beets-beatport4


def beatport_download_data(input):
    beatport_api_url = "https://api.beatport.com/v4/catalog"
    full_url = beatport_api_url + input
    return download_json(full_url)


def run_tests():
    return beatport_download_data("/tracks/?artist_name=dynoro")


if __name__ == "__main__":
    print(run_tests())
