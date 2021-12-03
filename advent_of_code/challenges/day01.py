"""Day 1: Sonar Sweep."""

from pathlib import Path
from typing import Final

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 1

_test_sonar_sweep_report = """
199
200
208
210
200
207
240
269
260
263
"""


def _read_sonar_sweep_data(data_file: Path) -> list[int]:
    with open(data_file, "r") as file:
        data = [int(line.strip()) for line in file if len(line) > 0]
    return data


def _parse_sonar_sweep_data(data: str) -> list[int]:
    return [int(x) for x in data.strip().splitlines()]


def count_increases(sonar_sweep_report: list[int]) -> int:
    """Count the number of increases in a sonar sweep report.

    Args:
        sonar_sweep_report (list[int]): Sonar sweep report values.

    Returns:
        int: Number of increases in depth.
    """
    n_increases = 0
    for i in range(len(sonar_sweep_report) - 1):
        n_increases += int(sonar_sweep_report[i] < sonar_sweep_report[i + 1])
    return n_increases


def make_sliding_window(sonar_sweep: list[int], width: int = 3) -> list[int]:
    """Make a sliding window of sonar sweep depths.

    Args:
        sonar_sweep (list[int]): Sonar sweep report values.
        width (int, optional): Sliding window. Defaults to 3.

    Returns:
        list[int]: Window-summed sonar sweep depths.
    """
    new_sonar_sweep: list[int] = []
    for i in range(len(sonar_sweep) - (width - 1)):
        window = sonar_sweep[i : (i + width)]
        new_sonar_sweep.append(sum(window))
    return new_sonar_sweep


if __name__ == "__main__":
    # Data.
    test_sonar_sweep = _parse_sonar_sweep_data(_test_sonar_sweep_report)
    sonar_sweep_report = _read_sonar_sweep_data(get_data_path(DAY))

    # Part 1.
    test_res = count_increases(test_sonar_sweep)
    check_example(7, test_res)
    answer1 = count_increases(sonar_sweep_report)
    check_answer(1226, answer1, day=DAY, part=1)
    print_single_answer(DAY, 1, answer1)

    # Part 2.
    test_windowed_sonar_sweep = make_sliding_window(test_sonar_sweep)
    test_res = count_increases(test_windowed_sonar_sweep)
    check_example(5, test_res)
    windowed_sonar_sweep = make_sliding_window(sonar_sweep_report)
    answer2 = count_increases(windowed_sonar_sweep)
    check_answer(1252, answer1, day=DAY, part=2)
    print_single_answer(DAY, 2, answer2)
