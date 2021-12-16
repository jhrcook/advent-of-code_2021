"""Day 13: Transparent Origami."""

from enum import Enum

import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path
from advent_of_code.utils import PuzzleInfo

PUZZLE_INFO = PuzzleInfo(day=13, title="Transparent Origami")


_example_instructions = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


class FoldAxis(Enum):
    """Possible folding axes."""

    Y = "Y"
    X = "X"


class FoldInstruction:
    """A folding instruction."""

    axis: FoldAxis
    value: int

    def __init__(self, instruction: str) -> None:
        """Create a folding instruction.

        Args:
            instruction (str): The instruction string.
        """
        parts = instruction.replace("fold along ", "").split("=")
        self.axis = FoldAxis(parts[0].upper())
        self.value = int(parts[1])
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"fold {self.axis.value.lower()} = {self.value}"

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)


def _coords_to_array(coords: list[tuple[int, int]]) -> np.ndarray:
    max_r = np.max([c[1] for c in coords]) + 1
    max_c = np.max([c[0] for c in coords]) + 1
    ary = np.zeros((max_r, max_c), dtype=bool)
    for coord in coords:
        c, r = coord
        ary[r, c] = True
    return ary


def _parse_manual_instructions(
    instructions_str: str,
) -> tuple[np.ndarray, list[FoldInstruction]]:
    coords: list[tuple[int, int]] = []
    folds: list[FoldInstruction] = []
    instruction_lines = instructions_str.strip().splitlines()
    while True:
        line = instruction_lines.pop(0).strip()
        if line == "":
            break
        coord = [int(a) for a in line.split(",")]
        assert len(coord) == 2
        coords.append((coord[0], coord[1]))
    for line in instruction_lines:
        line = line.strip()
        folds.append(FoldInstruction(line))
    return _coords_to_array(coords), folds


def _get_example_data() -> tuple[np.ndarray, list[FoldInstruction]]:
    return _parse_manual_instructions(_example_instructions)


def get_data() -> tuple[np.ndarray, list[FoldInstruction]]:
    """Get the puzzle input.

    Returns:
        tuple[np.ndarray, list[FoldInstruction]]: The array to be folded and a list of
        folding instructions.
    """
    data = ""
    with open(get_data_path(PUZZLE_INFO.day), "r") as file:
        for line in file:
            data += line
    return _parse_manual_instructions(data)


def print_array(ary: np.ndarray) -> None:
    """Print an array in an easy-to-read format."""
    ary = ary.copy().astype(str)
    ary[ary == "True"] = "#"
    ary[ary == "False"] = "."
    str_ary = ""
    for row in range(ary.shape[0]):
        str_ary += "".join(ary[row, :].tolist()) + "\n"
    str_ary = str_ary
    print(str_ary)
    return None


def _match_num_rows(
    ary1: np.ndarray, ary2: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    ary1, ary2 = ary1.copy(), ary2.copy()
    n_rows_1, n_rows_2 = ary1.shape[0], ary2.shape[0]
    _diff = np.abs(n_rows_1 - n_rows_2)
    if n_rows_2 < n_rows_1:
        ary2 = np.pad(
            ary2, ((_diff, 0), (0, 0)), mode="constant", constant_values=False
        )
    elif n_rows_1 < n_rows_2:
        ary1 = np.pad(
            ary1, ((_diff, 0), (0, 0)), mode="constant", constant_values=False
        )
    assert ary1.shape == ary2.shape
    return ary1, ary2


def fold_array(ary: np.ndarray, fold: FoldInstruction) -> np.ndarray:
    """Fold an array.

    Args:
        ary (np.ndarray): Array to fold.
        fold (FoldInstruction): Folding instructions.

    Returns:
        np.ndarray: Folded array.
    """
    ary = ary.copy()
    if fold.axis is FoldAxis.X:
        ary = np.rot90(ary, 3)

    top = ary[0 : fold.value, :]
    bottom = ary[(fold.value + 1) :, :]
    bottom = np.flipud(bottom)
    top, bottom = _match_num_rows(top, bottom)
    ary = top + bottom

    if fold.axis is FoldAxis.X:
        ary = np.rot90(ary, k=1)

    return ary


def complete_folds(
    ary: np.ndarray, folds: list[FoldInstruction], verbose: bool = False
) -> np.ndarray:
    """Conduct a list of folds on an array.

    Args:
        ary (np.ndarray): Array to fold.
        folds (list[FoldInstruction]): Fold instructions.
        verbose (bool, optional): Print out intermediate results. Defaults to False.

    Returns:
        np.ndarray: Final folded array.
    """
    if verbose:
        print("Starting array:")
        print_array(ary)
    for fold in folds:
        ary = fold_array(ary, fold)
        if verbose:
            print_array(ary)

    if verbose:
        print("Final array:")
        print_array(ary)
    return ary


def main() -> None:
    """Run code for 'Day 13: Transparent Origami'."""
    # Part 1.
    # Example.
    ex_ary, ex_folds = _get_example_data()
    ex_ary = fold_array(ex_ary, ex_folds[0])
    check_example(17, np.sum(ex_ary))
    # Real.
    array, folds = get_data()
    array = fold_array(array, folds[0])
    num_points = np.sum(array)
    print_single_answer(PUZZLE_INFO.day, 1, num_points)
    check_answer(837, num_points, day=PUZZLE_INFO.day, part=1)

    # Part 2.
    # Example.
    ex_ary, ex_folds = _get_example_data()
    ex_ary = complete_folds(ex_ary, ex_folds, verbose=False)
    check_example(7, ex_ary.shape[0])
    check_example(5, ex_ary.shape[1])
    check_example(16, np.sum(ex_ary))
    # Real.
    array, folds = get_data()
    array = complete_folds(array, folds, verbose=False)
    # print_array(array)  # Un-comment to see real output.
    print_single_answer(PUZZLE_INFO.day, 2, "EPZGKCHU")
    return None


if __name__ == "__main__":
    main()
