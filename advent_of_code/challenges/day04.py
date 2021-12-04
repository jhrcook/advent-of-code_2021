"""Day 4: Giant Squid."""

from copy import deepcopy
from typing import Final, Optional

import numpy as np
from colorama import Fore, Style, init

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

init(autoreset=True)

DAY: Final[int] = 4

_example_bingo = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class BingoCard:
    """Bingo card."""

    card: np.ndarray
    marks: np.ndarray

    def __init__(self, card: np.ndarray) -> None:
        """Create a bingo card object."""
        assert card.shape == (5, 5), "Incorrect Bingo card dimensions."
        self.card = card
        self.marks = np.zeros_like(card, dtype=bool)

    def bingo_call(self, num: int) -> None:
        """Call a number in a game of bingo.

        Args:
            num (int): Number called.
        """
        self.marks[self.card == num] = True
        return None

    def _row_and_column_checks(self) -> tuple[list[bool], list[bool]]:
        dims = self.marks.shape
        row_check = [all(self.marks[i, :]) for i in range(dims[0])]
        col_check = [all(self.marks[:, i]) for i in range(dims[1])]
        return row_check, col_check

    def has_won(self) -> bool:
        """Whether or not the card has won."""
        row_check, col_check = self._row_and_column_checks()
        return any(row_check) or any(col_check)

    def winning_vector(self) -> Optional[np.ndarray]:
        """Get the vector (row or column) that won the game (if any).

        Returns:
            Optional[np.ndarray]: If any, the winning vector.
        """
        row_check, col_check = self._row_and_column_checks()
        if any(row_check):
            return self.card[row_check, :]
        elif any(col_check):
            return self.card[:, row_check]
        return None

    def sum_unmarkded_numbers(self) -> int:
        """Get the sum of the unmarked cells in the bingo card."""
        inv_marks = ((self.marks * -1) + 1).astype(bool)
        return np.sum(self.card[inv_marks])

    def __str__(self) -> str:
        """Human-readable format of the bingo card with marked cells highlighted."""
        dims = self.card.shape
        msg = ""
        for i in range(dims[0]):
            for j in range(dims[1]):
                val = f"{self.card[i, j]:2d}"
                m = self.marks[i, j]
                txt = (Fore.BLUE + Style.BRIGHT + val + Style.RESET_ALL) if m else val
                msg += " " + txt
            msg += "\n"
        return msg

    def __repr__(self) -> str:
        """Human-readable format of the bingo card with marked cells highlighted."""
        return str(self)


def _parse_bingo_card_info(card_str: str) -> BingoCard:
    card_str = card_str.strip()
    rows = [row.strip() for row in card_str.splitlines()]
    card_list = [[int(x) for x in row.split()] for row in rows]
    card = np.array(card_list)
    return BingoCard(card=card)


def _parse_bingo_string(data: str) -> tuple[list[int], list[BingoCard]]:
    data = data.strip()
    called_numbers = [int(x) for x in data.splitlines()[0].strip().split(",")]

    data = "\n".join(data.splitlines()[1:]).strip()
    bingo_cards = [
        _parse_bingo_card_info(card_info.strip()) for card_info in data.split("\n\n")
    ]
    return called_numbers, bingo_cards


def _parse_bingo_file() -> tuple[list[int], list[BingoCard]]:
    fpath = get_data_path(DAY)
    info_string = ""
    with open(fpath, "r") as file:
        for line in file:
            info_string += line
    return _parse_bingo_string(info_string)


def calculate_final_socre(card: BingoCard, num: int) -> int:
    """Calculate the final score of a Bingo game.

    Args:
        card (BingoCard): Winning card.
        num (int): Final number called.

    Returns:
        int: Bingo score.
    """
    return card.sum_unmarkded_numbers() * num


def play_bingo(
    cards: list[BingoCard], nums: list[int]
) -> Optional[tuple[BingoCard, int]]:
    """Play a game of bingo.

    Args:
        cards (list[BingoCard]): Bingo cards.
        nums (list[int]): Numbers called during the game.

    Returns:
        Optional[tuple[BingoCard, int]]: If there is a winner, return the winning card
        and last number called.
    """
    for num in nums:
        for card in cards:
            card.bingo_call(num)
            if card.has_won():
                return card, num
    return None


def get_last_to_win_bingo_card(
    cards: list[BingoCard], nums: list[int]
) -> Optional[tuple[BingoCard, int]]:
    """Get the last-to-win bingo card.

    Args:
        cards (list[BingoCard]): List of bingo cards.
        nums (list[int]): Numbers to call for bingo.

    Returns:
        Optional[tuple[BingoCard, int]]: If any, the last bingo card to win and the
        final number that would get it to win.
    """
    _cards = deepcopy(cards)
    for num in nums:
        for card in _cards:
            card.bingo_call(num)
            if card.has_won():
                _cards.remove(card)
        if len(_cards) == 1:
            return play_bingo(_cards, nums)
    return None


if __name__ == "__main__":
    # Data.
    ex_called_numbers, ex_bingo_cards = _parse_bingo_string(_example_bingo)
    called_numbers, bingo_cards = _parse_bingo_file()

    # Part 1.
    ex_bingo_res = play_bingo(ex_bingo_cards, ex_called_numbers)
    assert ex_bingo_res is not None, "No bingo winner found."
    ex_win_card, ex_win_num = ex_bingo_res
    check_example(24, ex_win_num)
    check_example(4512, calculate_final_socre(ex_win_card, ex_win_num))

    bingo_res = play_bingo(bingo_cards, called_numbers)
    assert bingo_res is not None, "No bingo winner found."
    winning_card, winning_num = bingo_res
    bingo_score = calculate_final_socre(winning_card, winning_num)
    print_single_answer(DAY, 1, bingo_score)
    check_answer(58374, bingo_score, DAY, 1)

    # Part 2.
    ex_bingo_last = get_last_to_win_bingo_card(ex_bingo_cards, ex_called_numbers)
    assert ex_bingo_last is not None, "No worst card found."
    ex_last_card, ex_last_num = ex_bingo_last
    check_example(13, ex_last_num)
    check_example(1924, calculate_final_socre(ex_last_card, ex_last_num))

    bingo_last = get_last_to_win_bingo_card(bingo_cards, called_numbers)
    assert bingo_last is not None, "No worst card found."
    last_card, last_num = bingo_last
    last_bingo_score = calculate_final_socre(last_card, last_num)
    print_single_answer(DAY, 2, last_bingo_score)
    check_answer(11377, last_bingo_score, DAY, 2)
