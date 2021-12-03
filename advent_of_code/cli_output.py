"""Command line output."""

from typing import Union

import rich

from advent_of_code.aoc_types import challenge_part


def print_single_answer(
    day: int, part: challenge_part, value: Union[bool, float, str]
) -> None:
    """Print the result of a single (simple) answer.

    Args:
        day (int): Day of the challenge.
        part (challenge_part): Part of the challenge (1 or 2).
        value (Union[bool, float, str]): Simple value to print.
    """
    rich.print(f"[bold blue]Day {day} part {part} answer: {value}[/bold blue]")
