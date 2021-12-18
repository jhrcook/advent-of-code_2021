"""Day 17: Trick Shot."""

from dataclasses import dataclass
from math import floor

import matplotlib.pyplot as plt
import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=17, title="Trick Shot")

_example_target_area = "target area: x=20..30, y=-10..-5"


Point = tuple[int, int]
Trajectory = list[Point]


@dataclass
class Area:
    """An object representing a rectangular area."""

    xmin: int
    xmax: int
    ymin: int
    ymax: int

    def is_inside(self, pt: tuple[float, float]) -> bool:
        """Determine if some point is inside of the area.

        Args:
            pt (tuple[float, float]): Point to check.

        Returns:
            bool: Whether a point is in the area.
        """
        x, y = pt
        return (self.xmin <= x <= self.xmax) and (self.ymin <= y <= self.ymax)

    @property
    def center(self) -> tuple[float, float]:
        """Center of the area."""
        return ((self.xmin + self.xmax) / 2.0, (self.ymin + self.ymax) / 2.0)


def parse_target_area_input(target_area_str: str) -> Area:
    """Parse target area string data."""
    x_range, y_range = target_area_str.replace("target area: ", "").split(
        ", ", maxsplit=1
    )
    xs = [abs(int(x)) for x in x_range.replace("x=", "").split("..", maxsplit=1)]
    assert len(xs) == 2
    ys = [int(x) for x in y_range.replace("y=", "").split("..", maxsplit=1)]
    assert len(ys) == 2
    return Area(xmin=min(xs), xmax=max(xs), ymin=min(ys), ymax=max(ys))


def get_puzzle_target_area() -> Area:
    """Get puzzle input."""
    return parse_target_area_input(read_data(PI.day).strip())


@dataclass
class SimulationResult:
    """Results of a simulation."""

    v_initial: tuple[int, int]
    hit: bool
    passed_through: bool
    trajectory: Trajectory

    @property
    def highest_point(self) -> Point:
        """Highest point reached in the simulation."""
        ys = [p[1] for p in self.trajectory]
        idx = ys.index(max(ys))
        return self.trajectory[idx]


def _get_nearest_point(a: Point, b: Point, area: Area) -> tuple[float, float]:
    x: float
    y: float
    if b[0] == a[0]:
        # Points a and b are vertical.
        x, y = a[0], area.center[1]
    elif b[1] == a[1]:
        # Points a and b are horizontal.
        x, y = area.center[0], a[1]
    else:
        # Step 1
        m = (b[1] - a[1]) / (b[0] - a[0])
        d = a[1] - m * a[0]
        # Step 2
        _m = 1.0 / m
        if _m == m:
            # Parallel and therefore the line goes through the middle.
            return area.center
        # Step 3
        c = area.center
        f = c[1] - _m * c[0]
        # Step 4
        x = (f - d) / (m - _m)
        y = m * x + d
    return x, y


def did_pass_through(a: Point, b: Point, area: Area) -> bool:
    """Check if a line between two points passes through an area.

    This algorithm is based off of the fact that this quality can be confirmed by
    determining if the point on the line between `a` and `b` that is closest to the
    center of the area is in the area.

    Algorithm:
      1. Find the line, `ab_line`,  between `a` and `b`.
      2. Use the slope of `ab_line`, `m`, to calculate the slope of the perpendicular,
         `_m`.
      3. Use that slope and the center of the area `c` to find the line perpendicular to
         `ab_line` that passes through `c`.
      4. Find the point of intersection between `ab_line` and `c_line`.
      5. Is this point in the area?

    `ab_line`: y = m * x + d
    `c_line`: y = _m * x + f

    Args:
        a (Point): First point.
        b (Point): Second point.
        area (Area): Area of intersection.

    Returns:
        bool: Does the line pass through the area?
    """
    # Steps 1-4
    nearest_point = _get_nearest_point(a, b, area)
    # Step 5
    return area.is_inside(nearest_point)


def run_simulation(
    v_initial: tuple[int, int],
    target_area: Area,
) -> SimulationResult:
    """Run a simulation.

    Args:
        v_initial (tuple[int, int]): Initial velocity.
        target_area (Area): Target area.

    Returns:
        SimulationResult: Simulation results.
    """
    pos = np.array([0, 0], dtype=int)
    v = np.array(v_initial, dtype=int)
    a = np.array([-1, -1], dtype=int)
    hit = False
    trajectory: Trajectory = [(0, 0)]
    while True:
        pos += v
        v += a
        v[0] = max([v[0], 0])

        if trajectory is not None:
            trajectory.append((pos[0], pos[1]))

        if pos[0] > target_area.xmax or pos[1] < target_area.ymin:
            break

        if target_area.is_inside((pos[0], pos[1])):
            hit = True
            break

    passed_through = hit
    if not hit:
        passed_through = did_pass_through(trajectory[-1], trajectory[-2], target_area)
    return SimulationResult(
        v_initial=v_initial,
        hit=hit,
        passed_through=passed_through,
        trajectory=trajectory,
    )


def plot_simulation(sim: SimulationResult, target: Area) -> None:
    """Plot the results of a simulation."""
    x = [p[0] for p in sim.trajectory]
    y = [p[1] for p in sim.trajectory]
    plt.plot(x, y, "o--")

    box_x = [target.xmin, target.xmax, target.xmax, target.xmin, target.xmin]
    box_y = [target.ymax, target.ymax, target.ymin, target.ymin, target.ymax]
    plt.plot(box_x, box_y, c="r")

    if not sim.hit:
        nearest_point = _get_nearest_point(
            sim.trajectory[-1], sim.trajectory[-2], target
        )
        plt.plot(
            [target.center[0], nearest_point[0]],
            [target.center[1], nearest_point[1]],
            "g--",
            marker="o",
        )

    high_pt = sim.highest_point
    plt.text(high_pt[0] * 1.02, high_pt[1] * 1.02, f"{high_pt}")

    title = f"initial velocity: {sim.v_initial}, "
    title += f"hit: {sim.hit}, passed through: {sim.passed_through}"
    plt.title(title)

    plt.show()
    return None


def _get_possible_x_velocities(target: Area) -> set[int]:
    xs: set[int] = set()
    for n in range(target.xmax):
        total = sum([n - i for i in range(n)])
        if target.xmin <= total <= target.xmax:
            xs.add(n)
        if total > target.xmax:
            break
    return xs


def find_highest_accurate_initial_velocity(target: Area) -> Point:
    """Find the initial velocity that hits the target after reaching the highest point.

    Args:
        target (Area): Target area.

    Raises:
        BaseException: If no solution is found.

    Returns:
        Point: Velocity that reaches the highest point and still hits the target.
    """
    possible_vx = _get_possible_x_velocities(target)
    best_v = (-1, -1)
    for vx in possible_vx:
        for vy in range(floor(target.center[1]), 200):
            res = run_simulation((vx, vy), target)
            if res.hit and vy > best_v[1]:
                best_v = (vx, vy)
    if best_v[0] < 0:
        raise BaseException("Did not find any solutions...")
    return best_v


def main() -> None:
    """Run code for 'Day 17: Trick Shot'."""
    _plot = False
    # Part 1.
    # Examples.
    ex_area = parse_target_area_input(_example_target_area)
    res = run_simulation((7, 2), ex_area)
    check_example(True, res.hit and res.passed_through)
    if _plot:
        plot_simulation(res, ex_area)

    res = run_simulation(v_initial=(6, 3), target_area=ex_area)
    check_example(True, res.hit and res.passed_through)
    if _plot:
        plot_simulation(res, ex_area)

    res = run_simulation(v_initial=(9, 0), target_area=ex_area)
    check_example(True, res.hit and res.passed_through)
    if _plot:
        plot_simulation(res, ex_area)

    res = run_simulation(v_initial=(17, -4), target_area=ex_area)
    check_example(True, (not res.hit) and res.passed_through)
    if _plot:
        plot_simulation(res, ex_area)

    res = run_simulation(v_initial=(6, 9), target_area=ex_area)
    check_example(True, res.hit and res.passed_through)
    if _plot:
        plot_simulation(res, ex_area)

    v = find_highest_accurate_initial_velocity(ex_area)
    check_example((6, 9), v)

    target_area = get_puzzle_target_area()
    best_initial_v = find_highest_accurate_initial_velocity(target_area)
    res = run_simulation(best_initial_v, target_area)
    highest_y = res.highest_point[1]
    if _plot:
        plot_simulation(res, target_area)
    print_single_answer(PI.day, 1, highest_y)
    check_answer(5565, highest_y, day=PI.day, part=1)
    return None


if __name__ == "__main__":
    main()
