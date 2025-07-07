"""test for URLBuilder class"""

from typing import Any

import pytest

from mmc.utils import url_builder

# list used to test the URLBuilder class
# format is service_name, request_type, request_resource, url_args, expected url result
url_tests: list[tuple[str, str, str, str | tuple[str, Any], str]] = [
    ("deezer", "lookup", "album", "123456", "https://api.deezer.com/album/123456"),
    (
        "deezer",
        "search",
        "album",
        ("ABC", "ZXY"),
        'https://api.deezer.com/search/album?q=album:"ABC" "artist:"ZXY"',
    ),
    ("spotify", "lookup", "album", "55424", "https://api.spotify.com/v1/albums/55424"),
    (
        "spotify",
        "search",
        "artist",
        "ABCD",
        "https://api.spotify.com/v1/search?type=artist&q=ABCD",
    ),
    (
        "music_brainz",
        "lookup",
        "track",
        "FooBar",
        "https://musicbrainz.org/ws/2/recording/FooBar?inc=artists+releases&fmt=json",
    ),
]


@pytest.mark.parametrize(
    ("service_name", "request_type", "request_resource", "url_args", "expected_url"),
    url_tests,
)
def test_api_builder(
    service_name: str,
    request_type: str,
    request_resource: str,
    url_args: str,
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
    # helper to populate list
    # test_data = ("music_brainz", "lookup", "track", "FooBar")
    # print(url_builder.ApiUrlBuilder(*test_data).full_url)
