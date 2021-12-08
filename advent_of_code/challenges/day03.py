"""Day 3: Binary Diagnostic."""

from typing import Callable, Final

import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 3

_example_diagnostic_report = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def _report_to_array(report: list[list[bool]]) -> np.ndarray:
    return np.asarray(report.copy())


def _array_to_report(ary: np.ndarray) -> list[list[bool]]:
    return ary.astype(bool).tolist()


def _ints_to_bin(values: list[int]) -> int:
    """Convert a list of binary bits to the integer (decimal) value."""
    return int("".join([str(x) for x in values]), 2)


def _most_common_in_column(ary: np.ndarray) -> list[int]:
    """Find the most common value in an array."""
    return [int(round(np.mean(ary[:, i]))) for i in range(ary.shape[1])]


def _oxygen_generator_bit_criteria(values: np.ndarray) -> int:
    _avg = np.mean(values)
    if _avg == 0.5:
        return 1
    return int(round(_avg))


def _co2_scrubber_bit_criteria(values: np.ndarray) -> int:
    _avg = (np.mean(values) * -1) + 1
    if _avg == 0.5:
        return 0
    else:
        return int(round(_avg))


def _filter_report_values_by_bit_criteria(
    report: list[list[bool]],
    bit_criteria: Callable[[np.ndarray], int],
    bit_idx: int = 0,
) -> int:
    ary = _report_to_array(report)
    bit_target = bit_criteria(ary[:, bit_idx])
    _mask = ary[:, bit_idx] == bit_target
    ary = ary[_mask, :]
    new_report = _array_to_report(ary)
    if len(new_report) == 1:
        res = [int(x) for x in new_report[0]]
        return _ints_to_bin(res)
    else:
        return _filter_report_values_by_bit_criteria(
            new_report, bit_criteria=bit_criteria, bit_idx=bit_idx + 1
        )


class DiagnosticReport:
    """Diagnostic report."""

    report: list[list[bool]]

    def __init__(self, report: list[list[bool]]) -> None:
        """Create a diagnostic report object."""
        self.report = report

    def gamma_rate(self) -> int:
        """Get the gamma rate from the diagnostic report."""
        ary = _report_to_array(self.report)
        gamma = _most_common_in_column(ary)
        return _ints_to_bin(gamma)

    def epsilon_rate(self) -> int:
        """Get the epsilon rate from the diagnostic report."""
        ary = _report_to_array(self.report)
        ary = (ary * -1) + 1
        eps = _most_common_in_column(ary)
        return _ints_to_bin(eps)

    def calc_power_consumption(self) -> int:
        """Calculate the power consumption from the diagnostic report."""
        return self.gamma_rate() * self.epsilon_rate()

    def oxygen_generator_rating(self) -> int:
        """Calculate the oxygen generator rating from the diagnostic report."""
        return _filter_report_values_by_bit_criteria(
            self.report, _oxygen_generator_bit_criteria
        )

    def co2_scrubber_rating(self) -> int:
        """Calculate the CO2 scrubber rating from the diagnostic report."""
        return _filter_report_values_by_bit_criteria(
            self.report, _co2_scrubber_bit_criteria
        )

    def calc_life_support_rating(self) -> int:
        """Calculate the life support rating from the diagnostic report."""
        return self.oxygen_generator_rating() * self.co2_scrubber_rating()


def _parse_diagnostic_report(data: str) -> list[list[bool]]:
    report: list[list[bool]] = []
    for line in data.strip().splitlines():
        report.append([bool(int(x)) for x in line.strip()])
    return report


def _parse_diagnostic_report_file() -> list[list[bool]]:
    p = get_data_path(DAY)
    report: list[list[bool]] = []
    with open(p, "r") as file:
        for line in file:
            report.append([bool(int(x)) for x in line.strip()])
    return report


def main() -> None:
    """Execute code for day 3."""
    # Data
    example_report_code = _parse_diagnostic_report(_example_diagnostic_report)
    report_code = _parse_diagnostic_report_file()

    # Part 1.
    example_report = DiagnosticReport(example_report_code)
    check_example(22, example_report.gamma_rate())
    check_example(9, example_report.epsilon_rate())
    report = DiagnosticReport(report_code)
    pow_consumption = report.calc_power_consumption()
    print_single_answer(DAY, 1, pow_consumption)
    check_answer(852500, pow_consumption, DAY, 1)

    # Part 2.
    check_example(23, example_report.oxygen_generator_rating())
    check_example(10, example_report.co2_scrubber_rating())
    life_support = report.calc_life_support_rating()
    print_single_answer(DAY, 2, life_support)
    check_answer(1007985, life_support, DAY, 2)


if __name__ == "__main__":
    main()
