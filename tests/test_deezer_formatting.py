import pytest

from MMC.Services.deezer import build_search_args


def test_build_search_args_all_empty():
    assert build_search_args('', '', '') == ''


def test_build_search_args_search_string_only():
    assert build_search_args('hello', '', '') == 'hello'


def test_build_search_args_artist_only():
    assert build_search_args('', 'Daft Punk', '') == 'artist:"Daft Punk"'


def test_build_search_args_track_only():
    assert build_search_args('', '', 'One More Time') == 'track:"One More Time"'


def test_build_search_args_search_and_artist():
    assert build_search_args('discovery', 'Daft Punk', '') == 'discovery artist:"Daft Punk"'


def test_build_search_args_search_and_track():
    assert build_search_args(
        'discovery', '', 'One More Time',
    ) == 'discovery track:"One More Time"'


def test_build_search_args_artist_and_track():
    assert build_search_args(
        '', 'Daft Punk', 'One More Time',
    ) == 'artist:"Daft Punk" track:"One More Time"'


def test_build_search_args_all_fields():
    assert build_search_args(
        'discovery', 'Daft Punk', 'One More Time',
        ) == 'discovery artist:"Daft Punk" track:"One More Time"'
