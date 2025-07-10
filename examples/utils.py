"""Utility functions for the examples."""
import os

from IPython.display import Markdown


def fix_path() -> None:
    """Change CWD to the parent directory of the current file."""
    os.chdir("..")


def build_list_table(
    data: list[list[str]],
    headers: list[str],
) -> Markdown:
    """Build a markdown table from two sets of lists: data and headers."""
    md = "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join(["-" * len(h) for h in headers]) + " |\n"
    for row in data:
        md += "| " + " | ".join(row) + " |\n"
    return Markdown(md)


def build_dict_table(data: list[dict[str, str | int]]) -> Markdown:
    """Build a markdown table from a dictionary of lists."""
    headers = list(data[0].keys())
    content = [[str(value) for value in item.values()] for item in data]
    md = "| " + " | ".join(headers) + " |\n"
    md += "| " + " | ".join(["-" * len(h) for h in headers]) + " |\n"
    for row in content:
        md += "| " + " | ".join(row) + " |\n"
    return Markdown(md)


if __name__ == "__main__":
    """build dict examples."""
    test_data: list[dict[str, str | int]] = [
        {
            "album_id": 146453642,
            "album_name": "Safe",
            "artist_id": 1047915,
            "artist_name": "Monkey Safari",
            "track_id": 951764442,
            "track_name": "Safe",
        },
        {
            "album_id": 239106862,
            "album_name": "These Things Will Come To Be",
            "artist_id": 11527131,
            "artist_name": "DJ Seinfeld",
            "track_id": 1411767462,
            "track_name": "These Things Will Come To Be",
        },
    ]

    print(build_dict_table(test_data).data) # type: ignore
