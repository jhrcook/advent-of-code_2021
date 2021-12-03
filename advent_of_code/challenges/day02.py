"""Day 2: Dive."""

from enum import Enum
from typing import Final

from pydantic import BaseModel

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path
from advent_of_code.utils import assert_never

DAY: Final[int] = 2


example_sub_course = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


class SubDirection(Enum):
    """Possible directions for a submaine."""

    FORWARD = "FORWARD"
    DOWN = "DOWN"
    UP = "UP"


class CourseInstruction(BaseModel):
    """Course instruction."""

    direction: SubDirection
    value: int

    def __str__(self) -> str:
        """Human-readable reprepresentation of a course instruction."""
        return f"{self.direction.value} {self.value}"

    def __repr__(self) -> str:
        """Human-readable reprepresentation of a course instruction."""
        return str(self)


class Submarine:
    """Submarine."""

    hor: int
    depth: int
    aim: int

    def __init__(self) -> None:
        """Create a submarine."""
        self.hor = 0
        self.depth = 0
        self.aim = 0

    def incorrect_move(self, by: CourseInstruction) -> None:
        """Move per a submarine course instruction (part 1).

        This command is used for Part 1 of the challenge, but Part 2 says this was
        "incorrect" and makes it more complicated.

        Args:
            by (CourseInstruction): Instruction.
        """
        if by.direction is SubDirection.FORWARD:
            self.hor += by.value
        elif by.direction is SubDirection.DOWN:
            self.depth += by.value
        elif by.direction is SubDirection.UP:
            self.depth -= by.value
        else:
            assert_never(by.direction)

    def incorrect_follow_course(self, course: list[CourseInstruction]) -> None:
        """Follow a list of submarine direction instructions (part 1).

        This command is used for Part 1 of the challenge, but Part 2 says this was
        "incorrect" and makes it more complicated.

        Args:
            course (list[CourseInstruction]): Instructions.
        """
        for instruction in course:
            self.incorrect_move(instruction)
        return None

    def move(self, by: CourseInstruction) -> None:
        """Move per a submarine course instruction.

        Args:
            by (CourseInstruction): Instruction.
        """
        if by.direction is SubDirection.FORWARD:
            self.hor += by.value
            self.depth += self.aim * by.value
        elif by.direction is SubDirection.DOWN:
            self.aim += by.value
        elif by.direction is SubDirection.UP:
            self.aim -= by.value
        else:
            assert_never(by.direction)

    def follow_course(self, course: list[CourseInstruction]) -> None:
        """Follow a list of submarine direction instructions.

        Args:
            course (list[CourseInstruction]): Instructions.
        """
        for instruction in course:
            self.move(instruction)
        return None

    def __str__(self) -> str:
        """Human-readable reprepresentation of a submarine."""
        return f"hor: {self.hor}, depth: {self.depth}"

    def __repr__(self) -> str:
        """Human-readable reprepresentation of a submarine."""
        return str(self)


def _parse_instruction(str_instruction: str) -> CourseInstruction:
    direction, value = str_instruction.split(" ")
    return CourseInstruction(direction=direction.upper(), value=int(value))


def _parse_instructions(data: str) -> list[CourseInstruction]:
    return [_parse_instruction(x) for x in data.strip().splitlines()]


def _read_instructions() -> list[CourseInstruction]:
    p = get_data_path(DAY)
    with open(p, "r") as file:
        instructions = [_parse_instruction(line.strip()) for line in file]
    return instructions


if __name__ == "__main__":
    # Data.
    example_instructions = _parse_instructions(example_sub_course)
    course_instructions = _read_instructions()

    # Part 1.
    # Example.
    sub = Submarine()
    sub.incorrect_follow_course(example_instructions)
    check_example(150, sub.depth * sub.hor)
    # Real.
    sub = Submarine()
    sub.incorrect_follow_course(course_instructions)
    res = sub.hor * sub.depth
    print_single_answer(DAY, 1, res)
    check_answer(1507611, res, day=DAY, part=1)

    # Part 2.
    # Example.
    sub = Submarine()
    sub.follow_course(example_instructions)
    check_example(900, sub.depth * sub.hor)
    # Real.
    sub = Submarine()
    sub.follow_course(course_instructions)
    res = sub.hor * sub.depth
    print_single_answer(DAY, 1, res)
    check_answer(1880593125, res, day=DAY, part=2)
