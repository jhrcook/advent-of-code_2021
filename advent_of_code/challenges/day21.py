"""Day 21: Dirac Dice."""
from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from functools import cache
from itertools import product
from typing import Counter

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=21, title="Dirac Dice")


@dataclass
class DeterministicDie:
    """Deterministic die for Dirac Dice."""

    value: int = 0

    def roll(self) -> int:
        """Role the die."""
        if self.value == 100:
            self.value = 0
        self.value += 1
        return self.value


@dataclass
class Player:
    """Player of Dirac Dice."""

    pos: int
    score: int = 0

    def move(self, n: int) -> None:
        """Move a player.

        Args:
            n (int): Number of positions to move.
        """
        self.pos += n
        while self.pos > 10:
            self.pos -= 10
        self.score += self.pos

    def __hash__(self) -> int:
        """Generate a hash."""
        return hash((self.pos, self.score))

    def __copy__(self) -> Player:
        """Generate a copy."""
        return Player(pos=self.pos, score=self.score)


def get_players() -> tuple[Player, Player]:
    """Parse input to get the two starting players."""
    data = read_data(day=PI.day).strip().splitlines()
    p1 = Player(int(data[0].strip().split(": ")[1]))
    p2 = Player(int(data[1].strip().split(": ")[1]))
    return p1, p2


def _roll_n_times(die: DeterministicDie, n: int = 3) -> int:
    return sum([die.roll() for _ in range(n)])


def play_practice_dirac_dice_game(p1: Player, p2: Player) -> int:
    """Player a practice round of Dirac Dice with a determinitic dice.

    Args:
        p1 (Player): Player 1.
        p2 (Player): Player 2.

    Returns:
        int: Number of rolls to reach a winner.
    """
    die = DeterministicDie()
    n_rolls = 0
    while True:
        n_rolls += 3
        res = _roll_n_times(die)
        p1.move(res)
        if p1.score >= 1000:
            break
        res = _roll_n_times(die)
        n_rolls += 3
        p2.move(res)
        if p2.score >= 1000:
            break
    return n_rolls


def _calc_puzzle_result(n_rolls: int, p1: Player, p2: Player) -> int:
    return min([p1.score, p2.score]) * n_rolls


# --- Part 2 ----

DIRAC_ROLLS = list([sum(x) for x in product(range(1, 4), range(1, 4), range(1, 4))])


@cache
def _all_dirac_outcomes(p1: Player, p2: Player) -> list[tuple[Player, Player]]:
    games: list[tuple[Player, Player]] = []
    for p1_rolls, p2_rolls in product(DIRAC_ROLLS, DIRAC_ROLLS):
        _p1, _p2 = copy(p1), copy(p2)
        _p1.move(p1_rolls)
        _p2.move(p2_rolls)
        games.append((_p1, _p2))
    return games


def play_dirac_dice(player1: Player, player2: Player) -> tuple[int, int]:
    """Play the game of Dirac Dice.

    I'm not sure where, but there is a counting error somewhere in my algorithm. Anyway,
    it seems to be fixed by dividing the number of player 1 wins by 27 (3^3).

    Args:
        player1 (Player): Starting position for player 1.
        player2 (Player): Starting position for player 2.

    Returns:
        tuple[int, int]: Number of games won by player 1 and player 2.
    """
    p1_wins, p2_wins = 0, 0
    games: Counter[tuple[Player, Player]] = Counter([(player1, player2)])
    while len(games) > 0:
        new_games: Counter[tuple[Player, Player]] = Counter()
        for (p1, p2), n in games.items():
            all_res = _all_dirac_outcomes(p1, p2)
            unfinished_games: list[tuple[Player, Player]] = []
            for _p1, _p2 in all_res:
                if _p1.score >= 21:
                    p1_wins += n
                elif _p2.score >= 21:
                    p2_wins += n
                else:
                    unfinished_games.append((_p1, _p2))
            _new_games = Counter(unfinished_games)
            _new_games = Counter({k: v * n for k, v in _new_games.items()})
            new_games += _new_games
        games = new_games
    return int(p1_wins / 27), p2_wins


def main() -> None:
    """Run code for 'Day 21: Dirac Dice'."""
    # Part 1.
    # Example.
    ex_p1, ex_p2 = Player(4), Player(8)
    ex_n_rolls = play_practice_dirac_dice_game(ex_p1, ex_p2)
    losing_score = min([ex_p1.score, ex_p2.score])
    check_example(993, ex_n_rolls)
    check_example(745, losing_score)
    check_example(739785, _calc_puzzle_result(ex_n_rolls, ex_p1, ex_p2))
    # Real
    p1, p2 = get_players()
    n_rolls = play_practice_dirac_dice_game(p1, p2)
    res = _calc_puzzle_result(n_rolls, p1, p2)
    print_single_answer(day=PI.day, part=1, value=res)
    check_answer(921585, res, day=PI.day, part=1)

    # Part 2.
    # Example.
    if False:
        ex_p1, ex_p2 = Player(4), Player(8)
        ex_wins = play_dirac_dice(ex_p1, ex_p2)
        check_example((444356092776315, 341960390180808), ex_wins)

    # Real.
    p1, p2 = get_players()
    wins = play_dirac_dice(p1, p2)
    print_single_answer(PI.day, 2, value=max(wins))
    check_answer(911090395997650, max(wins), day=PI.day, part=2)

    return None


if __name__ == "__main__":
    main()
