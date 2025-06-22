"""Constants used throught the project."""
from pathlib import Path

VALID_SERVICE_NAMES: list[str] = [
    'deezer',
    'spotify',
]
VALID_LOOKUP_TYPES: list[str] = [
    'album',
    'artist',
    'track',
]

TEST_DIR: Path = Path('tests')
TEST_FIXTURE_DIR: Path = TEST_DIR / 'fixtures'
EXPECTED_FILENAME_PREFIX: str = '_expected'

LOOKUP_FUNCTION_SUFFIX: str = 'lookup_'
