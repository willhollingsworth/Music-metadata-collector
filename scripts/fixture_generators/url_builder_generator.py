"""Build test fixtures for the ApiUrlBuilder class.

uses the URL_ARGS_FORMAT dict to generate all possible URL args
"""

from utils import random_string, write_json_fixture

from mmc.utils.url_builder import URL_ARGS_FORMAT, ApiUrlBuilder


def load_all_url_args() -> list[tuple[str, str, str, int]]:
    """Load all URL args from the URL_ARGS_FORMAT dict.

    Returns:
        list[tuple[str, str, str, int]]: A list of tuples containing:
            - service_name: str
            - request_type: str
            - resource_type: str
            - resource_count: int (number of {} in the URL)

    """
    all_args: list[tuple[str, str, str, int]] = []
    for service_name, request_types in URL_ARGS_FORMAT.items():
        for request_type, resource_type in request_types.items():
            for resource, url in resource_type.items():
                resource_count = url.count("{}")
                all_args.append((service_name, request_type, resource, resource_count))
    return all_args


def loop_over_all_args(
    all_args: list[tuple[str, str, str, int]],
) -> list[tuple[str, str, str, list[str], str]]:
    """Loop over all URL args and format them.

    Returns:
        list[tuple[str, str, str, list[str], str]]: A list of tuples containing:
            - service_name: str
            - request_type: str
            - resource_type: str
            - resources: list[str] (random strings)
            - expected completed url: str

    """
    all_fixtures: list[tuple[str, str, str, list[str], str]] = []
    for service_name, request_type, resource_type, resource_count in all_args:
        # build random strings
        random_args: list[str] = [random_string() for _ in range(resource_count)]
        fixture_data = (
            service_name,
            request_type,
            resource_type,
            random_args,
            ApiUrlBuilder(
                service_name,
                request_type,
                resource_type,
                random_args,
            ).full_url,
        )
        all_fixtures.append(fixture_data)
    return all_fixtures


def main() -> None:
    """Run the fixture builder main function."""
    print("Running fixture builder...")
    all_args = load_all_url_args()
    print(f"Loaded {len(all_args)} URL args.")
    fixtures_data = loop_over_all_args(all_args)
    print(f"Generated data for {len(fixtures_data)} fixtures.")
    fixtures_path = "url_builder_fixtures.json"
    print(f"Writing fixtures to {fixtures_path}")
    write_json_fixture(fixtures_data, fixtures_path)


if __name__ == "__main__":
    print("Running directly")
    main()
