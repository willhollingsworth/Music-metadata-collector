import json
from pathlib import Path
from typing import Any
import MMC.Services.deezer as deezer

FIXTURE_DIR = Path('tests/fixtures/deezer/')
EXPECTED_FILENAME_PREFIX = '_expected'
LOOKUP_FUNCTION_SUFFIX = 'lookup_'

def generate_deezer_fixtures(type: str, id: int) -> None:
    # Generate a fixture from Deezer's API response.
    api_response = deezer.download_deezer_data(type, str(id))
    if isinstance(api_response, list):
        api_response = deezer.get_first_track(api_response)
    path = FIXTURE_DIR / type / f'{id}.json'
    write_json_fixture(api_response, path)
    print(f'Fixture written to {path}')
    # Generate expected outcome from the lookup function.
    lookup_function = getattr(deezer, f'{LOOKUP_FUNCTION_SUFFIX}{type}', None)
    if lookup_function is None:
        raise ValueError(f'No lookup function found for "{LOOKUP_FUNCTION_SUFFIX}{type}"')
    expected_response = lookup_function(str(id))
    expected_path = FIXTURE_DIR / type / f'{id}{EXPECTED_FILENAME_PREFIX}.json'
    write_json_fixture(expected_response, expected_path)
    print(f'Fixture written to {expected_path}')

def write_json_fixture(data: dict[str, Any], path: Path) -> None:
    """Write a JSON fixture to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    # open the deezer_fixture_ids.json as json object
    with open('scripts/deezer_fixture_ids.json') as file:
        ids = json.load(file)
        for type, id_list in ids.items():
            for id in id_list:
                print(f'Generating fixture for {type} {id}')
                generate_deezer_fixtures(type, id)
    print('All fixtures generated successfully.')
        
