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


def read_data(day: int, name: str = "input.txt") -> str:
    """Read in the day's puzzle input as a string.

    Args:
        day (int): Day of the challenge.
        name (str, optional): Name of the file. Defaults to "input.txt".

    Returns:
        str: The puzzle input as a string.
    """
    with open(get_data_path(day=day, name=name), "r") as file:
        data = "".join(line for line in file)
    return data


def output_dir() -> Path:
    """Path to the output directory.

    Returns:
        Path: Output directory for saving files.
    """
    return Path(__file__).parent.parent / "output"
