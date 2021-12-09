"""Day 9: Smoke Basin."""

from dataclasses import dataclass
from itertools import product
from typing import Final

import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 9


def _example_heightmap() -> np.ndarray:
    _data = """
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    """
    rows: list[list[int]] = []
    for line in _data.strip().splitlines():
        rows.append([int(x) for x in line.strip()])
    return np.array(rows)


def _get_heightmap() -> np.ndarray:
    rows: list[list[int]] = []
    with open(get_data_path(DAY), "r") as file:
        for line in file:
            rows.append([int(x) for x in line.strip()])
    return np.array(rows)


@dataclass
class LowPoint:
    """Low point on the sea floor."""

    pos: tuple[int, int]
    value: int

    @property
    def risk_level(self) -> int:
        """Risk level of the low point."""
        return self.value + 1

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"({self.pos[0]}, {self.pos[1]}): {self.value}"

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)


# ---- Part 1 ----


def _add_wall_around_heightmap(heightmap: np.ndarray) -> np.ndarray:
    return np.pad(heightmap, (1, 1), mode="constant", constant_values=10)


def _get_surrounding_positions(i: int, j: int) -> list[tuple[int, int]]:
    return [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]


def _get_surrounding_values(heightmap: np.ndarray, i: int, j: int) -> np.ndarray:
    return np.array([heightmap[a, b] for a, b in _get_surrounding_positions(i, j)])


def heightmap_position_iter(heightmap: np.ndarray) -> product:
    """Make an iterator over the heightmap ignoring the padding.

    Args:
        heightmap (np.ndarray): Heightmap of the sea floor.

    Returns:
        product: Iterator for the postions of the heightmap.
    """
    dims = heightmap.shape
    return product(range(1, dims[0] - 1), range(1, dims[1] - 1))


def find_lowpoints(heightmap: np.ndarray) -> list[LowPoint]:
    """Find the low points in a heightmap.

    Args:
        heightmap (np.ndarray): Heightmap of the sea floor.

    Returns:
        list[LowPoint]: All of the low points.
    """
    heightmap = _add_wall_around_heightmap(heightmap)
    low_pts: list[LowPoint] = []
    for i, j in heightmap_position_iter(heightmap):
        neighbor_values = _get_surrounding_values(heightmap, i, j)
        value = heightmap[i, j]
        if np.all(neighbor_values > value):
            low_pts.append(LowPoint(pos=(i, j), value=value))
    return low_pts


def total_risk_level(low_points: list[LowPoint]) -> int:
    """Calculate the total risk level from all of the low points.

    Args:
        low_points (list[LowPoint]): List of low points.

    Returns:
        int: Total risk level.
    """
    return sum([pt.risk_level for pt in low_points])


# ---- Part 2 ----


def _init_basin(heightmap: np.ndarray, low_pt: LowPoint) -> np.ndarray:
    basin = np.zeros_like(heightmap)
    basin[low_pt.pos[0], low_pt.pos[1]] = 1
    return basin.astype(bool)


def can_be_part_of_the_basin(basin: np.ndarray, i: int, j: int) -> bool:
    """Whether a position could be part of a basin.

    Args:
        basin (np.ndarray): Existing basin.
        i (int): Row position.
        j (int): Column position.

    Returns:
        bool: Can the position (i,j) be part of the basin?
    """
    for a, b in _get_surrounding_positions(i=i, j=j):
        if basin[a, b]:
            return True
    return False


def find_basin(heightmap: np.ndarray, low_pt: LowPoint) -> np.ndarray:
    """Find the basin in a heightmap for a given low point.

    Args:
        heightmap (np.ndarray): Heightmap of the sea floor.
        low_pt (LowPoint): Low point in the map.

    Returns:
        np.ndarray: Numpy array representing the locations of the basin.
    """
    heightmap = _add_wall_around_heightmap(heightmap)
    basin = _init_basin(heightmap, low_pt)
    _previous_size: int = 0
    while np.sum(basin) != _previous_size:
        _previous_size = np.sum(basin)
        for i, j in heightmap_position_iter(heightmap):
            if not basin[i, j] and heightmap[i, j] < 9:
                basin[i, j] = can_be_part_of_the_basin(basin, i, j)
    return basin


def find_all_basins(heightmap: np.ndarray, low_pts: list[LowPoint]) -> list[np.ndarray]:
    """Find all of the basins in a hieghtmap.

    Args:
        heightmap (np.ndarray): Heightmap of the sea floor.
        low_pts (list[LowPoint]): All of the low points in the heightmap.

    Returns:
        list[np.ndarray]: List of the basins.
    """
    return [find_basin(heightmap=heightmap, low_pt=pt) for pt in low_pts]


def product_of_size_of_three_largest_basins(basins: list[np.ndarray]) -> int:
    """Product of the sizes of the 3-largest basins.

    This is the numeric answer to Part 2.

    Args:
        basins (list[np.ndarray]): All of the basins.

    Returns:
        int: The product of the sizes of the 3-largest basins.
    """
    basin_sizes = [np.sum(b) for b in basins]
    basin_sizes.sort()
    return np.prod(basin_sizes[-3:])


def main() -> None:
    """Run code for 'Day 9: Smoke Basin'."""
    # Part 1.
    # Example.
    ex_map = _example_heightmap()
    ex_low_pts = find_lowpoints(ex_map)
    check_example(4, len(ex_low_pts))
    check_example(15, total_risk_level(ex_low_pts))
    # Real.
    heightmap = _get_heightmap()
    risk_level = total_risk_level(find_lowpoints(heightmap))
    print_single_answer(DAY, 1, risk_level)
    check_answer(633, risk_level, DAY, 1)

    # Part 2.
    # Example.
    ex_map = _example_heightmap()
    ex_low_pts = find_lowpoints(ex_map)
    ex_basins = find_all_basins(heightmap=ex_map, low_pts=ex_low_pts)
    [check_example(x, np.sum(y)) for x, y in zip([3, 9, 14, 9], ex_basins)]
    check_example(1134, product_of_size_of_three_largest_basins(ex_basins))
    # Real.
    heightmap = _get_heightmap()
    low_pts = find_lowpoints(heightmap)
    basins = find_all_basins(heightmap=heightmap, low_pts=low_pts)
    res = product_of_size_of_three_largest_basins(basins)
    print_single_answer(DAY, 2, res)
    check_example(1050192, res)
    return None


if __name__ == "__main__":
    main()
