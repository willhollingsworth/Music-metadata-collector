import json
from pathlib import Path
from typing import Any
from MMC.Services.deezer import download_deezer_data, lookup_track, get_first_track, lookup_album

FIXTURE_DIR = Path('tests/fixtures/deezer/')

def generate_track_fixtures(track_id: str) -> None:
    """Generate json response for a Deezer track lookup."""
    track = download_deezer_data('track', track_id)
    if isinstance(track, list):
        track = get_first_track(track)
    path = Path('tracks') / f'{track_id}.json'
    write_json_fixture(track, path)

def generate_track_fixtures_expected(track_id: str) -> None:
    """Generate expected fixture for a track."""
    track = lookup_track(track_id)
    path = Path('tracks') / f'{track_id}_expected.json'
    write_json_fixture(track, path)

def generate_album_fixtures(album_id: str) -> None:
    """Generate json response for a Deezer album lookup."""
    album = download_deezer_data('album', album_id)
    path = Path('albums') / f'{album_id}.json'
    write_json_fixture(album, path)

def generate_album_fixtures_expected(album_id: str) -> None:
    """Generate expected fixture for an album."""
    album = lookup_album(album_id)
    path = Path('albums') / f'{album_id}_expected.json'
    write_json_fixture(album, path)

def write_json_fixture(data: dict[str, Any], path: Path) -> None:
    """Write a JSON fixture to a file."""
    full_path = FIXTURE_DIR / path
    with open(full_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    track_ids = [
        '2582922142',  
        '2582922152',
    ]
    
    album_ids = [
        '523121232',
        '7933290'
    ]

    for track_id in track_ids:
        generate_track_fixtures(track_id)
        generate_track_fixtures_expected(track_id)

    for album_id in album_ids:
        generate_album_fixtures(album_id)
        generate_album_fixtures_expected(album_id)