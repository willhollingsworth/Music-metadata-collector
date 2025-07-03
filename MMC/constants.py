"""Constants used throught the project."""

from pathlib import Path

VALID_SERVICE_NAMES: list[str] = [
    "deezer",
    "spotify",
]
VALID_LOOKUP_TYPES: list[str] = [
    "album",
    "artist",
    "track",
]

TEST_DIR: Path = Path("tests")
TEST_FIXTURE_DIR: Path = TEST_DIR / "fixtures"
EXPECTED_FILENAME_PREFIX: str = "_expected"
CACHE_FOLDER: Path = Path("http_cache")
LOOKUP_FUNCTION_SUFFIX: str = "lookup_"
SPOTIFY_API_URL = "https://api.spotify.com/v1/"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"
MUSIC_BRAINZ_API_URL = "https://musicbrainz.org/ws/2/"
DEEZER_API_URL = "https://api.deezer.com/"
