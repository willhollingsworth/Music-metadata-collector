"""Deezer API requests module."""

from typing import Any

from mmc.utils.http_client import download_json
from mmc.utils.url_builder import ApiUrlBuilder

# deezer's api docs are behind a login wall
# some public api docs https://apieco.ir/docs/deezer#api-Search-search
# also examples of use here https://github.com/deepjyoti30/ytmdl/blob/master/ytmdl/meta/deezer.py

DEEZER_API_URL = "https://api.deezer.com/"
SERVICE_NAME = "deezer"


def request_lookup(
    request_type: str,
    id_number: str,
) -> dict[str, Any] | list[Any]:
    """Run a Deezer API lookup."""
    url_builder = ApiUrlBuilder(
        service_name=SERVICE_NAME,
        request_type="lookup",
        request_resource=request_type,
        url_args=id_number,
    )
    return download_json(url_builder.full_url)
