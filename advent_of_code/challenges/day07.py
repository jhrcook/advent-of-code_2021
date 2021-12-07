"""Day 7: The Treachery of Whales."""

from functools import cache
from typing import Final

import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 7


def _get_input_data() -> list[int]:
    data = ""
    with open(get_data_path(DAY), "r") as file:
        for line in file:
            data += line.strip()
    return [int(x) for x in data.split(",")]


def _get_example_data() -> list[int]:
    return [int(x) for x in "16,1,2,0,4,2,7,1,2,14".split(",")]


def find_cheapest_position_constant_fuel(postions: list[int]) -> tuple[int, int]:
    """Find the cheapeast position if fuel is consumed as a constant rate.

    This provides the answer for Part 1.

    Args:
        postions (list[int]): Initial crab positions.

    Returns:
        tuple[int, int]: Final position and cost of moving.
    """
    pos = np.around(np.quantile(postions, 0.5)).astype(int)
    cost = sum([abs(x - pos) for x in postions])
    return pos, cost


@cache
def _calc_fuel_cost(a: int, b: int) -> int:
    return sum(list(range(abs(a - b) + 1)))


def _growing_fuel_cost(target: int, positions: list[int]) -> int:
    return sum([_calc_fuel_cost(target, x) for x in positions])


def find_cheapest_position_increasing_fuel(positions: list[int]) -> tuple[int, int]:
    """Find the cheapeast position if fuel is consumed as a growing rate.

    This provides the answer for Part 2.

    Args:
        postions (list[int]): Initial crab positions.

    Returns:
        tuple[int, int]: Final position and cost of moving.
    """
    min_pos, min_cost = len(positions), _growing_fuel_cost(0, positions)
    for target in range(min(positions), max(positions)):
        cost = _growing_fuel_cost(target, positions)
        if cost < min_cost:
            min_pos, min_cost = target, cost
    return min_pos, min_cost


def main() -> None:
    """Run code for day 7 'The Treachery of Whales'."""
    # Part 1.
    ex_crab_positions = _get_example_data()
    ex_pos, ex_cost = find_cheapest_position_constant_fuel(ex_crab_positions)
    check_example(2, ex_pos)
    check_example(37, ex_cost)
    crab_postion = _get_input_data()
    _, cost = find_cheapest_position_constant_fuel(crab_postion)
    print_single_answer(DAY, 1, cost)
    check_answer(352997, cost, DAY, 1)

    # Part 2.
    ex_crab_positions = _get_example_data()
    ex_pos, ex_cost = find_cheapest_position_increasing_fuel(ex_crab_positions)
    check_example(ex_pos, 5)
    check_example(ex_cost, 168)
    crab_postion = _get_input_data()
    _, cost = find_cheapest_position_increasing_fuel(crab_postion)
    print_single_answer(DAY, 2, cost)
    check_answer(101571302, cost, DAY, 2)

    return None


if __name__ == "__main__":
    main()
