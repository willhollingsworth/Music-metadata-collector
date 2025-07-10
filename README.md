# Music Metadata Collector

A tool for collecting music metadata from various online sources.

A work in progress but currently supports
- Deezer
- Spotify
- Music Brainz
- Last FM.

## Examples
Examples are available in the `examples` folder as Jupyter notebooks

## Testing
Fixtures are dynamically generated using a JSON file at `scripts/fixture_ids.json` and the python file `scripts/generate_fixtures.py`

The created fixtures files are then used to dynamically create tests via `tests\test_lookups.py` 