"""Day 12: Passage Pathing."""

from __future__ import annotations

from collections import Counter
from enum import Enum
from typing import Final

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import get_data_path
from advent_of_code.utils import assert_never

DAY: Final[int] = 12
NAME: Final[str] = "Passage Pathing"

BAD_END = "🙁"


Cave = str
Neighbors = set[str]
CaveConnections = dict[Cave, Neighbors]
Path = list[str]


def _get_small_example_data() -> str:
    return """
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
    """.strip()


def _get_large_example_data() -> str:
    return """
    fs-end
    he-DX
    fs-he
    start-DX
    pj-DX
    end-zg
    zg-sl
    zg-pj
    pj-he
    RW-he
    fs-DX
    pj-RW
    zg-RW
    start-pj
    he-WI
    zg-he
    pj-fs
    start-RW
    """.strip()


def _get_data() -> str:
    data = ""
    with open(get_data_path(DAY), "r") as file:
        for line in file:
            data += line.strip() + "\n"
    return data


def _add_cave_to_paths(
    cave: Cave, neighbor: Cave, connections: CaveConnections
) -> None:
    cave = cave.strip()
    p = connections.get(cave, set())
    p.add(neighbor)
    connections[cave] = p
    return None


def _parse_cave_data(cave_data_str: str) -> CaveConnections:
    caves: CaveConnections = {}
    for path in cave_data_str.strip().splitlines():
        a, b = path.strip().split("-")
        _add_cave_to_paths(a, b, caves)
        _add_cave_to_paths(b, a, caves)
    return caves


def remove_already_visited(neighbors: Neighbors, path: Path) -> Neighbors:
    """Remove the 'small' caves from a set of neighbors that are already in the path.

    This is the triming method for part 1 of the puzzle.

    Args:
        neighbors (Neighbors): A set of neighboring caves.
        path (Path): Current path.

    Returns:
        Neighbors: Trimmed set of neighbors.
    """
    _neighbors = neighbors.copy()
    for neighbor in neighbors:
        if neighbor.isupper():
            continue
        if neighbor in path:
            _neighbors.remove(neighbor)
    return _neighbors


def _any_duplicate_smalls(path: Path) -> bool:
    path_counts = Counter(
        [cave for cave in path if cave not in {"start", "end"} and cave.islower()]
    )
    return any([c > 1 for c in path_counts.values()])


def remove_already_visited_twice(neighbors: Neighbors, path: Path) -> Neighbors:
    """Remove the 'small' caves if any small cave has already been visited twice.

    This is the triming method for part 2 of the puzzle.

    Args:
        neighbors (Neighbors): Set of neighboring caves.
        path (Path): Current path.

    Returns:
        Neighbors: Trimmed set of neighbors.
    """
    _neighbors = neighbors.copy()

    if "start" in neighbors and "start" in path:
        _neighbors.remove("start")

    if not _any_duplicate_smalls(path):
        return _neighbors
    else:
        return remove_already_visited(neighbors=_neighbors, path=path)


class SearchMode(Enum):
    """Available search modes (for parts 1 and 2 of the challenge)."""

    ONCE = "ONCE"
    TWICE = "TWICE"


def path_search(
    caves: CaveConnections,
    path: Path,
    all_paths: list[Path],
    mode: SearchMode,
    start: str = "start",
    end: str = "end",
) -> None:
    """Search a network of caves for a path from `start` to `end`.

    Algorithm:
    1. get all of the neighbors for the current cave (`start`)
    2. trim the available neighbors (per `mode`)
    3. if there are no neighbors, cap the path with a sad face and add the path to the
       list
    4. otherwise, for each neighboring cave,
        a. if the neighbor is the end, cap the path and add it to the list
        b. else add the cave to a copy of the current path and recurse

    Args:
        caves (CaveConnections): Network of caves.
        path (Path): Current path.
        all_paths (list[Path]): A collection of all paths.
        mode (SearchMode): Mode of path finding.
        start (str, optional): Start cave. Defaults to "start".
        end (str, optional): End cave. Defaults to "end".
    """
    neighbors = caves[start].copy()

    if mode is SearchMode.ONCE:
        neighbors = remove_already_visited(neighbors=neighbors, path=path)
    elif mode is SearchMode.TWICE:
        neighbors = remove_already_visited_twice(neighbors=neighbors, path=path)
    else:
        assert_never(mode)

    if len(neighbors) == 0:
        new_path = path.copy() + [BAD_END]
        all_paths.append(new_path)
    else:
        for n in neighbors:
            if n == end:
                new_path = path.copy() + [n]
                all_paths.append(new_path)
            else:
                new_path = path.copy() + [n]
                path_search(
                    caves=caves, path=new_path, all_paths=all_paths, mode=mode, start=n
                )
    return


def _filter_out_bad_paths(paths: list[Path]) -> list[Path]:
    return [p for p in paths if BAD_END not in p]


def number_paths(caves: CaveConnections, mode: SearchMode) -> int:
    """Count the number of paths in a network of caves.

    Args:
        caves (CaveConnections): Network of caves.
        mode (SearchMode): Mode of path finding.

    Returns:
        int: Number of paths.
    """
    all_paths: list[Path] = []
    path_search(
        caves=caves,
        path=["start"],
        all_paths=all_paths,
        mode=mode,
        start="start",
        end="end",
    )
    return len(_filter_out_bad_paths(all_paths))


# ---- Part 2 ----


def main() -> None:
    """Run code for 'Day 12: Passage Pathing'."""
    # Part 1.
    # Examples.
    ex_caves_1 = _parse_cave_data(_get_small_example_data())
    check_example(10, number_paths(ex_caves_1, mode=SearchMode.ONCE))
    ex_caves_2 = _parse_cave_data(_get_large_example_data())
    check_example(226, number_paths(ex_caves_2, mode=SearchMode.ONCE))
    # Real
    caves = _parse_cave_data(_get_data())
    n_paths = number_paths(caves, mode=SearchMode.ONCE)
    print_single_answer(DAY, 1, n_paths)
    check_answer(5254, n_paths, DAY, 1)

    # Part 2.
    # Examples.
    check_example(36, number_paths(ex_caves_1, mode=SearchMode.TWICE))
    check_example(3509, number_paths(ex_caves_2, mode=SearchMode.TWICE))
    # Real
    n_paths = number_paths(caves, mode=SearchMode.TWICE)
    print_single_answer(DAY, 2, n_paths)
    check_answer(149385, n_paths, DAY, 2)
    return None


if __name__ == "__main__":
    main()
