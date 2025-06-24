import spotipy  # type: ignore  # noqa: PGH003
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


def current_playing() -> str | None:
    """Get the currently playing track on Spotify."""
    load_dotenv()
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    current_playback = sp.current_playback()
    if not current_playback:
        print("spotify is not currently playing anything")
        return None
    if False:
        print_dict_keys(
            current_playback["item"],
            ["name", ["artists", 0, "name"], ["album", "name"], "id"],
        )
    return current_playback["item"]["id"]


if __name__ == "__main__":
    print("Running Spotify status...")
    track_id: str = current_playing()
    if track_id:
        print("Currently playing track ID:", track_id)
    else:
        print("No track is currently playing.")
