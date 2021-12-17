"""Day 15: Chiton."""

from itertools import product

import networkx as nx
import numpy as np

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=15, title="Chiton")

_ex_cave_data = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def cave_data_to_numpy(data: str) -> np.ndarray:
    """Cave map data string to a numpy array.

    Args:
        data (str): Cave map as a string.

    Returns:
        np.ndarray: Cave map as an array.
    """
    rows = []
    for line in data.strip().splitlines():
        rows.append([int(x) for x in line.strip()])
    return np.array(rows, dtype=int)


def _get_example_cave_data() -> np.ndarray:
    return cave_data_to_numpy(_ex_cave_data)


def _get_puzzle_data() -> np.ndarray:
    return cave_data_to_numpy(read_data(PI.day))


def _loc_to_node_name(a: int, b: int) -> str:
    return f"{a},{b}"


def iter_around_point(
    pt: tuple[int, int], dims: tuple[int, int]
) -> list[tuple[int, int]]:
    """Iterate over the neighbors of a point in an array.

    Args:
        pt (tuple[int, int]): Point to get neighbors for.
        dims (tuple[int, int]): Dimensions of the array.

    Returns:
        list[tuple[int, int]]: [description]
    """
    neighbors: list[tuple[int, int]] = []
    i, j = pt
    if i > 0:
        neighbors.append((i - 1, j))
    if j > 0:
        neighbors.append((i, j - 1))
    if i < (dims[0] - 1):
        neighbors.append((i + 1, j))
    if j < (dims[1] - 1):
        neighbors.append((i, j + 1))
    return neighbors


def cave_to_network(cave: np.ndarray) -> tuple[nx.Graph, str]:
    """Make a network from a cave map.

    Args:
        cave (np.ndarray): Cave map.

    Returns:
        tuple[nx.Graph, str]: Network of the cave system.
    """
    dims = cave.shape
    tree = nx.DiGraph()
    for i, j in product(range(dims[0]), range(dims[1])):
        node = _loc_to_node_name(i, j)
        for a, b in iter_around_point((i, j), dims=dims):
            to = _loc_to_node_name(a, b)
            weight = cave[a, b]
            tree.add_weighted_edges_from([(node, to, weight)])

    target = _loc_to_node_name(dims[0] - 1, dims[1] - 1)
    return tree, target


def _total_edge_weights(path: list[str], tree: nx.Graph) -> int:
    total_weight = 0
    for i in range(len(path) - 1):
        total_weight += tree.get_edge_data(path[i], path[i + 1])["weight"]
    return total_weight


def shortest_path_weight(gr: nx.Graph, source: str, target: str) -> int:
    """Get the total weight of the shortest path in a graph.

    Args:
        gr (nx.Graph): Weighted, directed graph.
        source (str): Source node.
        target (str): Target node.

    Returns:
        int: Total path weight.
    """
    path: list[str] = nx.shortest_path(
        gr, source=source, target=target, weight="weight"
    )
    return _total_edge_weights(path, gr)


def _add_block_to_right(
    ary: np.ndarray, block: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    new_block = block.copy() + 1
    new_block[new_block > 9] = 1
    ary = np.hstack([ary.copy(), new_block])
    return ary, new_block


def build_out_full_map(cave_map: np.ndarray, n: int = 5) -> np.ndarray:
    """Build out the "full" cave map for part 2 of the puzzle.

    Args:
        cave_map (np.ndarray): Original cave map.
        n (int, optional): Number of iterations in each dimension. Defaults to 5.

    Returns:
        np.ndarray: Larger array.
    """
    extended_cave_map = cave_map.copy()
    block = cave_map.copy()
    for _ in range(n - 1):
        extended_cave_map, block = _add_block_to_right(extended_cave_map, block)

    extended_cave_map = np.rot90(extended_cave_map)
    block = extended_cave_map.copy()
    for _ in range(n - 1):
        extended_cave_map, block = _add_block_to_right(extended_cave_map, block)

    extended_cave_map = np.rot90(extended_cave_map, k=3)
    return extended_cave_map


def main() -> None:
    """Run code for 'Day 15: Chiton'."""
    # Part 1.
    # Example.
    ex_cave_graph, ex_target = cave_to_network(_get_example_cave_data())
    ex_weight = shortest_path_weight(ex_cave_graph, "0,0", ex_target)
    check_example(40, ex_weight)
    # Real
    cave_tree, target = cave_to_network(_get_puzzle_data())
    shortest_path = shortest_path_weight(cave_tree, "0,0", target)
    print_single_answer(PI.day, 1, shortest_path)
    check_answer(707, shortest_path, day=PI.day, part=1)

    # Example.
    ex_large_cave_map = build_out_full_map(_get_example_cave_data(), 5)
    ex_cave_graph, ex_target = cave_to_network(ex_large_cave_map)
    ex_weight = shortest_path_weight(ex_cave_graph, "0,0", ex_target)
    check_example(315, ex_weight)
    # Real
    cave_tree, target = cave_to_network(build_out_full_map(_get_puzzle_data()))
    shortest_path = shortest_path_weight(cave_tree, "0,0", target)
    print_single_answer(PI.day, 2, shortest_path)
    check_answer(2942, shortest_path, day=PI.day, part=2)
    return None


if __name__ == "__main__":
    main()
