"""Day 5: Hydrothermal Venture."""

from enum import Enum
from typing import Final

import numpy as np
from pydantic import BaseModel

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path
from advent_of_code.utils import assert_never

DAY: Final[int] = 5

_ex_list_of_vents = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


class Orientation(Enum):
    """Possible orientations of a line."""

    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"
    DIAGONAL = "DIAGONAL"
    OTHER = "OTHER"


class Point(BaseModel):
    """Point in space (helper for organizing (x,y) and (row, col) for numpy)."""

    x: int
    y: int

    @property
    def r(self) -> int:
        """Row."""
        return self.y

    @property
    def c(self) -> int:
        """Column."""
        return self.x


def is_45_diag(a: Point, b: Point) -> bool:
    """Determine if two points lie along a 45 deg. line.

    Args:
        a (Point): Point a.
        b (Point): Point b.

    Returns:
        bool: Whether the points lie along a 45 deg. line.
    """
    x_diff = np.abs(a.x - b.x)
    y_diff = np.abs(a.y - b.y)
    return x_diff == y_diff


class ThermalVent(BaseModel):
    """Line of thermal vents."""

    p1: Point
    p2: Point

    def __str__(self) -> str:
        """Human-readable form of the thermal vents."""
        a, b = self.p1, self.p2
        o = self.orientation
        return f"vent: ({a.x}, {a.y}) → ({b.x}, {b.y})  {o}"

    def __repr__(self) -> str:
        """Human-readable form of the thermal vents."""
        return str(self)

    @property
    def orientation(self) -> Orientation:
        """Orientation of the line of thermal vents."""
        if self.p1.x == self.p2.x:
            return Orientation.VERTICAL
        elif self.p1.y == self.p2.y:
            return Orientation.HORIZONTAL
        elif is_45_diag(self.p1, self.p2):
            return Orientation.DIAGONAL
        else:
            return Orientation.OTHER


def _max_rc(vents: list[ThermalVent]) -> tuple[int, int]:
    r = max([max(v.p1.r, v.p2.r) for v in vents])
    c = max([max(v.p1.c, v.p2.c) for v in vents])
    return r + 1, c + 1


def _filter_only_hv(vents: list[ThermalVent]) -> list[ThermalVent]:
    return [
        v
        for v in vents
        if v.orientation in {Orientation.HORIZONTAL, Orientation.VERTICAL}
    ]


def draw_horizontal_vent_line(vent_grid: np.ndarray, r: int, c1: int, c2: int) -> None:
    """Draw of horizontal line of vents in a vent grid.

    Note that the vent grid is passed as a reference to a numpy array and it is modified
    in place.

    Args:
        vent_grid (np.ndarray): Existing vent grid.
        r (int): Row of the grid which the vents line upon.
        c1 (int): Start column.
        c2 (int): End column.
    """
    c1, c2 = min(c1, c2), max(c1, c2)
    vent_grid[r, c1 : (c2 + 1)] += 1
    return None


def _sort_diag_points_left_to_right(a: Point, b: Point) -> tuple[Point, Point]:
    if a.x < b.x:
        return a, b
    else:
        return b, a


def draw_diagonal_vent_line(vent_grid: np.ndarray, a: Point, b: Point) -> None:
    """Draw a diagonal line of vents.

    Note that the vent grid is passed as a reference to a numpy array and it is modified
    in place.

    Args:
        vent_grid (np.ndarray): Existing grid of vents.
        a (Point): Starting point of line of vents.
        b (Point): End point of ling of vents.
    """
    # Sort diagonal points going from left to right.
    a, b = _sort_diag_points_left_to_right(a, b)
    if a.y < b.y:
        # slanting down
        for r, c in zip(range(a.r, b.r + 1), range(a.c, b.c + 1)):
            vent_grid[r, c] += 1
    else:
        # slanting up
        for r, c in zip(range(a.r, b.r - 1, -1), range(a.c, b.c + 1)):
            vent_grid[r, c] += 1
    return None


def make_grid_of_vents(vents: list[ThermalVent], only_hv: bool = True) -> np.ndarray:
    """Make a grid of vents from a list of thermal vent locations.

    Note that the functions that draw lines work on the same vent grid numpy array (it
    is passed as a reference). This results in a significant computational speed-up, but
    leaves the door open for odd behavior if future modifications are made ot the code.

    Args:
        vents (list[ThermalVent]): List of thermal vent lines.
        only_hv (bool, optional): Only include horizontal and vertical vents? Defaults
        to True.

    Returns:
        np.ndarray: Grid showing locations and number of vents.
    """
    if only_hv:
        vents = _filter_only_hv(vents)
    grid = np.zeros(_max_rc(vents), dtype=int)
    for v in vents:
        p1, p2 = v.p1, v.p2
        if v.orientation is Orientation.HORIZONTAL:
            draw_horizontal_vent_line(grid, p1.r, p1.c, p2.c)
        elif v.orientation is Orientation.VERTICAL:
            grid = grid.T
            draw_horizontal_vent_line(grid, p1.c, p1.r, p2.r)
            grid = grid.T
        elif v.orientation is Orientation.DIAGONAL:
            draw_diagonal_vent_line(grid, p1, p2)
        elif v.orientation is Orientation.OTHER:
            pass
        else:
            assert_never(v.orientation)
    return grid


def n_dangerous_points(grid: np.ndarray, val: int = 2) -> int:
    """Count the number of dangerous cells in a grid of vents.

    Args:
        grid (np.ndarray): Grid of vents.
        val (int, optional): Level at which the vents are dangerous. Defaults to 2.

    Returns:
        int: Number of dangerous cells.
    """
    return np.sum(grid >= val)


def _parse_vent_line_digram(vent_str: str) -> ThermalVent:
    points = [x.split(",") for x in vent_str.strip().split(" -> ")]
    assert len(points) == 2
    p1 = Point(x=points[0][0], y=points[0][1])
    p2 = Point(x=points[1][0], y=points[1][1])
    return ThermalVent(p1=p1, p2=p2)


def _parse_list_of_vents(vents_str: str) -> list[ThermalVent]:
    return [_parse_vent_line_digram(x) for x in vents_str.strip().splitlines()]


def _get_vents() -> list[ThermalVent]:
    with open(get_data_path(DAY), "r") as file:
        vent_str = "\n".join([line.strip() for line in file]).strip()
    return _parse_list_of_vents(vent_str)


def main() -> None:
    """Run the code for day 5's challenge."""
    # Part 1.
    ex_vents = _parse_list_of_vents(_ex_list_of_vents)
    vents = _get_vents()
    ex_grid = make_grid_of_vents(ex_vents)
    check_example(5, n_dangerous_points(ex_grid))
    vent_grid = make_grid_of_vents(vents)
    n_danger = n_dangerous_points(vent_grid)
    print_single_answer(DAY, 1, n_danger)
    check_answer(5092, n_danger, DAY, 1)

    # Part 2.
    ex_vents = _parse_list_of_vents(_ex_list_of_vents)
    vents = _get_vents()
    ex_grid = make_grid_of_vents(ex_vents, only_hv=False)
    check_example(12, n_dangerous_points(ex_grid))
    vent_grid = make_grid_of_vents(vents, only_hv=False)
    n_danger = n_dangerous_points(vent_grid)
    print_single_answer(DAY, 2, n_danger)
    check_answer(20484, n_danger, DAY, 2)


if __name__ == "__main__":
    main()
