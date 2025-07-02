"""testing lookups."""

import importlib
from collections.abc import Callable
from dataclasses import asdict
from unittest.mock import patch

import pytest

from mmc.constants import (
    TEST_FIXTURE_DIR,
)
from mmc.types.deezer_types import DeezerEntity
from tests.utils.fixtures import (
    get_raw_json_filnames,
    load_json_fixture,
    read_folder_names,
)
from tests.utils.functions import count_args

# Define type aliases for readability
LookupFunc = Callable[[str], DeezerEntity]
PytestParam = tuple[str, str, str]


def build_lookup_types(service: str) -> list[str]:
    """Build a list of targets, should be lookups funcs of that service.

    Can be read from the folder names as fixture generation should have created
    a folder for each lookup function.
    """
    return read_folder_names(folder=service)


def build_service_names() -> list[str]:
    """Build a list of service names.

    Based of folders already created by the fixture generator.
    """
    return read_folder_names(folder=TEST_FIXTURE_DIR)


def build_pytest_parameters() -> list[PytestParam]:
    """Build a list of parameters for pytest.

    This will be used to parametrize the tests.
    Each parameter is a tuple of (service name, lookup type, id_value).
        Service name: The name of the service (e.g., 'deezer').
        Lookup type: The type of lookup (e.g., 'artist', 'album').
        Id_value: The ID value to be looked up (e.g., '123456').
    """
    pytest_parameters: list[PytestParam] = []
    services = build_service_names()
    for service in services:
        lookup_types = build_lookup_types(service=service)
        for lookup_type in lookup_types:
            raw_json_filenames = get_raw_json_filnames(
                folder=f"{service}/{lookup_type}",
            )
            for filename in raw_json_filenames:
                pytest_tuple = (service, lookup_type, filename)
                pytest_parameters.append(pytest_tuple)
    return pytest_parameters


@pytest.mark.parametrize(
    ("service_name", "lookup_type", "id_value"),
    build_pytest_parameters(),
)
def test_lookup_success(service_name: str, lookup_type: str, id_value: str) -> None:
    """Test that the lookup function returns the expected result.

    Uses parametrized arguments to allow testing of multiple services and lookup types.

    Raises:
        ValueError: If the lookup function is not found in the specified module.

    """
    # Setup fixture paths
    fixture_folder = TEST_FIXTURE_DIR / service_name / lookup_type
    api_response_fullpath = fixture_folder / f"{id_value}.json"
    expected_response_fullpath = fixture_folder / f"{id_value}_expected.json"
    # Get fixture data
    mock_api_data = load_json_fixture(api_response_fullpath)
    expected_result = load_json_fixture(expected_response_fullpath)
    # setup function variables
    api_func_name = "request_lookup"
    api_func_path = f"mmc.services.{service_name}.lookups.{api_func_name}"
    lookup_func_name = f"lookup_{lookup_type}"
    lookup_module_path = f"mmc.services.{service_name}.lookups"
    try:
        lookup_module = importlib.import_module(lookup_module_path)
        lookup_func = getattr(lookup_module, lookup_func_name)
    except (ModuleNotFoundError, AttributeError) as err:
        msg = f"Function '{lookup_func_name}' not found in {lookup_module_path}"
        raise ValueError(msg) from err
    lookup_func_arg_count = count_args(lookup_func)
    dummy_lookup_args = [""] * lookup_func_arg_count
    # confirm lookup matches expected results
    with patch(api_func_path, return_value=mock_api_data):
        result = asdict(lookup_func(*dummy_lookup_args))
        assert result == expected_result


if __name__ == "__main__":
    # allow direct running of this script
    pytest.main(["-v", __file__])
    print("Tests completed.")
