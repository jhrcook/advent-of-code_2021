"""Command line output."""

from typing import Union

from colorama import Fore, Style

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
    msg = f"Day {day} part {part} answer: {value}"
    print(Fore.BLUE + Style.BRIGHT + msg + Style.RESET_ALL)
