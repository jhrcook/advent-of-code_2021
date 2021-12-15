"""Day 14: Extended Polymerization."""

from typing import Counter

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import DayInfo

PUZZLE_INFO = DayInfo(day=14, title="Extended Polymerization")

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
            pair (str): PAir of characters to search for.
            add (str): Character to insert between the pair.
        """
        assert len(pair) == 2
        assert len(add) == 1
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
    verbose: bool = False,
) -> PolymerTemplate:
    """Apply the polymerization insertion rules to a template repeatedly.

    Args:
        template (PolymerTemplate): Initial template.
        rules (list[PairInsertionRule]): Polymerization insertion rules.
        n (int): Number of repeats.
        verbose (bool, optional): Run verbosely. Defaults to False.

    Returns:
        PolymerTemplate: Final polymer.
    """
    if verbose:
        print(f"starting template: {template}")
    for i in range(n):
        template = apply_rules(template=template, rules=rules.copy())
        if verbose:
            print(f"iteration {i}: {template}")
    if verbose:
        print(f"final template: {template}")
    return template


def _diff_between_most_and_least_common_characters(template: PolymerTemplate) -> int:
    counts = Counter(list(template))
    return max(counts.values()) - min(counts.values())


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
    # Examples.
    # tic = time()
    # ex_res_40 = apply_rules_n(ex_template, ex_rules, 23)
    # toc = time()
    # print(f"timer: {toc-tic:0.3f}")
    # check_example(
    #     2188189693529, _diff_between_most_and_least_common_characters(ex_res_40)
    # )
    return None


if __name__ == "__main__":
    main()
