"""Utility functions for Deezer services."""

from typing import Any


def find_first_matching_dict(
    search_list: list[dict[str, Any]],
    target_key: str,
    taget_value: str,
) -> dict[str, Any]:
    """Search a list of dicts and get the first match.

    Raises:
        KeyError: If no match is found.

    """
    for result in search_list:
        if result[target_key] == taget_value:
            return result
    unique_values = {result[target_key] for result in search_list}
    msg = f"No keypair {target_key}={taget_value}, only found {unique_values} "
    raise KeyError(msg)
