"""Checking values against knowns."""

from typing import TypeVar

from advent_of_code.aoc_types import challenge_part

T = TypeVar("T")


def check_example(expected: T, actual: T) -> bool:
    """Check an example provided in the challenge description.

    Args:
        expected (T): Expected value.
        actual (T): Actual value (i.e. calculated by my code).

    Returns:
        bool: Whether the value matches the expected.
    """
    assert expected == actual, f"failed example: expected {expected}, got {actual}"
    return True


def check_answer(expected: T, actual: T, day: int, part: challenge_part) -> bool:
    """Check an answer agains the known solution.

    Args:
        expected (T): Expected answer.
        actual (T): Calculated answer (i.e. calculated by my code).
        day (int): Day of the challenge.
        part (int): Part of the challenge (1 or 2).

    Returns:
        bool: Whether the value matches the expected.
    """
    assert expected == actual, f"Incorrect puzzle answer for day {day} part {part}."
    return True
