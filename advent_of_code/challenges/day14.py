"""Day 14: Extended Polymerization."""

from typing import Counter, Union

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PUZZLE_INFO = PuzzleInfo(day=14, title="Extended Polymerization")

_example_poylmer_data = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

PolymerTemplate = str


class PairInsertionRule:
    """Polymerization rule."""

    pair: str
    add: str
    replace: str

    def __init__(self, pair: str, add: str) -> None:
        """Make a polymerization rule object.

        Args:
            pair (str): Pair of characters to search for.
            add (str): Character to insert between the pair.
        """
        self.pair = pair
        self.add = add
        self.replace = self.pair[0] + ":" + self.add + ":" + self.pair[1]
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        return self.pair + " → " + self.add

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)

    def __hash__(self) -> int:
        """Hash of the polymerization rule."""
        return hash(self.pair + "->" + self.add)


def parse_polymer_data(data: str) -> tuple[PolymerTemplate, list[PairInsertionRule]]:
    """Parse polymer data into the template and rules."""
    split_data = data.strip().splitlines()
    polymer_template = split_data.pop(0).strip()
    insertion_rules: list[PairInsertionRule] = []
    for line in split_data:
        line = line.strip()
        if len(line) == 0:
            continue
        pair, add = line.split(" -> ")
        insertion_rules.append(PairInsertionRule(pair=pair, add=add))
    return polymer_template, insertion_rules


def apply_rule(template: PolymerTemplate, rule: PairInsertionRule) -> PolymerTemplate:
    """Apply a polymerization rule to a polymer template.

    Args:
        template (PolymerTemplate): Polymer template to work on.
        rule (PairInsertionRule): Polymerization insertion rule.

    Returns:
        PolymerTemplate: Resulting polymer.
    """
    if rule.pair not in template:
        return template
    _old_template = ""
    while True:
        _old_template = template
        template = template.replace(rule.pair, rule.replace)
        if _old_template == template:
            break
    return template


def apply_rules(
    template: PolymerTemplate, rules: list[PairInsertionRule]
) -> PolymerTemplate:
    """Apply polymerization rules to a polymer template.

    Args:
        template (PolymerTemplate): Polymer template to work on.
        rules (list[PairInsertionRule]): Polymerization insertion rules.

    Returns:
        PolymerTemplate: Resulting polymer.
    """
    for rule in rules:
        template = apply_rule(template=template, rule=rule)
    return template.replace(":", "")


def apply_rules_n(
    template: PolymerTemplate,
    rules: list[PairInsertionRule],
    n: int,
) -> PolymerTemplate:
    """Apply the polymerization insertion rules to a template repeatedly.

    Args:
        template (PolymerTemplate): Initial template.
        rules (list[PairInsertionRule]): Polymerization insertion rules.
        n (int): Number of repeats.

    Returns:
        PolymerTemplate: Final polymer.
    """
    for _ in range(n):
        template = apply_rules(template=template, rules=rules.copy())
    return template


def _diff_between_most_and_least_common_characters(
    template: Union[PolymerTemplate, Counter]
) -> int:
    if isinstance(template, PolymerTemplate):
        counts = Counter(list(template))
    else:
        counts = template.copy()
    return max(counts.values()) - min(counts.values())


def _strip_new_add(template: PolymerTemplate) -> PolymerTemplate:
    return template[1:][:-1]


def _perferate_rule_insertion(rule: PairInsertionRule) -> PairInsertionRule:
    _add = ":".join(list(rule.add))
    return PairInsertionRule(pair=rule.pair, add=_add)


def apply_rules_to_rules(
    rules: list[PairInsertionRule], n: int
) -> list[PairInsertionRule]:
    """Apply the insertion rules to the rules themselves.

    This was another algorithm that I tried that i was quite pleased with. It works, but
    isn't any faster or more efficient than the first.

    Args:
        rules (list[PairInsertionRule]): Insertion rules.
        n (int): Iterations.

    Returns:
        list[PairInsertionRule]: New insertion rules.
    """
    mod_rules = [PairInsertionRule(pair=r.pair, add=r.pair) for r in rules]
    for _ in range(n):
        for mod_rule in mod_rules:
            mod_rule.add = apply_rules(mod_rule.add, rules=rules)
    new_rules = [
        PairInsertionRule(pair=r.pair, add=_strip_new_add(r.add)) for r in mod_rules
    ]
    new_rules = [_perferate_rule_insertion(r) for r in new_rules]
    return new_rules


def _rules_to_lookup_dict(rules: list[PairInsertionRule]) -> dict[str, str]:
    return {r.pair: r.add for r in rules}


def polymerize(
    template: PolymerTemplate, rules: list[PairInsertionRule], iterations: int
) -> Counter:
    """Counter-based algorithm for the polymerization puzzle.

    Attribution: GitHub account "kresimir-lukin".
    https://github.com/kresimir-lukin/AdventOfCode2021/blob/main/day14.py

    Args:
        template (PolymerTemplate): Initial polymer template.
        rules (list[PairInsertionRule]): Pair insertion rules.
        iterations (int): Number of iterations.

    Returns:
        Counter: Counter of frequency of each charater.
    """
    rules_dict = _rules_to_lookup_dict(rules)

    pair_frequencies: Counter[str] = Counter()
    char_frequencies = Counter(list(template))

    for i in range(len(template) - 1):
        pair = template[i : (i + 2)]
        pair_frequencies[pair] += 1

    for _ in range(iterations):
        new_pair_freq: Counter[str] = Counter()
        for pair, freq in pair_frequencies.items():
            if (new_char := rules_dict.get(pair)) is not None:
                new_pair_freq[pair[0] + new_char] += freq
                new_pair_freq[new_char + pair[1]] += freq
                char_frequencies[new_char] += freq
        pair_frequencies = new_pair_freq

    return char_frequencies


def main() -> None:
    """Run code for 'Day 14: Extended Polymerization'."""
    # Part 1.
    # Example.
    ex_template, ex_rules = parse_polymer_data(_example_poylmer_data)
    check_example(16, len(ex_rules))
    ex_template_mod = apply_rules(ex_template, ex_rules)
    check_example("NCNBCHB", ex_template_mod)
    check_example("NBCCNBBBCBHCB", apply_rules_n(ex_template, ex_rules, 2))
    check_example("NBBBCNCCNBBNBNBBCHBHHBCHB", apply_rules_n(ex_template, ex_rules, 3))
    check_example(97, len(apply_rules_n(ex_template, ex_rules, 5)))
    ex_res_10 = apply_rules_n(ex_template, ex_rules, 10)
    check_example(3073, len(ex_res_10))
    check_example(1588, _diff_between_most_and_least_common_characters(ex_res_10))
    # Real.
    template, rules = parse_polymer_data(read_data(day=PUZZLE_INFO.day))
    template_10 = apply_rules_n(template, rules, 10)
    answer = _diff_between_most_and_least_common_characters(template_10)
    print_single_answer(day=PUZZLE_INFO.day, part=1, value=answer)
    check_answer(2874, answer, day=PUZZLE_INFO.day, part=1)

    # Part 2.
    # Example with method for building up rules.
    ex_new_rules = apply_rules_to_rules(ex_rules.copy(), 3)
    ex_res_3 = apply_rules(ex_template, ex_new_rules)
    check_example("NBBBCNCCNBBNBNBBCHBHHBCHB", ex_res_3)
    # Example with counters.
    res_10 = _diff_between_most_and_least_common_characters(
        polymerize(template, rules, 10)
    )
    check_example(answer, res_10)
    # Real
    answer_40 = _diff_between_most_and_least_common_characters(
        polymerize(template, rules, 40)
    )
    print_single_answer(day=PUZZLE_INFO.day, part=2, value=answer_40)
    check_answer(5208377027195, answer_40, PUZZLE_INFO.day, 2)
    return None


if __name__ == "__main__":
    main()
