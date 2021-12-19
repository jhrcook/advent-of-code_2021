"""Day 18: Snailfish."""

from __future__ import annotations

from itertools import product
from math import ceil, floor
from typing import Any, Optional, Union

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=18, title="Snailfish")


class SFNum:
    """Represent a snailfish number as an 'ordered' tree."""

    parent: Optional[SFNum]
    left: Union[int, SFNum]
    right: Union[int, SFNum]

    def __init__(
        self, parent: Optional[SFNum], left: Union[int, SFNum], right: Union[int, SFNum]
    ) -> None:
        """Create a snailfish number object.

        Args:
            parent (Optional[SFNum]): The parent, if any, of this snailfish number pair.
            left (Union[int, SFNum]): Left value.
            right (Union[int, SFNum]): Right value.
        """
        self.parent = parent
        self.left = left
        self.right = right
        return None

    def __eq__(self, right: Any) -> bool:
        """Equate two snailfish numbers."""
        return str(self) == str(right)

    def __add__(self, right: SFNum) -> SFNum:
        """Add two snailfish numbers together."""
        return SFNum(parent=None, left=self, right=right)

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"[{self.left},{self.right}]"

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)


def _list_to_snailfish_number(data: list[Any], parent: Optional[SFNum] = None) -> SFNum:
    assert len(data) == 2
    sf_num = SFNum(parent=parent, left=-1, right=-1)
    left_data = data[0]
    right_data = data[1]

    if isinstance(left_data, int):
        sf_num.left = left_data
    else:
        sf_num.left = _list_to_snailfish_number(left_data, parent=sf_num)

    if isinstance(right_data, int):
        sf_num.right = right_data
    else:
        sf_num.right = _list_to_snailfish_number(right_data, parent=sf_num)

    return sf_num


def parse_snailfish_number(data: str) -> SFNum:
    """Parse a string into snailfish data."""
    return _list_to_snailfish_number(eval(data))


def parse_snailfish_numbers(data: str) -> list[SFNum]:
    """Parse a collection of snailfish numbers."""
    pairs: list[SFNum] = []
    for line in data.strip().splitlines():
        pairs.append(parse_snailfish_number(line))
    return pairs


def _get_example_snailfish_numbers() -> list[SFNum]:
    _data = """
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    [7,[5,[[3,8],[1,4]]]]
    [[2,[2,2]],[8,[8,1]]]
    [2,9]
    [1,[[[9,3],9],[[9,0],[0,7]]]]
    [[[5,[7,4]],7],1]
    [[[[4,2],2],6],[8,7]]
    """
    return parse_snailfish_numbers(_data)


def _get_example_snailfish_numbers2() -> list[SFNum]:
    _data = """
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """
    return parse_snailfish_numbers(_data)


def _get_puzzle_snailfish_numbers() -> list[SFNum]:
    return parse_snailfish_numbers(read_data(PI.day))


def split(sf_num: SFNum) -> SFNum:
    """Split a snailfish number as a part of the reducing process.

    Args:
        sf_num (SFNum): Snailfish number.

    Returns:
        SFNum: Updated number.
    """
    sf_num_0: str = str(sf_num)

    if isinstance(sf_num.left, SFNum):
        sf_num.left = split(sf_num.left)
    elif sf_num.left >= 10:
        x = sf_num.left
        sf_num.left = SFNum(parent=sf_num, left=floor(x / 2), right=ceil(x / 2))

    if str(sf_num) != sf_num_0:
        return sf_num

    if isinstance(sf_num.right, SFNum):
        sf_num.right = split(sf_num.right)
    elif sf_num.right >= 10:
        x = sf_num.right
        sf_num.right = SFNum(parent=sf_num, left=floor(x / 2), right=ceil(x / 2))

    return sf_num


def _add_to_first_left_value_going_down(sf_num: SFNum, value: int) -> None:
    if isinstance(sf_num.left, int):
        sf_num.left += value
    else:
        _add_to_first_left_value_going_down(sf_num.left, value)
    return None


def _add_to_first_right_value_going_down(sf_num: SFNum, value: int) -> None:
    if isinstance(sf_num.right, int):
        sf_num.right += value
    else:
        _add_to_first_right_value_going_down(sf_num.right, value)
    return None


def _add_to_first_value_to_the_right(sf_num: SFNum, value: int) -> None:
    if sf_num.parent is None:
        return None
    elif isinstance(sf_num.parent.right, int):
        sf_num.parent.right += value
    elif sf_num.parent.right is not sf_num:
        _add_to_first_left_value_going_down(sf_num.parent.right, value)
    else:
        _add_to_first_value_to_the_right(sf_num.parent, value)
    return None


def _add_to_first_value_to_the_left(sf_num: SFNum, value: int) -> None:
    if sf_num.parent is None:
        return None
    elif isinstance(sf_num.parent.left, int):
        sf_num.parent.left += value
    elif sf_num.parent.left is not sf_num:
        _add_to_first_right_value_going_down(sf_num.parent.left, value)
    else:
        _add_to_first_value_to_the_left(sf_num.parent, value)
    return None


def explode(sf_num: SFNum, layer: int = 1) -> SFNum:
    """Explode a snailfish number as a part of the reducing process.

    Args:
        sf_num (SFNum): Snailfish number.
        layer (int, optional): Current layer of the number. Defaults to 1.

    Returns:
        SFNum: Updated snailfish number.
    """
    sf_num_0: str = str(sf_num)

    if layer == 4:
        if isinstance(sf_num.left, SFNum):
            left_val, right_val = sf_num.left.left, sf_num.left.right
            assert isinstance(left_val, int) and isinstance(right_val, int)
            if isinstance(sf_num.right, int):
                sf_num.right += right_val
            else:
                assert isinstance(sf_num.right.left, int)
                sf_num.right.left += right_val
            _add_to_first_value_to_the_left(sf_num, left_val)
            sf_num.left = 0
            return sf_num
        elif isinstance(sf_num.right, SFNum):
            left_val, right_val = sf_num.right.left, sf_num.right.right
            assert isinstance(left_val, int) and isinstance(right_val, int)
            if isinstance(sf_num.left, int):
                sf_num.left += left_val
            else:
                assert isinstance(sf_num.left.right, int)
                sf_num.left.right += left_val
            _add_to_first_value_to_the_right(sf_num, right_val)
            sf_num.right = 0
            return sf_num

    if str(sf_num) != sf_num_0:
        return sf_num

    if isinstance(sf_num.left, SFNum):
        explode(sf_num.left, layer + 1)

    if str(sf_num) != sf_num_0:
        return sf_num

    if isinstance(sf_num.right, SFNum):
        explode(sf_num.right, layer + 1)

    return sf_num


def _rebuild_snailfish_number(sf_num: SFNum) -> SFNum:
    return parse_snailfish_number(str(sf_num))


def reduce_snailfish_number(sf_num: SFNum) -> SFNum:
    """Reduce a snailfish number."""
    sf_num_0: str = ""
    while str(sf_num) != sf_num_0:
        sf_num = _rebuild_snailfish_number(sf_num)
        sf_num_0 = str(sf_num)
        sf_num = explode(sf_num)
        if str(sf_num) == sf_num_0:
            sf_num = split(sf_num)
    return sf_num


def perform_addition(sf_nums: list[SFNum]) -> SFNum:
    """Add together a list of snailfish numbers.

    Args:
        sf_nums (list[SFNum]): List of snailfish numbers.

    Returns:
        SFNum: Cumulative sum of the snailfish numbers.
    """
    sf_num = sf_nums[0]
    for i in range(1, len(sf_nums)):
        sf_num += sf_nums[i]
        sf_num = reduce_snailfish_number(sf_num)
    return sf_num


def snailfish_number_magnitude(sf_num: SFNum) -> int:
    """Calculate the 'magnitude' of a snailfish number.

    Args:
        sf_num (SFNum): Snailfish number.

    Returns:
        int: Magnitude.
    """
    if isinstance(sf_num.left, int):
        left = sf_num.left
    else:
        left = snailfish_number_magnitude(sf_num.left)

    if isinstance(sf_num.right, int):
        right = sf_num.right
    else:
        right = snailfish_number_magnitude(sf_num.right)

    return left * 3 + right * 2


def find_larget_magnitude(sf_nums: list[SFNum]) -> int:
    """Find the larget magnitude from adding two different snailfish numbers.

    Args:
        sf_nums (list[SFNum]): List of snailfish numbers.

    Returns:
        int: Larget magnitude.
    """
    magnitudes: list[int] = []
    for a, b in product(sf_nums, sf_nums):
        if a == b:
            continue
        s1 = snailfish_number_magnitude(perform_addition([a, b]))
        s2 = snailfish_number_magnitude(perform_addition([b, a]))
        magnitudes.append(s1)
        magnitudes.append(s2)
    return max(magnitudes)


def main() -> None:
    """Run code for 'Day 18: Snailfish'."""
    # Part 1.
    # Examples.
    ex_nums = """
    [[[[4,3],4],4],[7,[[8,4],9]]]
    [1,1]
    """
    ex_snail_nums = parse_snailfish_numbers(ex_nums)
    check_example(2, len(ex_snail_nums))
    ex_added = ex_snail_nums[0] + ex_snail_nums[1]
    check_example(str(ex_added), "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")

    a = explode(parse_snailfish_number("[[[[[9,8],1],2],3],4]"))
    check_example("[[[[0,9],2],3],4]", a)
    b = explode(parse_snailfish_number("[7,[6,[5,[4,[3,2]]]]]"))
    check_example("[7,[6,[5,[7,0]]]]", b)
    ex_snail_num = parse_snailfish_number("[[6,[5,[4,[3,2]]]],1]")
    c = explode(ex_snail_num)
    check_example("[[6,[5,[7,0]]],3]", c)
    d = explode(parse_snailfish_number("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"))
    check_example("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", d)

    a = split(parse_snailfish_number("[[[[0,7],4],[15,[0,13]]],[1,1]]"))
    check_example("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", a)
    b = split(a)
    check_example("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", b)

    reduced_added = reduce_snailfish_number(ex_added)
    check_example("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", reduced_added)

    ex_sf_nums = _get_example_snailfish_numbers()
    ex_addition_res = perform_addition(ex_sf_nums)
    check_example(
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", ex_addition_res
    )
    check_example(3488, snailfish_number_magnitude(ex_addition_res))

    # Real.
    snailfish_numbers = _get_puzzle_snailfish_numbers()
    snailfish_sum = perform_addition(snailfish_numbers)
    snailfish_sum_mag = snailfish_number_magnitude(snailfish_sum)
    print_single_answer(day=PI.day, part=1, value=snailfish_sum_mag)
    check_answer(4207, snailfish_sum_mag, day=PI.day, part=1)

    # Part 2.
    # Examples.
    ex_sf_nums = _get_example_snailfish_numbers2()
    ex_largest_mag = find_larget_magnitude(ex_sf_nums)
    check_example(3993, ex_largest_mag)

    # Real.
    snailfish_numbers = _get_puzzle_snailfish_numbers()
    largest_mag = find_larget_magnitude(snailfish_numbers)
    print_single_answer(day=PI.day, part=2, value=largest_mag)
    check_example(4635, largest_mag)
    return None


if __name__ == "__main__":
    main()
