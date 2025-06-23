"""testing deezer lookups."""

from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import pytest

from MMC.constants import (
    LOOKUP_FUNCTION_SUFFIX,
)
from MMC.Services import deezer
from tests.utils.fixtures import load_json_fixture, load_json_listing, read_folder_names

SERVICE_NAME = "deezer"

# Define type aliases for readability
LookupFunc = Callable[[str], dict[str, Any]]
PytestParam = tuple[str, LookupFunc]


def build_targets(folder: str) -> list[str]:
    """Build a list of targets, should be lookups funcs of that service.

    Can be read from the folder names as fixture generation should have created
    a folder for each lookup function.
    """
    return read_folder_names(folder=folder)


def build_pytest_parameters(service: str) -> list[PytestParam]:
    """Build a list of parameters for pytest."""
    targets = build_targets(folder=service)
    folders = [f"{service}/{target}" for target in targets]
    lookup_functions = [
        getattr(deezer, f"{LOOKUP_FUNCTION_SUFFIX}{target}") for target in targets
    ]
    return list(zip(folders, lookup_functions, strict=False))


@pytest.mark.parametrize(
    ("folder", "lookup_func"),
    build_pytest_parameters(SERVICE_NAME),
    ids=build_targets(SERVICE_NAME),
)
def test_lookup_success(folder: str, lookup_func: LookupFunc) -> None:
    for mock_path, expected_path in load_json_listing(folder=folder):
        mock_data = load_json_fixture(mock_path)
        expected_result = load_json_fixture(expected_path)
        with patch(
            "MMC.Services.deezer.download_json",
            return_value=mock_data,
        ) as mock_download_json:
            result = lookup_func(mock_data["id"])
            mock_download_json.assert_called_once()
            assert result == expected_result


if __name__ == "__main__":
    # allow direct running of this script
    pytest.main(["-v", __file__])
    print("Tests completed.")
