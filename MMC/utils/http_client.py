"""HTTP client utilities for downloading data"""

from __future__ import annotations

from typing import Any

import requests

from .cache import check_cache, write_cache


def download_json(
    url: str,
    headers: dict[str, str] | None = None,
    overwrite: bool = False,
    debug: bool = False,
) -> dict[str, Any]:
    """Download data from a URL and cache it locally."""
    file_type = 'json'
    if headers is None:
        headers = {}
    processed_url = url
    data = check_cache(url, file_type)
    if data is not None and not overwrite:
        if debug:
            print(f'Using cached data from {processed_url}')
    else:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'data' in data:
            data = data['data']
        if len(data) < 1:
            msg = f'Error, response too small: {data}'
            raise ValueError(msg)
        write_cache(url, file_type, data)
    if debug:
        print(data['tracks'].keys())
    return data


def download_html(
    url: str,
    headers: dict[str, str] | None = None,
    overwrite: bool = False,
    debug: bool = False,
) -> str:
    """Download HTML data from a URL and cache it locally."""
    file_type = 'html'
    if headers is None:
        headers = {}

    # Check cache first
    cached_data = check_cache(url, file_type)
    if cached_data is not None and not overwrite:
        return cached_data

    # Download fresh data
    response = requests.get(url, headers=headers)
    html_content = response.text

    if debug:
        print(f'Downloaded HTML content, length: {len(html_content)}')

    if len(html_content) < 1:
        print('error, response too small', html_content)
        raise ValueError('Response too small')

    write_cache(url, file_type, html_content)
    return html_content
