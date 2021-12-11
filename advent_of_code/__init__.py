"""Advent of Code 2021."""

from typing import Callable, Optional

from typer import Typer

from .challenges import (
    day01,
    day02,
    day03,
    day04,
    day05,
    day06,
    day07,
    day08,
    day09,
    day10,
)

__version__ = "0.1"

app = Typer()

_day_code_map: dict[int, Callable] = {
    1: day01.main,
    2: day02.main,
    3: day03.main,
    4: day04.main,
    5: day05.main,
    6: day06.main,
    7: day07.main,
    8: day08.main,
    9: day09.main,
    10: day10.main,
}


@app.command()
def run(day: Optional[int] = None) -> None:
    """Run the code for all days or a specific day.

    Args:
        day (Optional[int], optional): Specific day to run. Defaults to None.

    Raises:
        BaseException: If the code for the requested day is not available.
    """
    if day is not None:
        if day in _day_code_map:
            _day_code_map[day]()
        else:
            raise BaseException(f"Code for day {day} not available.")
    else:
        for day_code in _day_code_map.values():
            day_code()
    return None


def main() -> None:
    """Use the package CLI."""
    app()


if __name__ == "__main__":
    main()
