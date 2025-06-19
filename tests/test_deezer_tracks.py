from unittest.mock import patch
import pytest
from MMC.Services.deezer import lookup_track, lookup_track_detailed


def test_lookup_track_success():
    fake_track = {'id': '123', 'title': 'Test Track'}
    with patch(
        'MMC.Services.deezer.download_json',
        return_value=fake_track,
    ) as mock_download_json:
        result = lookup_track('123')
        mock_download_json.assert_called_once()
        assert result == fake_track


def test_lookup_track_detailed_success() -> None:
    fake_track = {
        'title': 'Test Song',
        'id': '1',
        'artist': {'name': 'Test Artist', 'id': '10'},
        'album': {'title': 'Test Album', 'id': '100'},
    }
    fake_album = {'genres': {'data': [{'name': 'Electronic'}]}}

    with patch('MMC.Services.deezer.lookup_track', return_value=fake_track), \
         patch('MMC.Services.deezer.lookup_album', return_value=fake_album):
        result = lookup_track_detailed('1')
        assert result['track name'] == 'Test Song'
        assert result['album genres'] == ['Electronic']


def test_lookup_track_detailed_fail() -> None:
    with patch('MMC.Services.deezer.lookup_track', side_effect=KeyError("id")), \
         pytest.raises(KeyError):
        lookup_track_detailed('bad_id')
