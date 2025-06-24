"""Credential management Utilities."""

from __future__ import annotations

import json

from .exceptions import InvalidServiceException


def load_credentials(service: str) -> dict[str, str]:
    """Load credentials for a given service from a JSON file.

    Args:
        service (str): The name of the service to load credentials for.

    Returns:
        dict: The credentials for the specified service.

    Raises:
        InvalidServiceException: If the specified service is not valid.
    """
    valid_services = ['spotify', 'last_fm', 'genius']
    if service not in valid_services:
        msg = (
            f"Invalid service: {service}. "
            f"Please choose from the following valid services: {valid_services}."
        )
        raise InvalidServiceException(msg)
    # load credentials via json
    with open('credentials.json', encoding='utf-8') as r:
        return json.load(r)[service]
