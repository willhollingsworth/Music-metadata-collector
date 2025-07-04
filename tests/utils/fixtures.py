"""Utility functions for loading JSON fixtures in tests."""

import json
from pathlib import Path
from typing import Any

from mmc.constants import EXPECTED_FILENAME_PREFIX, TEST_FIXTURE_DIR


def load_json_fixture(full_path: Path) -> dict[str, Any]:
    """Load a JSON fixture file. full_path should include forward slashes.

    Raises:
        FileNotFoundError: If the fixture file does not exist or is not a file.

    """
    with full_path.open("r", encoding="utf-8") as file:
        # Ensure the file exists
        if not full_path.exists() or not full_path.is_file():
            msg = f"Fixture file {full_path} does not exist or is not a file."
            raise FileNotFoundError(msg)
        return json.load(file)


def get_raw_json_filnames(folder: str) -> list[str]:
    """Get a list of filename of the raw(not expected) filenames in a folder.

    Raises:
        NotADirectoryError: If the specified folder is not a directory.

    """
    folder_path = TEST_FIXTURE_DIR / folder
    if not folder_path.is_dir():
        msg = f"{folder_path} is not a directory."
        raise NotADirectoryError(msg)
    return [
        f.stem
        for f in folder_path.glob("*.json")
        if not f.name.endswith("_expected.json")
    ]


def load_json_listing(folder: str) -> list[tuple[Path, Path]]:
    """Provide a listing of JSON files in a folder.

    Raises:
        NotADirectoryError: If the specified folder is not a directory.

    """
    folder_path = TEST_FIXTURE_DIR / folder
    if not folder_path.is_dir():
        msg = f"{folder_path} is not a directory."
        raise NotADirectoryError(msg)
    standard_files = [
        f for f in folder_path.glob("*.json") if not f.name.endswith("_expected.json")
    ]
    expected_files = folder_path.glob(f"*{EXPECTED_FILENAME_PREFIX}.json")
    return list(zip(standard_files, expected_files, strict=False))


def read_folder_names(folder: str | Path) -> list[str]:
    """Read folder names from a given folder.

    Raises:
        NotADirectoryError: If the specified folder is not a directory.

    """
    folder_path = TEST_FIXTURE_DIR / folder if isinstance(folder, str) else folder
    if not folder_path.is_dir():
        msg = f"{folder_path} is not a directory."
        raise NotADirectoryError(msg)
    return [f.name for f in folder_path.iterdir() if f.is_dir()]


if __name__ == "__main__":
    # Example json fixture loading
    service_name = "deezer"
    folder = read_folder_names(service_name)[0]
    full_folder_path = f"{service_name}/{folder}"
    file = get_json_file_pairs(full_folder_path)[0][1]
    print(load_json_fixture(file))

    # Example usage for listing JSON files in a folder
    json_files = get_json_file_pairs(full_folder_path)
    for standard, expected in json_files:
        print(standard)
        print(expected)
