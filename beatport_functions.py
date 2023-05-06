import json
import requests
import bs4
import utility_functions


# api key request link is currently broken
# will use scraping instead


def beatport_download_data(input):
    beatport_api_url = 'https://api.beatport.com/v4/catalog'
    full_url = beatport_api_url + input
    return utility_functions.download_data(full_url)


def run_tests():
    return beatport_download_data('/tracks/?artist_name=dynoro')


if __name__ == '__main__':
    print(run_tests())
