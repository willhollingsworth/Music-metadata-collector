"""Utility functions for loading JSON fixtures in tests."""
import json
from pathlib import Path
from typing import Any


def load_json_fixture(full_path: str) -> dict[str, Any]:
    """Load a JSON fixture file. full_path should include forward slashes.

    Raises:
        FileNotFoundError: If the fixture file does not exist or is not a file.

    """
    final_path = Path('tests', 'fixtures', full_path).with_suffix('.json')
    with final_path.open('r', encoding='utf-8') as file:
        # Ensure the file exists
        if not final_path.exists() or not final_path.is_file():
            msg = f"Fixture file {final_path} does not exist or is not a file."
            raise FileNotFoundError(msg)
        return json.load(file)


if __name__ == "__main__":
    # Example usage
    path = 'deezer/tracks/395141722'
    fixture_data = load_json_fixture(path)
    print(fixture_data)
