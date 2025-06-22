"""Utility functions for loading JSON fixtures in tests."""
import json
from pathlib import Path
from typing import Any


def load_json_fixture(full_path: Path) -> dict[str, Any]:
    """Load a JSON fixture file. full_path should include forward slashes.

    Raises:
        FileNotFoundError: If the fixture file does not exist or is not a file.

    """
    with full_path.open('r', encoding='utf-8') as file:
        # Ensure the file exists
        if not full_path.exists() or not full_path.is_file():
            msg = f"Fixture file {full_path} does not exist or is not a file."
            raise FileNotFoundError(msg)
        return json.load(file)


def load_json_listing(folder: str) -> list[tuple[Path, Path]]:
    """Provide a listing of JSON files in a folder.

    Raises:
        NotADirectoryError: If the specified folder is not a directory.

    """
    folder_path = Path('tests', 'fixtures', folder)
    if not folder_path.is_dir():
        msg = f"{folder_path} is not a directory."
        raise NotADirectoryError(msg)
    standard_files = [
        f for f in folder_path.glob('*.json') if not f.name.endswith('_expected.json')
        ]
    expected_files = folder_path.glob('*_expected.json')
    return list(zip(standard_files, expected_files, strict=False))


def read_folder_names(folder: str) -> list[str]:
    """Read folder names from a given folder.

    Raises:
        NotADirectoryError: If the specified folder is not a directory.

    """
    folder_path = Path('tests', 'fixtures', folder)
    if not folder_path.is_dir():
        msg = f"{folder_path} is not a directory."
        raise NotADirectoryError(msg)
    return [f.name for f in folder_path.iterdir() if f.is_dir()]


if __name__ == "__main__":
    # Example json fixture loading
    path = Path('tests/fixtures/deezer/tracks/2582922142.json')
    fixture_data = load_json_fixture(path)
    print(fixture_data)
    # Example usage for listing JSON files in a folder
    folder = 'deezer/tracks'
    json_files = load_json_listing(folder)
    for standard, expected in json_files:
        print(standard)
        print(expected)
