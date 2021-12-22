"""Day 22: Reactor Reboot."""

from dataclasses import dataclass

import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=22, title="Reactor Reboot")


@dataclass
class RebootInstruction:
    """A single reboot instruction."""

    turn_on: bool
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    def apply(self, reactor: np.ndarray) -> None:
        """Apply this instruction to a reactor."""
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


def parse_reboot_instructions(data: str) -> list[RebootInstruction]:
    """Parse data into a collection of reboot instructions."""
    cuboids: list[RebootInstruction] = []
    for line in data.strip().splitlines():
        line = line.strip()
        on_off, ranges = line.split(" ", maxsplit=1)
        xs, ys, zs = tuple([a.split("=")[1] for a in ranges.split(",")])
        x = tuple([int(a) for a in xs.split("..")])
        y = tuple([int(a) for a in ys.split("..")])
        z = tuple([int(a) for a in zs.split("..")])
        cuboids.append(RebootInstruction(on_off == "on", x=x, y=y, z=z))  # type: ignore
    return cuboids


def _get_example_cuboid_instructions(i: int) -> list[RebootInstruction]:
    return parse_reboot_instructions(read_data(PI.day, f"example-input{i}.txt"))


def _get_cuboid_instructions() -> list[RebootInstruction]:
    return parse_reboot_instructions(read_data(PI.day))


def _filter_within_50(instructions: list[RebootInstruction]) -> list[RebootInstruction]:
    new_instructions: list[RebootInstruction] = []
    for i in instructions:
        if all(-50 <= a[0] and a[1] <= 50 for a in [i.x, i.y, i.z]):
            new_instructions.append(i)
    return new_instructions


def _assert_pos(ri: RebootInstruction) -> None:
    assert min(ri.x) >= 0 and min(ri.y) >= 0 and min(ri.z) >= 0
    return None


def translate_instruction_positions_to_positives(
    instructions: list[RebootInstruction],
) -> None:
    """Translate a collection of instructions to all be positive.

    Args:
        instructions (list[RebootInstruction]): Same instructions, just shifted to be
        positive.
    """
    min_x = min([min(i.x) for i in instructions])
    min_y = min([min(i.y) for i in instructions])
    min_z = min([min(i.z) for i in instructions])
    for instruction in instructions:
        instruction.translate(dx=-min_x, dy=-min_y, dz=-min_z)
        _assert_pos(instruction)


def apply_instructions(
    reactor: np.ndarray, instructions: list[RebootInstruction]
) -> None:
    """Apply instructions to a reactor.

    Args:
        reactor (np.ndarray): Reactor array.
        instructions (list[RebootInstruction]): Collection of instructions.
    """
    for instruction in instructions:
        instruction.apply(reactor)
    return None


def make_reactor(instructions: list[RebootInstruction]) -> np.ndarray:
    """Create a reactor to fit all of the instructions."""
    x = max([i.x[1] for i in instructions])
    y = max([i.y[1] for i in instructions])
    z = max([i.z[1] for i in instructions])
    return np.zeros((x + 1, y + 1, z + 1), dtype=bool)


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
    return None


if __name__ == "__main__":
    main()
