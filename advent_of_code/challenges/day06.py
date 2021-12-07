"""Day 6: Lanternfish."""

from __future__ import annotations

from collections import Counter
from functools import cache
from typing import Final, Optional

import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 6

_ex_lanternfish_ages: Final[str] = "3,4,3,1,2"


class LanternFish:
    """A single lanternfish."""

    age: int

    def __init__(self, age: int = 8) -> None:
        """Create a new lanternfish.

        Args:
            age (int, optional): Age of the lanternfish. Defaults to 8.
        """
        self.age = age
        return None

    def new_day(self) -> Optional[LanternFish]:
        """Adavance the age of the fish by one day.

        Returns:
            Optional[LanternFish]: If the lanternfish reproduced, its offspring is
            returned.
        """
        if self.age == 0:
            self.age = 6
            return LanternFish()
        else:
            self.age -= 1
            return None

    def __str__(self) -> str:
        """Human-readable description of the lanternfish."""
        return str(self.age)

    def __repr__(self) -> str:
        """Human-readable description of the lanternfish."""
        return str(self)


class LanternFishPopulation:
    """Population of lanternfish."""

    day: int
    lanternfishes: list[LanternFish]

    def __init__(self, lanternfishes: list[LanternFish]) -> None:
        """Create a population of lanternfish.

        Args:
            lanternfishes (list[LanternFish]): Population of lanternfish.
        """
        self.day = 0
        self.lanternfishes = lanternfishes
        return None

    def new_day(self) -> None:
        """Advance the population's age by one day."""
        self.day += 1
        new_fishes: list[LanternFish] = []
        for fish in self.lanternfishes:
            new_fish = fish.new_day()
            if new_fish is not None:
                new_fishes.append(new_fish)
        self.lanternfishes += new_fishes
        return None

    def advance(self, days: int) -> None:
        """Advance the population by a set number of days.

        Args:
            days (int): Number of days.
        """
        for _ in range(days):
            self.new_day()

    def __len__(self) -> int:
        """Size of the population."""
        return len(self.lanternfishes)

    def __str__(self) -> str:
        """Human-readable description of the population."""
        return f"After {self.day:3d} days: {len(self)} fish"

    def __repr__(self) -> str:
        """Human-readable description of the population."""
        return str(self)

    def show(self) -> None:
        """Display a population of fish ages."""
        fishes = ", ".join([str(f) for f in self.lanternfishes])
        print(f"After {self.day:3d} days: {fishes}")


# ---- Data parsing ---- #


def _parse_lanternfish_ages_str(age_str: str) -> list[LanternFish]:
    return [LanternFish(int(x)) for x in age_str.strip().split(",")]


def _get_lanternfish_ages_data() -> LanternFishPopulation:
    fish: list[LanternFish] = []
    with open(get_data_path(DAY), "r") as file:
        for line in file:
            fish += _parse_lanternfish_ages_str(line)
    return LanternFishPopulation(fish)


# ---- Part 2 ---- #


def _split_up_days(n_days: int, by: int) -> list[int]:
    if n_days < by:
        return [n_days]
    split_days = [by] * (n_days // by)
    rem = n_days % by
    if rem > 0:
        split_days += [rem]
    return split_days


@cache
def age_fish(fish: int, days: int) -> np.ndarray:
    """Age a single fish (memoized).

    Args:
        fish (int): Fish to age.
        days (int): Number of days to age the fish.

    Returns:
        np.ndarray: Resulting population of lanterfish.
    """
    ary = np.asarray([fish], dtype=int)
    for _ in range(days):
        ary = ary - 1
        idx = ary == -1
        ary[idx] = 6
        ary = np.hstack([ary, np.zeros(np.sum(idx), dtype=int) + 8])
    return ary


def age_a_population(
    population: LanternFishPopulation, days: int, day_split: int = 128
) -> int:
    """Age a population of lanternfish.

    While this is not a readable as the nice abstraction above, it is **far** more
    efficient and takes way less time to run for larger values of `days`.

    Args:
        population (LanternFishPopulation): Population of lanternfish.
        days (int): Days to age.
        day_split (int, optional): Split of day (recommend a value below 150 and an even
        split of the total number of days). Defaults to 128 (to go well with 256 days).

    Returns:
        int: Number of fish after the number of days.
    """
    fishes = np.array([f.age for f in population.lanternfishes], dtype=int)
    fish_age_count: Counter = Counter(fishes)
    for days_chunk in _split_up_days(days, day_split):
        new_fish_ages: Counter = Counter()
        for age, n_fish in fish_age_count.items():
            new_fish_ages += Counter(
                {  # type: ignore
                    a: n * n_fish for a, n in Counter(age_fish(age, days_chunk)).items()
                }
            )
        fish_age_count = new_fish_ages
    return sum(list(fish_age_count.values()))


def main() -> None:
    """Run code for day 6 challenge."""
    # Part 1.
    ex_fishes = LanternFishPopulation(_parse_lanternfish_ages_str(_ex_lanternfish_ages))
    fishes = _get_lanternfish_ages_data()
    ex_fishes.advance(80)
    check_example(5934, len(ex_fishes))
    fishes.advance(80)
    n_fish = len(fishes)
    print_single_answer(DAY, 1, n_fish)
    check_answer(351092, n_fish, DAY, 1)

    # Part 2.
    ex_fishes = LanternFishPopulation(_parse_lanternfish_ages_str(_ex_lanternfish_ages))
    ex_n_fish = age_a_population(ex_fishes, 80, day_split=40)
    check_example(5934, ex_n_fish)
    ex_n_fish = age_a_population(ex_fishes, 256, day_split=128)
    check_example(26984457539, ex_n_fish)
    fishes = _get_lanternfish_ages_data()
    n_fish = age_a_population(fishes, 256, day_split=128)
    print_single_answer(DAY, 2, n_fish)
    check_answer(1595330616005, n_fish, DAY, 2)

    return None


if __name__ == "__main__":
    main()
