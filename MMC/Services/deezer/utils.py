"""Utility functions for Deezer services."""

from typing import Any


def get_first_track(track_results: dict[str, Any] | list[Any]) -> dict[str, Any]:
    """Get the first track from a Deezer track search result.

    Raises:
        TypeError: If track_results is not a dict or list.

    """
    if isinstance(track_results, list):
        for track in track_results:
            if track["type"] == "track":
                return track
    if not isinstance(track_results, dict):
        msg = f"Expected a dict or list, got {type(track_results)}"
        raise TypeError(msg)
    return track_results
