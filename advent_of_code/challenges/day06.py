"""Day 6: Lanternfish."""

from __future__ import annotations

from typing import Final, Optional

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
        return f"After {self.day:2d} days: {len(self)} fish"

    def __repr__(self) -> str:
        """Human-readable description of the population."""
        return str(self)


def _parse_lanternfish_ages_str(age_str: str) -> list[LanternFish]:
    return [LanternFish(int(x)) for x in age_str.strip().split(",")]


def _get_lanternfish_ages_data() -> LanternFishPopulation:
    fish: list[LanternFish] = []
    with open(get_data_path(DAY), "r") as file:
        for line in file:
            fish += _parse_lanternfish_ages_str(line)
    return LanternFishPopulation(fish)


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


if __name__ == "__main__":
    main()
