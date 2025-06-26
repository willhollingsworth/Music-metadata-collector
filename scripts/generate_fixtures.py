"""Script to generate Deezer API fixtures and expected lookup results for testing."""

import json
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from typing import Any

import mmc
from mmc.constants import (
    EXPECTED_FILENAME_PREFIX,
    LOOKUP_FUNCTION_SUFFIX,
    TEST_FIXTURE_DIR,
)
from mmc.services.deezer.api_requests import (
    request_lookup as deezer_data_lookup,  # noqa: F401
)
from mmc.services.spotify.api_requests import (
    request_lookup as spotify_data_lookup,  # noqa: F401
)


class generate_fixture:
    """Generate a fixture."""

    def __init__(
        self,
        service_name: str,
        fixture_type: str,
        fixture_id: str | int,
    ) -> None:
        self.service_name = service_name
        self.fixture_type = fixture_type
        self.fixture_id = fixture_id
        self.fixture_type_folder = TEST_FIXTURE_DIR / service_name / fixture_type
        self.generate_raw_api_response()
        self.generate_expected_lookup_response()

    def generate_raw_api_response(self) -> None:
        """Generate a raw API response fixture.

        Raises:
            TypeError: If the API response is not a dictionary.

        """
        download_function_name = f"{self.service_name}_data_lookup"
        download_function = globals().get(download_function_name)
        if not isinstance(download_function, Callable):
            msg = f'No download function found for "{download_function_name}"'
            raise TypeError(msg)
        api_response = download_function(self.fixture_type, self.fixture_id)
        api_file_path = self.fixture_type_folder / f"{self.fixture_id}.json"
        if not isinstance(api_response, dict):
            msg = f"API response needs to be a dict, got {type(api_response)}"
            raise TypeError(msg)
        write_json_fixture(api_response, api_file_path)
        print(f"Fixture written to {api_file_path}")

    def generate_expected_lookup_response(self) -> None:
        """Generate an expected lookup response fixture.

        Raises:
            ValueError: If no lookup function is found for the given type.

        """
        lookup_function_name = (
            f"{self.service_name}_{LOOKUP_FUNCTION_SUFFIX}{self.fixture_type}"
        )
        lookup_function = getattr(mmc, lookup_function_name)
        if lookup_function is None:
            msg = (
                f'No lookup function found for "'
                f'{LOOKUP_FUNCTION_SUFFIX}{self.fixture_type}"'
            )
            raise ValueError(msg)
        expected_response = asdict(lookup_function(self.fixture_id))
        expected_path = (
            self.fixture_type_folder
            / f"{self.fixture_id}{EXPECTED_FILENAME_PREFIX}.json"
        )
        write_json_fixture(expected_response, expected_path)
        print(f"Fixture written to {expected_path}")


def write_json_fixture(data: dict[str, Any], path: Path) -> None:
    """Write a JSON fixture to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def delete_deezer_fixtures() -> None:
    """Delete all files in the fixture dir."""
    for item in FIXTURE_FOLDER.iterdir():
        if item.is_dir():
            print(f"skipping folder {item}")
        else:
            item.unlink()


def service_setup(service_name: str) -> None:
    """Set up the fixture directory."""
    fixture_folder: Path = TEST_FIXTURE_DIR / service_name
    fixture_folder.mkdir(parents=True, exist_ok=True)


def loop_over_fixture_config(fixture_config_path: Path) -> None:
    """Loop over the fixture configuration file and generate fixtures."""
    with fixture_config_path.open(encoding="utf-8") as file:
        services = json.load(file)
        for service_name, types_list in services.items():
            print(f"Generating fixtures for {service_name}")
            service_setup(service_name)
            for type_name, id_list in types_list.items():
                for id_number in id_list:
                    print(
                        f"Generating fixture for {service_name} {type_name} {id_number}",
                    )
                    generate_fixture(
                        service_name=service_name,
                        fixture_type=type_name,
                        fixture_id=id_number,
                    )


if __name__ == "__main__":
    """Main function to generate Deezer fixtures based on predefined IDs."""
    fixture_ids_path = Path("scripts/fixture_ids.json")
    loop_over_fixture_config(fixture_ids_path)
    # Delete existing fixtures
    # delete_deezer_fixtures()
    # open the deezer_fixture_ids.json as json object

    #         for fixture_id in id_list:
    #             print(f"Generating fixture for {fixture_type} {fixture_id}")
    #             generate_deezer_lookup_fixtures(fixture_type, fixture_id)
    # print("All fixtures generated successfully.")
