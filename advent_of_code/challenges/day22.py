"""Day 22: Reactor Reboot."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Optional

import numpy as np
from shapely.geometry import Polygon

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=22, title="Reactor Reboot")

ReactorSet = set[tuple[int, int, int]]


def _range_p1(x: tuple[int, int]) -> range:
    return range(x[0], x[1] + 1)


@dataclass
class RebootInstruction:
    """A single reboot instruction."""

    turn_on: bool
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @property
    def shape2d(self) -> Polygon:
        """Reboot instruction as a polygon."""
        x1, x2 = self.x
        y1, y2 = self.y
        x2 += 1
        y2 += 1
        return Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

    def apply(self, reactor: np.ndarray) -> None:
        """Apply the reboot instruction to a reactor.

        Args:
            reactor (np.ndarray): Reactor array (modified in place).
        """
        assert reactor.ndim == 3
        (x1, x2), (y1, y2), (z1, z2) = self.x, self.y, self.z
        reactor[x1 : (x2 + 1), y1 : (y2 + 1), z1 : (z2 + 1)] = self.turn_on
        return None

    def translate(self, dx: int, dy: int, dz: int) -> None:
        """Move coordinates."""
        self.x = (self.x[0] + dx, self.x[1] + dx)
        self.y = (self.y[0] + dy, self.y[1] + dy)
        self.z = (self.z[0] + dz, self.z[1] + dz)
        return None

    def __hash__(self) -> int:
        """Hash of object."""
        return hash((self.turn_on, self.x, self.y, self.z))


RebootInstructions = list[RebootInstruction]


def parse_reboot_instructions(data: str) -> RebootInstructions:
    """Parse data into a collection of reboot instructions."""
    cuboids: RebootInstructions = []
    for line in data.strip().splitlines():
        line = line.strip()
        on_off, ranges = line.split(" ", maxsplit=1)
        xs, ys, zs = tuple([a.split("=")[1] for a in ranges.split(",")])
        x = tuple([int(a) for a in xs.split("..")])
        y = tuple([int(a) for a in ys.split("..")])
        z = tuple([int(a) for a in zs.split("..")])
        cuboids.append(RebootInstruction(on_off == "on", x=x, y=y, z=z))  # type: ignore
    return cuboids


def _get_example_cuboid_instructions(i: int) -> RebootInstructions:
    return parse_reboot_instructions(read_data(PI.day, f"example-input{i}.txt"))


def _get_cuboid_instructions() -> RebootInstructions:
    return parse_reboot_instructions(read_data(PI.day))


def _filter_within_50(instructions: RebootInstructions) -> RebootInstructions:
    new_instructions: RebootInstructions = []
    for i in instructions:
        if all(-50 <= a[0] and a[1] <= 50 for a in [i.x, i.y, i.z]):
            new_instructions.append(i)
    return new_instructions


def _assert_pos(ri: RebootInstruction) -> None:
    assert min(ri.x) >= 0 and min(ri.y) >= 0 and min(ri.z) >= 0
    return None


def translate_instruction_positions_to_positives(
    instructions: RebootInstructions,
) -> None:
    """Translate a collection of instructions to all be positive.

    Args:
        instructions (RebootInstructions): Same instructions, just shifted to be
        positive.
    """
    min_x = min([min(i.x) for i in instructions])
    min_y = min([min(i.y) for i in instructions])
    min_z = min([min(i.z) for i in instructions])
    for instruction in instructions:
        instruction.translate(dx=-min_x, dy=-min_y, dz=-min_z)
        _assert_pos(instruction)


def apply_instructions(reactor: np.ndarray, instructions: RebootInstructions) -> None:
    """Apply instructions to a reactor.

    Args:
        reactor (np.ndarray): Reactor array.
        instructions (RebootInstructions): Collection of instructions.
    """
    for instruction in instructions:
        instruction.apply(reactor)
    return None


def make_reactor(instructions: RebootInstructions) -> np.ndarray:
    """Create a reactor to fit all of the instructions."""
    x = max([i.x[1] for i in instructions])
    y = max([i.y[1] for i in instructions])
    z = max([i.z[1] for i in instructions])
    return np.zeros((x + 1, y + 1, z + 1), dtype=bool)


def _iter_over_zrange(instructions: RebootInstructions) -> range:
    z_min = min(min(i.z) for i in instructions)
    z_max = max(max(i.z) for i in instructions)
    return range(z_min, z_max + 1)


def _filter_instructions_by_z(
    instructions: RebootInstructions, z: int
) -> RebootInstructions:
    return [i for i in instructions if i.z[0] <= z <= i.z[1]]


@cache
def apply_instructions_2d(instructions: tuple[RebootInstruction, ...]) -> int:
    """Apply instructions over a 2D slice of a reactor.

    Args:
        instructions (tuple[RebootInstruction, ...]): Reboot instructions for a slice.

    Returns:
        int: Number of cuboids turned on.
    """
    shape: Optional[Polygon] = None
    for i in instructions:
        if shape is None and not i.turn_on:
            continue
        elif shape is None and i.turn_on:
            shape = i.shape2d
        elif i.turn_on:
            shape = shape.union(i.shape2d)  # type: ignore
        elif not i.turn_on:
            shape = shape.difference(i.shape2d)  # type: ignore

    if shape is None:
        return 0
    return int(shape.area)


def number_cubes_on_after_restart(instructions: RebootInstructions) -> int:
    """Follow reboot instructions and count the number of cubes on in the end.

    Args:
        instructions (RebootInstructions): Reboot instructions.

    Returns:
        int: Number of on cubes
    """
    total_on = 0
    for z in _iter_over_zrange(instructions):
        z_instructions = _filter_instructions_by_z(instructions, z=z)
        cubes_on = apply_instructions_2d(tuple(z_instructions))
        total_on += cubes_on
    return total_on


def main() -> None:
    """Run code for 'Day 22: Reactor Reboot'."""
    # Part 1.
    # Example.
    ex_instructions = _get_example_cuboid_instructions(1)
    ex_instructions = _filter_within_50(ex_instructions)
    translate_instruction_positions_to_positives(ex_instructions)
    ex_reactor = make_reactor(ex_instructions)
    apply_instructions(ex_reactor, ex_instructions)
    check_example(590784, np.sum(ex_reactor))

    # Real.
    instructions = _get_cuboid_instructions()
    instructions = _filter_within_50(instructions)
    translate_instruction_positions_to_positives(instructions)
    reactor = make_reactor(instructions)
    apply_instructions(reactor, instructions)
    res = np.sum(reactor)
    print_single_answer(PI.day, 1, res)
    check_answer(590467, res, day=PI.day, part=1)

    # Part 2.
    # Examples.
    ex_instructions = _get_example_cuboid_instructions(2)
    translate_instruction_positions_to_positives(ex_instructions)
    ex_res = number_cubes_on_after_restart(ex_instructions)
    check_example(2758514936282235, ex_res)

    # Real.
    instructions = _get_cuboid_instructions()
    translate_instruction_positions_to_positives(instructions)
    n_cubes = number_cubes_on_after_restart(instructions)
    print_single_answer(day=PI.day, part=2, value=n_cubes)
    check_answer(1225064738333321, n_cubes, PI.day, 2)
    return None


if __name__ == "__main__":
    main()
