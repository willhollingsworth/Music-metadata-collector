"""HTTP client utilities for downloading data."""

from __future__ import annotations

from typing import Any

import requests

from .cache import read_cache, write_cache


def download_json(
    url: str,
    headers: dict[str, str] | None = None,
) -> dict[str, Any] | list[dict[str, Any]]:
    """Download data from a URL and cache it locally.

    Args:
        url (str): The URL to download data from.
        headers (dict[str, str] | None): Optional headers to include in the request.

    Raises:
        ValueError: If the response data is empty or too small.

    """
    if headers is None:
        headers = {}
    # add the cache folder to the start of the cache path
    cache_data = read_cache(url)
    if not cache_data:
        response = requests.get(url, headers=headers)
        cache_data = response.json()
        if "data" in cache_data:
            cache_data = cache_data["data"]
        if len(cache_data) < 1:
            msg = f"Error, response too small: {cache_data}"
            raise ValueError(msg)
        write_cache(cache_data, url)
    return cache_data


"""

def download_html(
    url: str,
    headers: dict[str, str] | None = None,
    overwrite: bool = False,
    debug: bool = False,
) -> str:
    #Download HTML data from a URL and cache it locally.
    file_type = "html"
    if headers is None:
        headers = {}

    # Check cache first
    cached_data = read_cache(url, file_type)
    if cached_data is not None and not overwrite:
        return cached_data

    # Download fresh data
    response = requests.get(url, headers=headers)
    html_content = response.text

    if debug:
        print(f"Downloaded HTML content, length: {len(html_content)}")

    if len(html_content) < 1:
        print("error, response too small", html_content)
        raise ValueError("Response too small")

    write_cache(url, file_type, html_content)
    return html_content
"""
