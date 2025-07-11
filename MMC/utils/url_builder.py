# type alias for url args format
type URLArgsFormat = dict[str, dict[str, dict[str, str]]]

BASE_URLS = {
    "deezer": "https://api.deezer.com/",
    "last_fm": "http://ws.audioscrobbler.com/2.0/",
    "spotify": "https://api.spotify.com/v1/",
    "music_brainz": "https://musicbrainz.org/ws/2/",
}


URL_ARGS_FORMAT: URLArgsFormat = {
    "deezer": {
        "lookup": {
            "album": "album/{}",
            "artist": "artist/{}",
            "track": "track/{}",
        },
        "search": {
            "album": 'search/album?q=album:"{}" "artist:"{}"',
            "artist": 'search/artist?q=artist:"{}"',
            "track": 'search/track?q=track:"{}" "artist:"{}"',
            "track-album": 'search/track?q=track:"{}" "album:"{}"',
        },
    },
    "spotify": {
        "lookup": {
            "album": "albums/{}",
            "artist": "artists/{}",
            "track": "tracks/{}",
        },
        "search": {
            "track": "search?type=track&q=track:{}&artist:{}&limit=5",
            "artist": "search?type=artist&q=artist:{}&limit=5",
            "album": "search?type=album&q=album:{}&artist:{}&limit=5",
        },
    },
    "music_brainz": {
        "lookup": {
            "artist": "artist/{}?fmt=json",
            "track": "recording/{}?inc=artists+releases&fmt=json",
            "album": "release/{}?inc=artists+recordings&fmt=json",
        },
        "search": {},
    },
}


class ApiUrlBuilder:
    """Base class for building API URLs."""

    def __init__(
        self,
        service_name: str,
        request_type: str,
        request_resource: str,
        url_args: list[str] | str,
    ) -> None:
        """Initialize the ApiUrlBuilder.

        Args:
            service_name (str): The name of the API service ('deezer', 'spotify').
            request_type (str): The type of request ('lookup', 'search').
            request_resource (str): The requested resource ('album', 'artist', 'track').
            url_args (list[str] | str): args for request (track id, track string etc.).

        """
        self.service_name: str = service_name
        self.request_type: str = request_type
        self.request_resource: str = request_resource
        self.url_args: list[str] | str = url_args
        self.base_url: str = ""
        self.full_url: str = ""
        self.__post_init__()

    def __post_init__(self) -> None:
        """Post initialization.

        Raises:
            ValueError: If the service name or request type is unsupported.

        """
        # error checking
        if self.service_name not in BASE_URLS:
            msg = f"Unsupported service name: {self.service_name}"
            raise ValueError(msg)
        if self.request_type not in URL_ARGS_FORMAT[self.service_name]:
            msg = (
                f"Unsupported request type: {self.request_type} "
                f"for service {self.service_name}"
            )
            raise ValueError(msg)
        # populate fields
        self.base_url = BASE_URLS[self.service_name]
        if isinstance(self.url_args, str):
            self.url_args = [self.url_args]
        self.full_url = self.build_full_url()

    def build_full_url(self) -> str:
        """Build the full API URL with method and parameters."""
        url_args = URL_ARGS_FORMAT[self.service_name][self.request_type][
            self.request_resource
        ]
        return self.base_url + url_args.format(*self.url_args)


if __name__ == "__main__":
    # Example usage
    url_builder = ApiUrlBuilder(
        service_name="deezer",
        request_type="lookup",
        request_resource="album",
        url_args="123456",
    )
    print(url_builder.full_url)  # Should print the full URL for the album lookup
