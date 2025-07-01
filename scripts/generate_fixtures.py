"""Script to generate Deezer API fixtures and expected lookup results for testing."""

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import mmc
from mmc.constants import (
    EXPECTED_FILENAME_PREFIX,
    LOOKUP_FUNCTION_SUFFIX,
    TEST_FIXTURE_DIR,
)
from mmc.utils.cache import load_cache_file

# recreated lookup logic in this file


class GenerateFixture:
    """Generate a fixture."""

    def __init__(
        self,
        service_name: str,
        fixture_type: str,
        fixture_args: list[str],
        # TODO(Will): correctly support multiple args
    ) -> None:
        """Initialize the GenerateFixture class.

        Args:
            service_name (str): The name of the service.
            fixture_type (str): The type of fixture to generate.
            fixture_args (list[str]): Arguments for the fixture.

        """
        self.service_name = service_name
        self.fixture_type = fixture_type
        self.fixture_args = fixture_args
        self.fixture_args_str = "_".join(self.fixture_args)
        self.fixture_type_folder = TEST_FIXTURE_DIR / service_name / fixture_type
        self.generate_expected_lookup_response()
        self.generate_raw_api_response()

    def generate_raw_api_response(self) -> None:
        """Generate a raw API response fixture.

        Loads the api response from the cache and writes it to a JSON file.
        """
        api_response = load_cache_file(
            self.service_name,
            [self.fixture_type, *self.fixture_args],
        )
        api_file_path = self.fixture_type_folder / f"{self.fixture_args_str}.json"
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
        expected_response = asdict(lookup_function(*self.fixture_args))
        expected_path = (
            self.fixture_type_folder
            / f"{self.fixture_args_str}{EXPECTED_FILENAME_PREFIX}.json"
        )
        write_json_fixture(expected_response, expected_path)
        print(f"Fixture written to {expected_path}")


def write_json_fixture(data: dict[str, Any], path: Path) -> None:
    """Write a JSON fixture to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def delete_all_fixtures() -> None:
    """Delete all files in the fixture dir."""
    for item in TEST_FIXTURE_DIR.iterdir():
        if item.is_dir():
            print(f"skipping folder {item}")
        else:
            item.unlink()


def service_setup(service_name: str) -> None:
    """Set up the fixture directory."""
    fixture_folder: Path = TEST_FIXTURE_DIR / service_name
    fixture_folder.mkdir(parents=True, exist_ok=True)


def loop_over_fixture_config(fixture_config_path: Path) -> None:
    """Loop over the fixture configuration file and generate fixtures.

    Raises:
        TypeError: If a fixture argument is not a list or string.

    """
    with fixture_config_path.open(encoding="utf-8") as file:
        services = json.load(file)
        for service_name, types_list in services.items():
            print(f"Generating fixtures for {service_name}")
            service_setup(service_name)
            for type_name, fixture_test_list in types_list.items():
                for fixture_args in fixture_test_list:
                    processed_args: list[str]
                    if isinstance(fixture_args, list):
                        processed_args = [str(arg) for arg in fixture_args]  # type: ignore[var-annotated]
                    elif isinstance(fixture_args, str):
                        processed_args = [str(fixture_args)]
                    else:
                        msg = (
                            "Fixture must be list or str, instead it's "
                            f"{type(fixture_args)}"
                        )
                        raise TypeError(msg)
                    print(
                        f"Generating fixture for {service_name} ",
                        f"{type_name} {fixture_args}",
                    )
                    GenerateFixture(
                        service_name=service_name,
                        fixture_type=type_name,
                        fixture_args=processed_args,
                    )


if __name__ == "__main__":
    """Main function to generate Deezer fixtures based on predefined IDs."""
    fixture_ids_path = Path("scripts/fixture_ids.json")
    loop_over_fixture_config(fixture_ids_path)
    # Delete existing fixtures
    # delete_deezer_fixtures()
