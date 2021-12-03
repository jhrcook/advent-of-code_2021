"""Dealing with data."""

from pathlib import Path


def get_data_path(day: int, name: str = "input.txt") -> Path:
    """Get the path to the data for a challenge day.

    Args:
        day (int): Day of the challenge.
        name (str, optional): Name of the file. Defaults to "input.txt".

    Returns:
        Path: Path to the data file.
    """
    return Path("data", f"day{day:02d}", name)
