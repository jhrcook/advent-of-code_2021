"""Day 11: Dumbo Octopus."""

from dataclasses import dataclass
from itertools import product
from typing import Final, Optional

import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 11
NAME: Final[str] = "Dumbo Octopus"

_small_example_energy_levels = """
11111
19991
19191
19991
11111
"""

_example_energy_levels = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""


def _parse_energy_level_grid(grid: str) -> np.ndarray:
    rows = []
    for line in grid.strip().splitlines():
        rows.append([int(x) for x in line.strip()])
    return np.array(rows)


def _get_small_example_energy_levels() -> np.ndarray:
    return _parse_energy_level_grid(_small_example_energy_levels)


def _get_example_energy_levels() -> np.ndarray:
    return _parse_energy_level_grid(_example_energy_levels)


def _get_energy_level_data() -> np.ndarray:
    data = ""
    with open(get_data_path(DAY), "r") as file:
        for line in file:
            data += line.strip() + "\n"
    return _parse_energy_level_grid(data)


def _add_inf_border(grid: np.ndarray) -> np.ndarray:
    """Add negative infinity padding to a grid."""
    return np.pad(grid.astype(float), (1, 1), mode="constant", constant_values=-np.inf)


def _padded_grid_position_iter(grid: np.ndarray) -> product:
    """Make an iterator over the octopus grid ignoring the padding."""
    dims = grid.shape
    return product(range(1, dims[0]), range(1, dims[1]))


def _strip_padding(grid: np.ndarray) -> np.ndarray:
    """Remove the padding of a grid."""
    dims = grid.shape
    return grid[1 : (dims[0] - 1), 1 : (dims[1] - 1)]


def _get_all_neighbor_positions(i: int, j: int) -> list[tuple[int, int]]:
    """Get the neighboring positions in a grid."""
    neighbors = []
    for a, b in product(range(-1, 2), range(-1, 2)):
        if a == 0 and b == 0:
            continue
        neighbors.append((i + a, j + b))
    return neighbors


def add_one_to_neighbors(grid: np.ndarray, i: int, j: int) -> np.ndarray:
    """Add one to all neighbors (including diagonals) in a grid.

    Args:
        grid (np.ndarray): Grid of octopuses.
        i (int): Row of octopus.
        j (int): Column of octopus.

    Returns:
        np.ndarray: Modified grid.
    """
    for a, b in _get_all_neighbor_positions(i, j):
        grid[a, b] += 1
    return grid


def octopus_step(grid: np.ndarray) -> tuple[np.ndarray, int]:
    """Carry out a single step of the algorithm.

    The algorithm:
      1. increment all by 1
      2. make a copy of the grid
      3. add the number of flashes to a running total
      4. for each position on the grid, if that octopus has flashed, add 1 to all of the
         neighbors and add that position to a collection of positions that have flashed
         (they can only flash once)
      5. set all octopus that are flashing or have flashed to 0
      6. if the total of the grid is different than at the beginning, return to step 2
         and repeat
      7. else return the new grid and total number of flashes

    Args:
        grid (np.ndarray): Grid of octopuses (padded with a layer of neg. infinity).

    Returns:
        tuple[np.ndarray, int]: Resulting grid and number of flashes that occurred.
    """
    grid += 1
    grid_sum = np.sum(_strip_padding(grid))
    _previous_sum = 0
    total_flashes = 0
    has_flashed: set[tuple[int, int]] = set()
    while grid_sum != _previous_sum:
        new_grid = grid.copy()
        _previous_sum = np.sum(_strip_padding(grid))
        total_flashes += np.sum(new_grid > 9.5)
        for i, j in _padded_grid_position_iter(grid):
            val = grid[i, j]
            if val > 9.5:
                new_grid = add_one_to_neighbors(new_grid, i=i, j=j)
                has_flashed.add((i, j))

        new_grid[grid > 9.5] = 0

        for a, b in has_flashed:
            new_grid[a, b] = 0

        grid = new_grid.copy()
        grid_sum = np.sum(_strip_padding(grid))

    return grid, total_flashes


@dataclass
class OctopusGridResult:
    """Result type for modeling the octopus grid."""

    grid: np.ndarray
    flashes: int
    synchronized_steps: list[int]


def octopus_grid_model(grid: np.ndarray, steps: Optional[int]) -> OctopusGridResult:
    """Model a number of steps for a grid of octopuses.

    Args:
        grid (np.ndarray): Grid of octopuses.
        steps (Optional[int]): Number of steps to model. Set to None to stop only when
        the grid is synchronized.

    Returns:
        OctopusGridResult: Result after the steps.
    """
    padded_grid = _add_inf_border(grid.copy())
    total_flashes = 0
    synced_steps: list[int] = []

    _stop_when_sync = False
    if steps is None:
        _stop_when_sync = True
        steps = 100000000

    for step in range(1, steps + 1):
        padded_grid, n_flashes = octopus_step(padded_grid)
        total_flashes += n_flashes
        if np.all(padded_grid < 1):
            synced_steps.append(step)
            if _stop_when_sync:
                break

    return OctopusGridResult(
        grid=_strip_padding(padded_grid),
        flashes=total_flashes,
        synchronized_steps=synced_steps,
    )


def main() -> None:
    """Run code for 'Day 11: Dumbo Octopus'."""
    # Part 1.
    # Examples
    _ex_grid = _get_example_energy_levels()
    _ex_res = octopus_grid_model(_ex_grid, steps=100)
    check_example(1656, _ex_res.flashes)
    # Real
    octo_grid = _get_energy_level_data()
    octo_grid_res = octopus_grid_model(octo_grid, steps=100)
    print_single_answer(DAY, 1, octo_grid_res.flashes)
    check_answer(1644, octo_grid_res.flashes, DAY, 1)

    # Part 2.
    # Example
    _ex_grid = _get_example_energy_levels()
    _ex_res = octopus_grid_model(_ex_grid, steps=200)
    check_example(195, np.min(_ex_res.synchronized_steps))
    # Real
    octo_grid = _get_energy_level_data()
    octo_grid_res = octopus_grid_model(octo_grid, steps=None)
    print_single_answer(DAY, 2, octo_grid_res.synchronized_steps[0])
    return None


if __name__ == "__main__":
    main()
