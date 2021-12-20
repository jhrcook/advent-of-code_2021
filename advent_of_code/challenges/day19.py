"""Day 19: Beacon Scanner."""
from __future__ import annotations

from copy import deepcopy
from enum import Enum
from functools import cache
from itertools import product
from typing import Any

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo, assert_never

PI = PuzzleInfo(day=19, title="Beacon Scanner")


class Axis(Enum):
    """Available axes."""

    X = "X"
    Y = "Y"
    Z = "Z"


class Beacon:
    """Location beacon."""

    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int) -> None:
        """Create a location beacon object."""
        self.x, self.y, self.z = x, y, z
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)

    def __copy__(self) -> Beacon:
        """Copy a beacon object to a new object."""
        return Beacon(self.x, self.y, self.z)

    def __eq__(self, b: Any) -> bool:
        """Is this beacon equal to another."""
        return self.x == b.x and self.y == b.y and self.z == b.z

    def __hash__(self) -> int:
        """Hash of this beacon."""
        return hash((self.x, self.y, self.z))

    def __getitem__(self, axis: Axis) -> int:
        """Index a beacon's location values.

        Args:
            axis (Axis): Axis to retreive.

        Returns:
            int: Value along that axis.
        """
        if axis is Axis.X:
            return self.x
        elif axis is Axis.Y:
            return self.y
        elif axis is Axis.Z:
            return self.z
        else:
            assert_never(axis)

    def translate(self, x: int, y: int, z: int) -> None:
        """Translate the beacon.

        Args:
            x (int): Change along the x-dimension.
            y (int): Change along the y-dimension.
            z (int): Change along the z-dimension.
        """
        self.x += x
        self.y += y
        self.z += z

    def rotate_90(self, around_axis: Axis) -> None:
        """Rotate a point 90 deg. around an axis.

        Source:
        https://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space

        Args:
            around_axis (Axis): Axis to rotate around.

        Raises:
            BaseException: If the axis is unknown.
        """
        # sin(90) = 1  and  cos(90) = 0
        x, y, z = self.x, self.y, self.z
        if around_axis is Axis.X:
            self.y = -z  # y cos θ − z sin θ
            self.z = y  # y sin θ + z cos θ
        elif around_axis is Axis.Y:
            self.x = z  # x cos θ + z sin θ
            self.z = -x  # −x sin θ + z cos θ
        elif around_axis is Axis.Z:
            self.x = -y  # x cos θ − y sin θ
            self.y = x  # x sin θ + y cos θ
        else:
            assert_never(around_axis)


class Scanner:
    """Scanner sensor."""

    id: str
    beacons: list[Beacon]
    center: Beacon

    def __init__(self, id: str, beacons: list[Beacon]) -> None:
        """Create a scanner object.

        Args:
            id (str): Unique identifier.
            beacons (list[Beacon]): List of detected beacons.
        """
        self.id = id
        self.beacons = deepcopy(beacons)
        self.center = Beacon(0, 0, 0)
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"scanner {self.id} | {len(self.beacons)} beacons | center: {self.center}"
        )

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)

    def __copy__(self) -> Scanner:
        """Make a duplicate object."""
        return Scanner(self.id, beacons=deepcopy(self.beacons))

    def __hash__(self) -> int:
        """Hash of this scanner object."""
        return hash(f"{self.id} | {self.center} | {self.beacons}")

    def translate_beacons(self, x: int, y: int, z: int) -> None:
        """Translate the scanner and its beacons locations.

        Args:
            x (int): Change along the x-dimension.
            y (int): Change along the y-dimension.
            z (int): Change along the z-dimension.
        """
        self.center.translate(x=x, y=y, z=z)
        for beacon in self.beacons:
            beacon.translate(x=x, y=y, z=z)

    def rotate_beacons_90(self, around_axis: Axis) -> None:
        """Rotate a scanner and its beacons aruond an axis.

        Args:
            around_axis (Axis): Axis to rotate around.
        """
        self.center.rotate_90(around_axis=around_axis)
        for beacon in self.beacons:
            beacon.rotate_90(around_axis=around_axis)
        return None


def _parse_single_scanner_data(data: str) -> list[Beacon]:
    split_data = data.strip().splitlines()
    title_line = split_data.pop(0)
    assert "scanner" in title_line
    beacons: list[Beacon] = []
    for pt in split_data:
        xyz: tuple[int, ...] = tuple([int(x) for x in pt.strip().split(",")])
        assert len(xyz) == 3
        beacons.append(Beacon(*xyz))
    return beacons


def parse_scanner_data(data: str) -> list[Scanner]:
    """Parse scanner data from a string to a list of scanner objects."""
    scanners: list[Scanner] = []
    for i, scanner_data in enumerate(data.strip().split("\n\n")):
        scanner = Scanner(id=str(i), beacons=_parse_single_scanner_data(scanner_data))
        scanners.append(scanner)
    return scanners


def _get_example_data() -> list[Scanner]:
    data = read_data(day=PI.day, name="example-input.txt")
    return parse_scanner_data(data)


def _get_puzzle_data() -> list[Scanner]:
    data = read_data(day=PI.day)
    return parse_scanner_data(data)


def get_overlapping_beacons(s1: Scanner, s2: Scanner) -> set[Beacon]:
    """Get the set of beacons shared by two scanners.

    Args:
        s1 (Scanner): Scanner 1.
        s2 (Scanner): Scanner 2.

    Returns:
        set[Beacon]: Set of shared beacons.
    """
    b1 = set(s1.beacons)
    b2 = set(s2.beacons)
    return b1.intersection(b2)


def count_overlapping_beacons(s1: Scanner, s2: Scanner) -> int:
    """Count the number of shared beacons.

    Args:
        s1 (Scanner): Scanner 1.
        s2 (Scanner): Scanner 2.

    Returns:
        int: Number of overlapping beacons.
    """
    return len(get_overlapping_beacons(s1, s2))


def _try_rotations(s1: Scanner, s2: Scanner) -> bool:
    for _ in range(4):
        s2.rotate_beacons_90(Axis.X)
        for _ in range(4):
            s2.rotate_beacons_90(Axis.Y)
            for _ in range(4):
                s2.rotate_beacons_90(Axis.Z)
                if count_overlapping_beacons(s1, s2) >= 12:
                    return True
    return False


def _recenter_scanners(s1: Scanner, s2: Scanner) -> None:
    s = deepcopy(s1.center)
    s1.translate_beacons(-s.x, -s.y, -s.z)
    s2.translate_beacons(-s.x, -s.y, -s.z)
    return None


@cache
def find_overlap_between_scanners(
    scanner_1: Scanner, scanner_2: Scanner
) -> tuple[Scanner, Scanner, bool]:
    """Search for the overlap of two scanners.

    The algorithm works by iterating over the beacons. For each pair, the scanners and
    their beacons are translated such that the two beacons are at the origin (0,0). Then
    all possible rotations are attempted until at least 12 beacons overlap.

    Args:
        scanner_1 (Scanner): Scanner 1.
        scanner_2 (Scanner): Scanner 2.

    Returns:
        tuple[Scanner, Scanner, bool]: The final scanners and whether or not a
        satisfactory overlap was found.
    """
    for b1, b2 in product(scanner_1.beacons, scanner_2.beacons):
        s1 = deepcopy(scanner_1)
        s2 = deepcopy(scanner_2)
        s1.translate_beacons(-b1.x, -b1.y, -b1.z)
        s2.translate_beacons(-b2.x, -b2.y, -b2.z)
        assert count_overlapping_beacons(s1, s2) > 0
        res = _try_rotations(s1, s2)
        if res:
            _recenter_scanners(s1, s2)
            return s1, s2, True
    return scanner_1, scanner_2, False


def _remove_solved_scanners_from_remaining_list(
    solved: list[Scanner], scanners: list[Scanner]
) -> list[Scanner]:
    solved_ids = set([s.id for s in solved])
    return [s for s in scanners if s.id not in solved_ids]


def solve_overlapping_scanners(scanners: list[Scanner]) -> list[Scanner]:
    """Solve the orientations of overallping scanners.

    First, a pair of scanners is found with satisfactory overlap. Then, the remaining
    scanners are added to those seeds until all scanners have been added.

    Args:
        scanners (list[Scanner]): List of scanners.

    Returns:
        list[Scanner]: Re-oriented scanners such that they form a contiguous network.
    """
    scanners = deepcopy(scanners)
    solved_scanners: list[Scanner] = []
    s1 = scanners[0]
    for s2 in scanners:
        if s1.id == s2.id:
            continue
        s1, s2, res = find_overlap_between_scanners(s1, s2)
        if res:
            print(f"first solved: {s1.id} - {s2.id}")
            solved_scanners.append(deepcopy(s1))
            solved_scanners.append(deepcopy(s2))
            break

    assert len(solved_scanners) == 2
    scanners = _remove_solved_scanners_from_remaining_list(
        solved=solved_scanners, scanners=scanners
    )

    while len(scanners) > 0:
        print(f"num scanners left: {len(scanners)}")
        for seed_scanner, s2 in product(solved_scanners, scanners):
            _, s2, res = find_overlap_between_scanners(seed_scanner, s2)
            if res:
                c = deepcopy(seed_scanner.center)
                s2.translate_beacons(c.x, c.y, c.z)
                assert count_overlapping_beacons(seed_scanner, s2) >= 12
                print(f"solved: {seed_scanner.id} - {s2.id}")
                solved_scanners.append(deepcopy(s2))
                scanners = _remove_solved_scanners_from_remaining_list(
                    solved=solved_scanners, scanners=scanners
                )
                break

    return solved_scanners


def unique_beacons(scanners: list[Scanner]) -> set[Beacon]:
    """Set of unique beacons in a collection of scanners.

    Args:
        scanners (list[Scanner]): Collection of scanners.

    Returns:
        set[Beacon]: All unique beacons.
    """
    beacons: set[Beacon] = set()
    for s in scanners:
        beacons = beacons.union(s.beacons)
    return beacons


def count_unique_beacons(scanners: list[Scanner]) -> int:
    """Count the number of unique beacons in a collection of scanners.

    Args:
        scanners (list[Scanner]): Collection of scanners.

    Returns:
        int: Number of unique beacons.
    """
    return len(unique_beacons(scanners))


def maximum_manhattan_distance(scanners: list[Scanner]) -> int:
    """Find the maximum Manhattan distance between all scanners.

    Args:
        scanners (list[Scanner]): Collection of scanners.

    Returns:
        int: Maximum Manhattan distance.
    """
    dists: list[int] = []
    for s1, s2 in product(scanners, scanners):
        if s1 is s2:
            continue
        c1, c2 = deepcopy(s1.center), deepcopy(s2.center)
        diffs = [c1.x - c2.x, c1.y - c2.y, c1.z - c2.z]
        dists.append(sum([abs(a) for a in diffs]))
    return max(dists)


def main() -> None:
    """Run code for 'Day 19: Beacon Scanner'."""
    # Part 1.
    # Examples.
    ex_scanner_data = _get_example_data()

    new_s0, new_s1, res = find_overlap_between_scanners(
        ex_scanner_data[0], ex_scanner_data[1]
    )
    check_example(True, res)
    check_example(12, count_overlapping_beacons(new_s0, new_s1))

    new_s1, new_s4, res = find_overlap_between_scanners(
        ex_scanner_data[1], ex_scanner_data[4]
    )
    check_example(True, res)
    check_example(12, count_overlapping_beacons(new_s1, new_s4))

    ex_solved_scanners = solve_overlapping_scanners(ex_scanner_data)
    check_example(len(ex_scanner_data), len(ex_solved_scanners))
    ex_beacons = unique_beacons(ex_solved_scanners)
    check_example(79, len(ex_beacons))

    # Real.
    scanners = _get_puzzle_data()
    solved_scanners = solve_overlapping_scanners(scanners)
    num_beacons = count_unique_beacons(solved_scanners)
    print_single_answer(day=PI.day, part=1, value=num_beacons)
    check_answer(457, num_beacons, day=PI.day, part=1)

    # Part 2.
    # Examples.
    ex_dist = maximum_manhattan_distance(ex_solved_scanners)
    check_example(3621, ex_dist)
    # Real.
    man_dist = maximum_manhattan_distance(solved_scanners)
    print_single_answer(day=PI.day, part=2, value=man_dist)
    check_answer(13243, man_dist, day=PI.day, part=2)
    return None


if __name__ == "__main__":
    main()
