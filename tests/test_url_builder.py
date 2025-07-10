"""test for URLBuilder class"""

import pytest

from mmc.constants import TEST_FIXTURE_DIR
from mmc.utils import url_builder
from tests.utils.fixtures import load_json_fixture

# Load url_tests from JSON fixture file
fixture_path = TEST_FIXTURE_DIR / "url_builder_fixtures.json"
url_tests = load_json_fixture(fixture_path)


@pytest.mark.parametrize(
    ("service_name", "request_type", "request_resource", "url_args", "expected_url"),
    url_tests,
)
def test_api_builder(
    service_name: str,
    request_type: str,
    request_resource: str,
    url_args: list[str],
    expected_url: str,
) -> None:
    url_result = url_builder.ApiUrlBuilder(
        service_name=service_name,
        request_type=request_type,
        request_resource=request_resource,
        url_args=url_args,
    )
    assert url_result.full_url == expected_url


if __name__ == "__main__":
    print("running tests directly")
    pytest.main(["-v", __file__])
    print("All tests run")
