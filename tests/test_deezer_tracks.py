"""Unit tests for Deezer track lookup functionality."""
from unittest.mock import patch

import pytest

from MMC.Services.deezer import lookup_track, lookup_track_genres
from tests.utils.fixtures import load_json_fixture


def test_lookup_track_success() -> None:
    mock_track_data = load_json_fixture('deezer/tracks/395141722')
    expected_track_result = load_json_fixture('deezer/tracks/395141722_expected')
    with patch(
        'MMC.Services.deezer.download_json',
        return_value=mock_track_data,
    ) as mock_download_json:
        result = lookup_track('123')
        mock_download_json.assert_called_once()
        assert result == expected_track_result


def test_lookup_track_detailed_success() -> None:
    fake_track_output = {
        'track name': 'Test Track',
        'track id': '123',
        'artist name': 'Test Artist',
        'artist id': '456',
        'album name': 'Test Album',
        'album id': '789',
    }
    fake_album = {'genres': {'data': [{'name': 'Electronic'}]}}
    with patch('MMC.Services.deezer.lookup_track', return_value=fake_track_output), \
         patch('MMC.Services.deezer.lookup_album', return_value=fake_album):
        result = lookup_track_genres('123')
        assert result['track name'] == 'Test Track'
        assert result['album genres'] == 'Electronic'


def test_lookup_track_detailed_fail() -> None:
    with patch('MMC.Services.deezer.lookup_track', side_effect=KeyError("id")), \
         pytest.raises(KeyError):
        lookup_track_genres('bad_id')


if __name__ == "__main__":
    pytest.main([__file__])
