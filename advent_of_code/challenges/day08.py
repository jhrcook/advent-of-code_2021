"""Day 8: Seven Segment Search."""

from collections import Counter
from copy import deepcopy
from typing import Callable, Final

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 8

_example_single_data_entry = """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
"""

_example_data = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

segment_counts: Final[dict[int, int]] = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}


segments_map: Final[dict[str, int]] = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


CHARS: Final[str] = "abcdefg"


possible_segment_mapping = dict[str, set[str]]
segment_mapping = dict[str, str]


def _sort_string(x: str) -> str:
    return "".join(sorted(x))


def convert_input_signal_to_output_segments(
    signal: str, inout_map: segment_mapping
) -> str:
    """Unscramble an input signal.

    Args:
        signal (str): Scrambled input signal.
        inout_map (segment_mapping): Mapping of input signal to correct segment.

    Returns:
        str: Intended input signal.
    """
    converted = [inout_map[i] for i in signal]
    converted.sort()
    return "".join(converted)


def convert_input_signal_to_output(signal: str, inout_map: segment_mapping) -> int:
    """Convert a scrambled input signal to an output value.

    Args:
        signal (str): Scrambled input signal.
        inout_map (segment_mapping): Mapping of input signal to correct segment.

    Returns:
        int: Intended output value.
    """
    return segments_map[convert_input_signal_to_output_segments(signal, inout_map)]


class SevenSegmentData:
    """Data for a single sevent-segment display."""

    signal_patterns: list[str]
    output: list[str]

    def __init__(self, data_entry: str) -> None:
        """Initialize a seven-segment data object.

        Args:
            data_entry (str): Data entry.
        """
        _data = [x.strip() for x in data_entry.strip().lower().split("|")]
        assert len(_data) == 2
        self.signal_patterns = [_sort_string(x) for x in _data[0].split(" ")]
        self.output = [_sort_string(x) for x in _data[1].split(" ")]
        # self.signal_patterns.sort()
        # self.output.sort()
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"{' '.join(self.signal_patterns)}  ->  {' '.join(self.output)}"

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)


class SevenSegmentDisplay:
    """Actual display values for a seven-segment display."""

    signal: list[int]
    output: list[int]

    def __init__(self, ss_data: SevenSegmentData, seg_map: segment_mapping) -> None:
        """Make a seven-segment display object.

        Args:
            ss_data (SevenSegmentData): Scrambled seven-segment display data.
            seg_map (segment_mapping): Map of input signal values to the correct
            segment.
        """
        self.signal = [
            convert_input_signal_to_output(s, seg_map) for s in ss_data.signal_patterns
        ]
        self.output = [
            convert_input_signal_to_output(s, seg_map) for s in ss_data.output
        ]
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        signal = [str(x) for x in self.signal]
        output = [str(x) for x in self.output]
        return f"{' '.join(signal)}  ->  {' '.join(output)}"

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)

    @property
    def value(self) -> int:
        """Get the output value for the seven-segment display."""
        return int("".join([str(x) for x in self.output]))


def _get_example_single_data() -> SevenSegmentData:
    return SevenSegmentData(_example_single_data_entry)


def _get_example_data() -> list[SevenSegmentData]:
    data: list[SevenSegmentData] = []
    for entry in _example_data.strip().splitlines():
        data.append(SevenSegmentData(entry))
    return data


def _get_data() -> list[SevenSegmentData]:
    with open(get_data_path(DAY), "r") as file:
        data = [SevenSegmentData(line) for line in file if len(line.strip()) > 0]
    return data


def count_easy_digits(segments: list[SevenSegmentData]) -> int:
    """Count the number of times a 1, 4, 7, or 8 appear in the ouput.

    Args:
        segments (list[SevenSegmentData]): List of seven-segment data objects.

    Returns:
        int: Count of easy-to-identify digits.
    """
    ct = 0
    easies = {2, 3, 4, 7}
    for segment in segments:
        for data in segment.output:
            if len(data) in easies:
                ct += 1
    return ct


def _check_segments_map() -> None:
    for key, value in segments_map.items():
        assert "".join(sorted(key)) == key
        assert value in set(range(10))
    return None


# ---- Rules ----

SegmentRule = Callable[[possible_segment_mapping, SevenSegmentData], None]
RULES: dict[str, SegmentRule] = {}


def segment_rule(fxn: SegmentRule) -> SegmentRule:
    """Register a seven-segment rule."""
    RULES[fxn.__name__] = fxn
    return fxn


def _get_code_for_easy_digit(ss: SevenSegmentData, expected_len: int) -> str:
    res = [segments for segments in ss.signal_patterns if len(segments) == expected_len]
    assert len(res) == 1
    return res[0]


def _get_one(ss: SevenSegmentData) -> str:
    return _get_code_for_easy_digit(ss, expected_len=2)


def _get_four(ss: SevenSegmentData) -> str:
    return _get_code_for_easy_digit(ss, expected_len=4)


def _get_seven(ss: SevenSegmentData) -> str:
    return _get_code_for_easy_digit(ss, expected_len=3)


def _get_eight(ss: SevenSegmentData) -> str:
    return _get_code_for_easy_digit(ss, expected_len=7)


def _get_all_fives(ss: SevenSegmentData) -> set[str]:
    res = [c for c in ss.signal_patterns if len(c) == 5]
    assert len(res) == 3
    return set(res)


def _get_all_sixes(ss: SevenSegmentData) -> set[str]:
    res = [c for c in ss.signal_patterns if len(c) == 6]
    assert len(res) == 3
    return set(res)


def update_segment_map(
    seg_map: possible_segment_mapping, char: str, possibles: set[str]
) -> None:
    """Update a segment map (in place).

    The new set of possible segments for a charater is the intersection of the existing
    possibilities and new ones.

    Args:
        seg_map (possible_segment_mapping): Segment map of input signals to possible
        output segments.
        char (str): Input signal to update.
        possibles (set[str]): Possible output segments.
    """
    seg_map[char] = seg_map[char].intersection(possibles)


def _sets_of_characters_to_counter(sets: set[str]) -> Counter:
    return Counter("".join(sets))


@segment_rule
def rule_by_count_in_one_and_seven(
    seg_map: possible_segment_mapping, ss: SevenSegmentData
) -> None:
    """Segment rule for the counts of segments expected between 1 and 7."""
    one = _get_one(ss)
    seven = _get_seven(ss)
    counts = _sets_of_characters_to_counter({one, seven})
    for c, count in counts.items():
        if count == 0:
            update_segment_map(seg_map, c, {"b", "d", "e", "g"})
        elif count == 1:
            update_segment_map(seg_map, c, {"a"})
        elif count == 2:
            update_segment_map(seg_map, c, {"c", "f"})
        else:
            raise BaseException("Unreachable")


@segment_rule
def rule_by_count_in_four_or_seven(
    seg_map: possible_segment_mapping, ss: SevenSegmentData
) -> None:
    """Segment rule for the counts of segments expected between 4 and 7."""
    four = _get_four(ss)
    seven = _get_seven(ss)
    counts = _sets_of_characters_to_counter({four, seven})
    for c, count in counts.items():
        if count == 0:
            update_segment_map(seg_map, c, {"e", "g"})
        elif count == 1:
            update_segment_map(seg_map, c, {"a", "b", "d"})
        elif count == 2:
            update_segment_map(seg_map, c, {"c", "f"})
        else:
            raise BaseException("Unreachable")


@segment_rule
def rule_by_count_in_one_or_four(
    seg_map: possible_segment_mapping, ss: SevenSegmentData
) -> None:
    """Segment rule for the counts of segments expected between 1 and 4."""
    one = _get_one(ss)
    four = _get_four(ss)
    counts = _sets_of_characters_to_counter({one, four})
    for c, count in counts.items():
        if count == 0:
            update_segment_map(seg_map, c, {"a", "e", "g"})
        elif count == 1:
            update_segment_map(seg_map, c, {"b", "d"})
        elif count == 2:
            update_segment_map(seg_map, c, {"c", "f"})
        else:
            raise BaseException("Unreachable")


@segment_rule
def rule_by_count_in_one_four_or_seven(
    seg_map: possible_segment_mapping, ss: SevenSegmentData
) -> None:
    """Segment rule for the counts of segments expected between 1, 4, and 7."""
    one = _get_one(ss)
    four = _get_four(ss)
    seven = _get_seven(ss)
    counts = _sets_of_characters_to_counter({one, four, seven})
    for c, count in counts.items():
        if count == 0:
            update_segment_map(seg_map, c, {"e", "g"})
        elif count == 1:
            update_segment_map(seg_map, c, {"a", "b", "d"})
        elif count == 2:
            raise BaseException("Unreachable")
        elif count == 3:
            update_segment_map(seg_map, c, {"c", "f"})
        else:
            raise BaseException("Unreachable")


@segment_rule
def rule_by_count_in_length_fives(
    seg_map: possible_segment_mapping, ss: SevenSegmentData
) -> None:
    """Segment rule for the counts of segments expected for digitis of 5 segments."""
    all_fives = _get_all_fives(ss)
    counts = _sets_of_characters_to_counter(all_fives)
    for char, count in counts.items():
        if count == 1:
            update_segment_map(seg_map, char, {"b", "e"})
        elif count == 2:
            update_segment_map(seg_map, char, {"c", "f"})
        elif count == 3:
            update_segment_map(seg_map, char, {"a", "d", "g"})
        else:
            raise BaseException("Unreachable")


@segment_rule
def rule_by_count_in_length_sixes(
    seg_map: possible_segment_mapping, ss: SevenSegmentData
) -> None:
    """Segment rule for the counts of segments expected for digitis of 6 segments."""
    all_sixes = _get_all_sixes(ss)
    counts = _sets_of_characters_to_counter(all_sixes)
    for char, count in counts.items():
        if count == 3:
            update_segment_map(seg_map, char, {"a", "b", "f", "g"})
        elif count == 2:
            update_segment_map(seg_map, char, {"c", "d", "e"})
        else:
            raise BaseException("Unreachable")


@segment_rule
def rule_remove_solved(seg_map: possible_segment_mapping, ss: SevenSegmentData) -> None:
    """Segment rule tpo remove possible segments when the segment has been solved.

    If a input signal only has one possibility, then that ouput segment is "solved" and
    can be removed from the possiblities of the other input signals.
    """
    can_remove: list[str] = []
    for possibles in seg_map.values():
        if len(possibles) == 1:
            can_remove.append(list(possibles)[0])
    for remove in can_remove:
        for char, possibles in seg_map.items():
            if len(possibles) == 1:
                continue
            seg_map[char] = possibles.difference(remove)


def _init_possible_segment_mapping() -> possible_segment_mapping:
    segment_chars = "abcdefg"
    return {c: set(segment_chars) for c in segment_chars}


def single_mapping(segment_map: possible_segment_mapping) -> bool:
    """Whether all of the input segments mapped to a single ouput segment.

    Args:
        segment_map (possible_segment_mapping): Segment map.

    Returns:
        bool: Are all of the input segments mapped to a single ouput segment?
    """
    return all([len(b) == 1 for b in segment_map.values()])


def _finalize_segment_map(segment_map: possible_segment_mapping) -> segment_mapping:
    return {a: list(b)[0] for a, b in segment_map.items()}


class NoFinalSegmentMapFound(BaseException):
    """No final segment map found."""

    def __init__(
        self, segment_data: SevenSegmentData, segment_map: possible_segment_mapping
    ) -> None:
        """No final segment map found."""
        msg = "\n"
        msg += str(segment_data) + "\n"
        msg += "segment map:\n"
        for key, possibles in segment_map.items():
            msg += f"  {key}: {', '.join(possibles)}\n"
        super().__init__(msg)


def discover_segment_mapping(
    segment_data: SevenSegmentData, verbose: bool = True
) -> segment_mapping:
    """Discover the mapping between scrambled input signals and output segments.

    Args:
        segment_data (SevenSegmentData): Seven-segment data.
        verbose (bool, optional): Print information during process. Defaults to True.

    Raises:
        NoFinalSegmentMapFound: Failed to find a segment map.

    Returns:
        segment_mapping: Final mapping of each input signal to an output signal.
    """
    segment_map = _init_possible_segment_mapping()
    _previous_seg_map: possible_segment_mapping = {}
    i = 0
    while segment_map != _previous_seg_map:
        i += 1
        if verbose:
            print(f"iteration {i}")
        _previous_seg_map = deepcopy(segment_map)
        for name, rule in RULES.items():
            if verbose:
                print(f"Applying rule: '{name}'")
            rule(segment_map, segment_data)
            if single_mapping(segment_map):
                return _finalize_segment_map(segment_map)
    raise NoFinalSegmentMapFound(segment_data, segment_map)


def get_display_value(segment_data: SevenSegmentData) -> SevenSegmentDisplay:
    """Solve a scrambled seven-segment display.

    Args:
        segment_data (SevenSegmentData): Scrambled seven-segment display data.

    Returns:
        SevenSegmentDisplay: Unscrambled seven-segment display data.
    """
    segment_map_solution = discover_segment_mapping(segment_data, verbose=False)
    return SevenSegmentDisplay(ss_data=segment_data, seg_map=segment_map_solution)


def main() -> None:
    """Run code for day 7 'Seven Segment Search'."""
    _check_segments_map()

    # Part 1.
    ex_data = _get_example_data()
    ex_ct_easy_digits = count_easy_digits(ex_data)
    check_example(26, ex_ct_easy_digits)
    segment_data = _get_data()
    ct_easy_digits = count_easy_digits(segment_data)
    print_single_answer(DAY, 1, ct_easy_digits)
    check_answer(479, ct_easy_digits, DAY, 1)

    # Part 2.
    # Example with single entry of segment data.
    ex_data_entry = _get_example_single_data()
    ex_seg_map_soln = discover_segment_mapping(ex_data_entry, verbose=False)
    x = convert_input_signal_to_output_segments("acedgfb", ex_seg_map_soln)
    check_example("abcdefg", x)
    y = segments_map[x]
    check_example(8, y)
    ex_ss_display = SevenSegmentDisplay(ex_data_entry, ex_seg_map_soln)
    [
        check_example(a, b)
        for a, b in zip([8, 5, 2, 3, 7, 9, 6, 4, 0, 1], ex_ss_display.signal)
    ]
    [check_example(a, b) for a, b in zip([5, 3, 5, 3], ex_ss_display.output)]
    check_example(5353, ex_ss_display.value)
    # Example with multiple segment data entries.
    ex_data = _get_example_data()
    ex_res = sum([get_display_value(ss).value for ss in ex_data])
    check_example(61229, ex_res)
    # On real input.
    segment_data = _get_data()
    sum_display_values = sum([get_display_value(ss).value for ss in segment_data])
    print_single_answer(DAY, 2, sum_display_values)
    check_answer(1041746, sum_display_values, day=DAY, part=2)
    return None


if __name__ == "__main__":
    main()
