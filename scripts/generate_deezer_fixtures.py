"""Script to generate Deezer API fixtures and expected lookup results for testing."""

import json
from pathlib import Path
from typing import Any

from MMC.Services import deezer

FIXTURE_DIR = Path('tests/fixtures/deezer/')
EXPECTED_FILENAME_PREFIX = '_expected'
LOOKUP_FUNCTION_SUFFIX = 'lookup_'


def generate_deezer_fixtures(fixture_type: str, fixture_id: int) -> None:
    """Generate a fixture from Deezer's API response.

    Raises:
        ValueError: If no lookup function is found for the given type.

    """
    api_response = deezer.download_deezer_data(fixture_type, str(fixture_id))
    if isinstance(api_response, list):
        api_response = deezer.get_first_track(api_response)
    path = FIXTURE_DIR / fixture_type / f'{fixture_id}.json'
    write_json_fixture(api_response, path)
    print(f'Fixture written to {path}')
    # Generate expected outcome from the lookup function.
    lookup_function = getattr(deezer, f'{LOOKUP_FUNCTION_SUFFIX}{fixture_type}', None)
    if lookup_function is None:
        msg = f'No lookup function found for "{LOOKUP_FUNCTION_SUFFIX}{fixture_type}"'
        raise ValueError(msg)
    expected_response = lookup_function(str(fixture_id))
    expected_path = (
        FIXTURE_DIR / fixture_type / f'{fixture_id}{EXPECTED_FILENAME_PREFIX}.json'
    )
    write_json_fixture(expected_response, expected_path)
    print(f'Fixture written to {expected_path}')


def write_json_fixture(data: dict[str, Any], path: Path) -> None:
    """Write a JSON fixture to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def delete_deezer_fixtures() -> None:
    """Deleta all folders in the fixture dir."""
    for item in FIXTURE_DIR.iterdir():
        if item.is_dir():
            for f in item.iterdir():
                f.unlink()
            print(f'Deleted folder {item}')
            item.rmdir()
        else:
            item.unlink()


if __name__ == '__main__':
    """Main function to generate Deezer fixtures based on predefined IDs."""
    # Delete existing fixtures
    delete_deezer_fixtures()
    # open the deezer_fixture_ids.json as json object
    fixture_ids_path = Path('scripts/deezer_fixture_ids.json')
    with fixture_ids_path.open(encoding='utf-8') as file:
        ids = json.load(file)
        for fixture_type, id_list in ids.items():
            for fixture_id in id_list:
                print(f'Generating fixture for {fixture_type} {fixture_id}')
                generate_deezer_fixtures(fixture_type, fixture_id)
    print('All fixtures generated successfully.')
