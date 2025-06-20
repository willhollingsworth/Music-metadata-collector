"""Unit tests for Deezer track lookup functionality."""
from unittest.mock import patch
from pathlib import Path
import pytest

from MMC.Services.deezer import lookup_track, lookup_track_genres
from tests.utils.fixtures import load_json_fixture, load_json_listing


@pytest.mark.parametrize(
    ("mock_path", "expected_path"),
    load_json_listing(folder="deezer/tracks")  # Replace with the correct folder path as needed
)
def test_lookup_track_success(mock_path: Path, expected_path: Path) -> None:
    mock_track_data = load_json_fixture(mock_path)
    expected_track_result = load_json_fixture(expected_path)
    with patch(
        'MMC.Services.deezer.download_json',
        return_value=mock_track_data,
    ) as mock_download_json:
        result = lookup_track(mock_track_data['id'])
        mock_download_json.assert_called_once()
        assert result == expected_track_result


# def test_lookup_track_detailed_success() -> None:
#     track_id = '395141722'
#     album_id = '523121232'
#     mock_track_data = load_json_fixture('deezer/tracks/' + track_id)
#     mock_album_data = load_json_fixture('deezer/albums/' + album_id)
#     with patch('MMC.Services.deezer.lookup_track', return_value=mock_track_data), \
#          patch('MMC.Services.deezer.lookup_album', return_value=mock_album_data):
#         result = lookup_track_genres(track_id)
#         print(result)
#         assert result == ['Electro']


def test_lookup_track_detailed_fail() -> None:
    with patch('MMC.Services.deezer.lookup_track', side_effect=KeyError("id")), \
         pytest.raises(KeyError):
        lookup_track_genres('bad_id')


if __name__ == "__main__":
    pytest.main([__file__])
