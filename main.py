"""Main module for the Music Metadata Collector.

This module initializes the metadata collector and retrieves the current track details.
"""

from mmc.core import metadata_collector

if __name__ == "__main__":
    metadata_collector.get_current_track_details()
