"""Unit tests for all Deezer lookup functionality."""
from unittest.mock import patch
from pathlib import Path
import pytest

import MMC.Services.deezer as deezer
from tests.utils.fixtures import load_json_fixture, load_json_listing


@pytest.mark.parametrize(
    ("mock_path", "expected_path"),
    load_json_listing(folder="deezer/artist")
)
def test_lookup_artist_success(mock_path: Path, expected_path: Path) -> None:
    mock_artist_data = load_json_fixture(mock_path)
    expected_artist_result = load_json_fixture(expected_path)
    with patch(
        'MMC.Services.deezer.download_json',
        return_value=mock_artist_data,
    ) as mock_download_json:
        result = deezer.lookup_artist(mock_artist_data['id'])
        mock_download_json.assert_called_once()
        assert result == expected_artist_result


@pytest.mark.parametrize(
    ("mock_path", "expected_path"),
    load_json_listing(folder="deezer/album")
)
def test_lookup_album_success(mock_path: Path, expected_path: Path) -> None:
    mock_album_data = load_json_fixture(mock_path)
    expected_album_result = load_json_fixture(expected_path)
    with patch(
        'MMC.Services.deezer.download_json',
        return_value=mock_album_data,
    ) as mock_download_json:
        result = deezer.lookup_album(mock_album_data['id'])
        mock_download_json.assert_called_once()
        assert result == expected_album_result

@pytest.mark.parametrize(
    ("mock_path", "expected_path"),
    load_json_listing(folder="deezer/track")  # Replace with the correct folder path as needed
)
def test_lookup_track_success(mock_path: Path, expected_path: Path) -> None:
    mock_track_data = load_json_fixture(mock_path)
    expected_track_result = load_json_fixture(expected_path)
    with patch(
        'MMC.Services.deezer.download_json',
        return_value=mock_track_data,
    ) as mock_download_json:
        result = deezer.lookup_track(mock_track_data['id'])
        mock_download_json.assert_called_once()
        assert result == expected_track_result


if __name__ == "__main__":
    # allow direct running of this script
    pytest.main(["-v", __file__])