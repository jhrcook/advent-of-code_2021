"""Day 10: Syntax Scoring."""

from typing import Final, Optional, TypeVar

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path

DAY: Final[int] = 10
NAME: Final[str] = "Syntax Scoring"

_T = TypeVar("_T")

OPENERS: Final[set[str]] = {"(", "[", "{", "<"}
CLOSERS: Final[set[str]] = {")", "]", "}", ">"}
CHUNK_PAIRS: Final[dict[str, str]] = {"(": ")", "[": "]", "{": "}", "<": ">"}
ILLEGAL_TOKEN_VALUE: Final[dict[str, int]] = {")": 3, "]": 57, "}": 1197, ">": 25137}
COMPLETION_TOKEN_VALUE: Final[dict[str, int]] = {")": 1, "]": 2, "}": 3, ">": 4}


class CorruptedSubsystemCodeError(BaseException):
    """Corrupted subsystem code error."""

    def __init__(self, corrupt_token: str) -> None:
        """Corrupted subsystem code error.

        Args:
            corrupt_token (str): Token that caused the corruption.
        """
        self.corrupt_token = corrupt_token
        self.msg = f"corrupt token: {corrupt_token}"
        return super().__init__(self.msg)


def _get_example_subsytem_code() -> str:
    return """
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}
    [[<[([]))<([[{}[[()]]]
    [{[{({}]{}}([{[{{{}}([]
    {<[[]]>}<{[{[{[]{()[[[]
    [<(<(<(<{}))><([]([]()
    <{([([[(<>()){}]>(<<{{
    <{([{{}}[<[[[<>{}]]]>[]]
    """


def _parse_subsystem_code_string(code_str: str) -> list[str]:
    return [c.strip() for c in code_str.strip().splitlines()]


def _get_subsystem_code() -> list[str]:
    with open(get_data_path(DAY), "r") as file:
        code = "\n".join([line.strip() for line in file])
    return _parse_subsystem_code_string(code)


# ---- Part 1 ----


def match(open_token: str, close_token: str) -> bool:
    """Whether the two tokens match.

    Args:
        open_token (str): Opening character.
        close_token (str): Closing character.

    Returns:
        bool: Do two tokens match?
    """
    res = CHUNK_PAIRS[open_token] == close_token
    return res


def parse_subsystem_code(code: list[str], openers: list[str]) -> None:
    """Parse the subsystem code looking for corruptions.

    Args:
        code (list[str]): List of characters consistuting the line of code.
        openers (list[str]): Collection of opening tokens. When using this function,
        just pass an empty list.

    Raises:
        CorruptedSubsystemCodeError: If a token is found that indicates the line of code
        is corrupt.
    """
    token = code.pop(0)
    if token in OPENERS:
        openers.append(token)
    else:
        last_opener = openers.pop()
        if not match(last_opener, token):
            raise CorruptedSubsystemCodeError(corrupt_token=token)

    if len(code) == 0:
        return None
    else:
        parse_subsystem_code(code, openers)


def find_corrupted_code(code: str) -> Optional[str]:
    """If the line of code is corrupt, find the corrupting token.

    Args:
        code (str): Line of code (as a string).

    Raises:
        BaseException: If an unexpected error is found.

    Returns:
        Optional[str]: If the line of code is corrupted, the corrupting token is
        returned.
    """
    try:
        parse_subsystem_code(code=list(code), openers=[])
    except CorruptedSubsystemCodeError as err:
        return err.corrupt_token
    except BaseException as err:
        raise err
    return None


def _filter_none(data: list[Optional[_T]]) -> list[_T]:
    return [t for t in data if t is not None]


def corrupt_token_scores(tokens: list[str]) -> int:
    """Calculate the total score for a collection of corrupted tokens.

    Calculates the answer for Part 1.

    Args:
        tokens (list[str]): Collection of corrupting tokens.

    Returns:
        int: Final score.
    """
    return sum([ILLEGAL_TOKEN_VALUE[t] for t in tokens])


def find_and_score_corrupt_lines(codes: list[str]) -> int:
    """Find all of the corrupting tokens for a collection of code and return the score.

    Args:
        codes (list[str]): List of lines of code.

    Returns:
        int: Final score for Part 1.
    """
    return corrupt_token_scores(_filter_none([find_corrupted_code(c) for c in codes]))


# ---- Part 2 ----


def filter_incomplete_code(codes: list[str]) -> list[str]:
    """Filter code for only the incomplete lines.

    Since all lines of code are incorrect, this just filters the corrupted lines.

    Args:
        codes (list[str]): Lines of code as strings.

    Returns:
        list[str]: Collection of incomplete code.
    """
    incomplete_code: list[str] = []
    for code in codes:
        if find_corrupted_code(code) is None:
            incomplete_code.append(code)
    return incomplete_code


def find_end_of_incomplete_code(
    code: list[str], new_code: list[str], closers: list[str]
) -> list[str]:
    """Get the end to incomplete code.

    Args:
        code (list[str]): Code as a list of characters (tokens).
        new_code (list[str]): Newly generated code. Start with an empty list.
        closers (list[str]): Collection of closers found during by the algorithm. Start
        with an empty list.

    Returns:
        list[str]: Collection of tokens that complete the code.
    """
    token = code.pop()
    if token in CLOSERS:
        closers.append(token)
    else:
        if len(closers) > 0:
            _ = closers.pop()
        else:
            new_code.append(CHUNK_PAIRS[token])

    if len(code) > 0:
        find_end_of_incomplete_code(code=code, new_code=new_code, closers=closers)

    return new_code


def autocomplete(code: str) -> str:
    """Autocomplete a line of code.

    Args:
        code (str): Code as a single string represneting a collection of tokens.

    Returns:
        str: Autocompleted code.
    """
    end = "".join(find_end_of_incomplete_code(list(code), [], []))
    return code + end


def calc_completion_score(oringal_code: str, complete_code: str) -> int:
    """Calculate the score for completed code.

    Args:
        oringal_code (str): Original line of code.
        complete_code (str): Autocompleted line of code.

    Returns:
        int: Score for Part 2.
    """
    added_code = complete_code[len(oringal_code) :]
    score = 0
    for token in added_code:
        score = score * 5 + COMPLETION_TOKEN_VALUE[token]
    return score


def _find_middle_completion_score(completed_code: dict[str, str]) -> int:
    """Go through the steps to get the single numeric answer for Part 2."""
    completion_scores = [calc_completion_score(a, b) for a, b in completed_code.items()]
    completion_scores.sort()
    mid_completion_score = completion_scores[len(completion_scores) // 2]
    return mid_completion_score


def main() -> None:
    """Run code for 'Day 10: Syntax Scoring'."""
    # Part 1
    # Examples
    ex_corrupt_token = find_corrupted_code("{()()()>")
    check_example(ex_corrupt_token, ">")
    ex_code = _parse_subsystem_code_string(_get_example_subsytem_code())
    ex_corrupt_tokens = _filter_none([find_corrupted_code(c) for c in ex_code])
    [check_example(a, b) for a, b in zip(["}", ")", "]", ")", ">"], ex_corrupt_tokens)]
    ex_score = corrupt_token_scores(ex_corrupt_tokens)
    check_example(26397, ex_score)
    check_example(26397, find_and_score_corrupt_lines(ex_code))
    # Real
    subsystem_code = _get_subsystem_code()
    corrupt_score = find_and_score_corrupt_lines(subsystem_code)
    print_single_answer(DAY, 1, corrupt_score)
    check_answer(193275, corrupt_score, DAY, 1)

    # Part 2.
    # Example 1.
    ex_code = _parse_subsystem_code_string(_get_example_subsytem_code())
    ex_incomplete_codes = filter_incomplete_code(ex_code)
    check_example(5, len(ex_incomplete_codes))
    # Example 2.
    ex_incomplete_code = "<{([{{}}[<[[[<>{}]]]>[]]"
    ex_solution = "<{([{{}}[<[[[<>{}]]]>[]]])}>"
    check_example(294, calc_completion_score(ex_incomplete_code, ex_solution))
    ex_autocomplete = autocomplete(ex_incomplete_code)
    check_example(ex_solution, ex_autocomplete)
    # Real
    subsystem_code = filter_incomplete_code(_get_subsystem_code())
    autocompleted_code = {code: autocomplete(code) for code in subsystem_code}
    middle_completion_score = _find_middle_completion_score(autocompleted_code)
    print_single_answer(DAY, 2, middle_completion_score)
    check_answer(2429644557, middle_completion_score, DAY, 2)
    return None


if __name__ == "__main__":
    main()
