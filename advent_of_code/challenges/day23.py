"""Day 23: Amphipod."""

from __future__ import annotations

from copy import copy, deepcopy
from dataclasses import dataclass
from enum import Enum
from functools import cache
from itertools import product
from typing import Any, Final, Optional, Union

# from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=23, title="Amphipod")

_example_puzzle_input = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

_example_finished = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""


N_ROOMS: Final[int] = 4
ROOM_LEN: int = 2
HALLWAY_LEN: Final[int] = 11
ROOM_TO_HALLWAY: Final[dict[int, int]] = {0: 2, 1: 4, 2: 6, 3: 8}


class AmphipodType(Enum):

    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Amphipod:

    atype: AmphipodType

    def __init__(self, atype: Union[str, AmphipodType]) -> None:
        if isinstance(atype, str):
            atype = AmphipodType(atype)
        self.atype = atype
        return None

    def __str__(self) -> str:
        return self.atype.value

    def __repr__(self) -> str:
        return str(self)

    def __copy__(self) -> Amphipod:
        return Amphipod(self.atype)


# index 0: bottom
# index 1: top
AmphipodRoom = list[Optional[Amphipod]]


class AmphipodBurrow:

    rooms: tuple[AmphipodRoom, AmphipodRoom, AmphipodRoom, AmphipodRoom]
    hallway: list[Optional[Amphipod]]
    _room_len: int

    def __init__(
        self,
        A: AmphipodRoom,
        B: AmphipodRoom,
        C: AmphipodRoom,
        D: AmphipodRoom,
        hallway: Optional[list[Optional[Amphipod]]] = None,
        room_len: int = 2,
    ) -> None:
        self._room_len = room_len
        # for x in (A, B, C, D):
        #     assert len(x) == room_len
        self.rooms = (A, B, C, D)

        if hallway is not None:
            self.hallway = hallway
        else:
            self.hallway = [None] * 11
        return None

    def __str__(self) -> str:
        out = "".join(
            [str(x) if isinstance(x, Amphipod) else "." for x in self.hallway]
        )
        out += "\n"
        for i in reversed(range(self._room_len)):
            row = "  "
            for room in self.rooms:
                apod = room[i]
                row += apod.atype.value if apod is not None else "."
                row += " "
            out += row + "\n"
        return out

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, a: Any) -> bool:
        return str(self) == str(a)

    def __copy__(self) -> AmphipodBurrow:
        a, b, c, d = (deepcopy(x) for x in self.rooms)
        return AmphipodBurrow(
            A=a, B=b, C=c, D=d, hallway=deepcopy(self.hallway), room_len=self._room_len
        )

    @property
    def is_complete(self) -> bool:
        if not all([x is None for x in self.hallway]):
            return False
        for atype, aroom in zip(AmphipodType, self.rooms):
            if not all([a is not None and a.atype is atype for a in aroom]):
                return False
        return True


def _amphipod_list(*args: str) -> AmphipodRoom:
    return [None if a == "." else Amphipod(a) for a in args]


# D#C#B#A#
# D#B#A#C#
PART2_ADDITIONS: Final[list[tuple[str, str]]] = [
    ("D", "D"),
    ("C", "B"),
    ("B", "A"),
    ("A", "C"),
]


def _convert_for_part2(aburrow: AmphipodBurrow) -> None:
    aburrow._room_len = 4
    for room_i, atypes in enumerate(PART2_ADDITIONS):
        for atype in atypes:
            aburrow.rooms[room_i].insert(1, Amphipod(atype))
    return None


def parse_puzzle_input(data: str, part: int) -> AmphipodBurrow:
    data_list = data.strip().splitlines()
    hallway = [
        None if x == "." else Amphipod(x) for x in data_list[1].strip().replace("#", "")
    ]
    row1 = list(data_list[2].strip().replace("#", ""))
    row2 = list(data_list[3].strip().replace("#", ""))
    A = _amphipod_list(row2[0], row1[0])
    B = _amphipod_list(row2[1], row1[1])
    C = _amphipod_list(row2[2], row1[2])
    D = _amphipod_list(row2[3], row1[3])
    apod = AmphipodBurrow(A, B, C, D, hallway=hallway)
    if part == 2:
        _convert_for_part2(apod)
    return apod


def _get_example_puzzle(part: int = 1) -> AmphipodBurrow:
    return parse_puzzle_input(_example_puzzle_input, part)


def _get_example_finished_puzzle(part: int = 1) -> AmphipodBurrow:
    return parse_puzzle_input(_example_finished, part)


def _get_puzzle_input(part: int = 1) -> AmphipodBurrow:
    return parse_puzzle_input(read_data(PI.day), part)


@dataclass
class MoveResult:

    aburrow: AmphipodBurrow
    score: int


@cache
def _move_distance(room_i: int, room_pos: int, hallway_i: int) -> int:
    x = abs(hallway_i - (2 * (1 + room_i)))
    x += ROOM_LEN - room_pos
    return x


AMPHIPOD_ENERGY: Final[dict[AmphipodType, int]] = {
    AmphipodType.A: 1,
    AmphipodType.B: 10,
    AmphipodType.C: 100,
    AmphipodType.D: 1000,
}

AMPHIPOD_DEST_ROOM: Final[dict[AmphipodType, int]] = {
    AmphipodType.A: 0,
    AmphipodType.B: 1,
    AmphipodType.C: 2,
    AmphipodType.D: 3,
}


def _can_reach_hallway_position_from_room(
    aburrow: AmphipodBurrow, room_i: int, hallway_pos: int
) -> bool:
    start = ROOM_TO_HALLWAY[room_i]
    if hallway_pos == start:
        return False
    elif hallway_pos < start:
        return all([a is None for a in aburrow.hallway[hallway_pos : (start + 1)]])
    else:
        end = min(HALLWAY_LEN, hallway_pos + 1)
        return all([a is None for a in aburrow.hallway[start:end]])


def _can_reach_room_from_hallway_pos(
    aburrow: AmphipodBurrow, room_i: int, hallway_pos: int
) -> bool:
    end = ROOM_TO_HALLWAY[room_i]
    if end == hallway_pos:
        return True
    if end < hallway_pos:
        return all([a is None for a in aburrow.hallway[end:hallway_pos]])
    else:
        start = hallway_pos + 1
        end += 1
        return all([a is None for a in aburrow.hallway[start:end]])


def _apod_is_in_destination(apod: Amphipod, room: AmphipodRoom, room_i: int) -> bool:
    if room_i != AMPHIPOD_DEST_ROOM[apod.atype]:  # in wrong room number
        return False
    idx = room.index(apod)
    for neighbor in room[0:idx]:  # check all below are same type
        assert neighbor is not None
        if neighbor.atype != apod.atype:
            return False
    return True


def pop_top_to_hallway(
    aburrow: AmphipodBurrow,
    room_i: int,
    hallway_pos: int,
    allow_atop_room: bool = False,
) -> int:
    if not allow_atop_room and hallway_pos in {2, 4, 6, 8}:
        return 0
    if aburrow.hallway[hallway_pos] is not None:
        # Position in hallway is taken.
        return 0
    aroom = aburrow.rooms[room_i]
    if all([a is None for a in aroom]):
        # No amphipods in the room.
        return 0
    if not _can_reach_hallway_position_from_room(aburrow, room_i, hallway_pos):
        return 0
    score: int = 0
    for i in reversed(range(ROOM_LEN)):
        if (apod := aroom[i]) is not None:
            if _apod_is_in_destination(apod, aroom, room_i=room_i):
                return 0
            aburrow.hallway[hallway_pos] = apod
            aroom[i] = None
            score = _move_distance(room_i, i, hallway_pos) * AMPHIPOD_ENERGY[apod.atype]
            return score
    print(aburrow)
    raise BaseException("Unforeseen possibility of moving amphipod.")


def _which_space_in_room(dest_room: AmphipodRoom) -> Optional[int]:
    for i, apod in enumerate(dest_room):
        if apod is None:
            return i
    return None


def _room_is_all_correct_type_or_none(atype: AmphipodType, aroom: AmphipodRoom) -> bool:
    for apod in aroom:
        if apod is not None and apod.atype != atype:
            return False
    return True


def try_moving_rooms(aburrow: AmphipodBurrow, room_i: int) -> int:
    """Try moving each amphipod from a room to another and return the energy."""
    for room_pos in (1, 0):
        if (apod := aburrow.rooms[room_i][room_pos]) is not None:
            room_dest_i = AMPHIPOD_DEST_ROOM[apod.atype]
            if not _room_is_all_correct_type_or_none(
                apod.atype, aburrow.rooms[room_dest_i]
            ):
                return 0
            room_dest_pos = _which_space_in_room(aburrow.rooms[room_dest_i])
            if room_dest_pos is None:
                # No space in destination room.
                return 0
            hallway_pos = ROOM_TO_HALLWAY[room_dest_i]
            score = pop_top_to_hallway(
                aburrow, room_i=room_i, hallway_pos=hallway_pos, allow_atop_room=True
            )
            if score == 0:
                # Unable to move apod to above its destination.
                return 0
            score += try_moving_from_hallway_to_room(aburrow, hallway_pos)
            return score
    # No amphipods to move.
    return 0


def try_moving_from_hallway_to_room(aburrow: AmphipodBurrow, hallway_pos: int) -> int:
    """Try moving an amphipod from the hallway to a room and return the energy."""
    if (apod := aburrow.hallway[hallway_pos]) is None:
        return 0
    dest_room_i = AMPHIPOD_DEST_ROOM[apod.atype]
    dest_room_pos = _which_space_in_room(aburrow.rooms[dest_room_i])
    if dest_room_pos is None:
        return 0
    if not _room_is_all_correct_type_or_none(apod.atype, aburrow.rooms[dest_room_i]):
        return 0
    if not _can_reach_room_from_hallway_pos(
        aburrow, room_i=dest_room_i, hallway_pos=hallway_pos
    ):
        return 0
    aburrow.hallway[hallway_pos] = None
    aburrow.rooms[dest_room_i][dest_room_pos] = apod
    n_moves = _move_distance(
        room_i=dest_room_i, room_pos=dest_room_pos, hallway_i=hallway_pos
    )
    return n_moves * AMPHIPOD_ENERGY[apod.atype]


def move_amphipods_to_destination(aburrow: AmphipodBurrow) -> int:
    _prev_burrow: str = ""
    score = 0
    while _prev_burrow != str(aburrow):
        _prev_burrow = str(aburrow)
        for hallway_pos in range(HALLWAY_LEN):
            score += try_moving_from_hallway_to_room(aburrow, hallway_pos)
        for room_i in range(N_ROOMS):
            score += try_moving_rooms(aburrow, room_i)
    return score


def _empty_hallway_positions(aburrow: AmphipodBurrow) -> list[int]:
    return [
        i
        for i, x in enumerate(aburrow.hallway)
        if x is None and x not in ROOM_TO_HALLWAY.values()
    ]


def make_all_moves(aburrow: AmphipodBurrow, scores: list[int], score: int = 0) -> None:
    if aburrow.is_complete:
        return None
    for room, hallway_pos in product(range(N_ROOMS), _empty_hallway_positions(aburrow)):
        copy_aburrow = copy(aburrow)
        res = pop_top_to_hallway(copy_aburrow, room, hallway_pos)
        res += move_amphipods_to_destination(copy_aburrow)
        # print(copy_aburrow)
        # continue
        if res == 0:
            continue
        new_score = score + res
        if len(scores) > 0 and min(scores) <= new_score:
            # End early if a faster solution has been found.
            return
        if copy_aburrow.is_complete:
            scores.append(new_score)
            print(f"completion score: {new_score}")
            return
        else:
            make_all_moves(aburrow=copy_aburrow, scores=scores, score=new_score)
    return None


def find_lowest_rearrange_score(aburrow: AmphipodBurrow) -> int:
    scores: list[int] = []
    make_all_moves(aburrow, scores)
    return min(scores)


def main() -> None:
    """Run code for 'Day 23: Amphipod'."""
    # Part 1.
    # Example.
    # ex_burrow = _get_example_puzzle()
    # print("Starting configuration:")
    # print(ex_burrow)
    # print("-" * 80)
    # ex_scores: list[int] = []
    # make_all_moves(ex_burrow, ex_scores)
    # print(f"number of scores: {len(ex_scores)}")
    # print(f"min score: {min(ex_scores)}")
    # check_example(12521, min(ex_scores))

    # Real.
    # burrow = _get_puzzle_input()
    # scores: list[int] = []
    # make_all_moves(burrow, scores)
    # print_single_answer(PI.day, 1, min(scores))
    # check_answer(15472, min(scores), day=PI.day, part=1)

    # Part 2.
    # Examples.
    global ROOM_LEN
    ROOM_LEN = 4
    # ex_burrow = _get_example_puzzle(part=2)
    # print("Starting configuration:")
    # print(ex_burrow)
    # print("-" * 80)
    # ex_scores: list[int] = []
    # make_all_moves(ex_burrow, ex_scores)
    # print(f"number of scores: {len(ex_scores)}")
    # print(f"min score: {min(ex_scores)}")
    # check_example(12521, min(ex_scores))

    # Real.
    burrow = _get_puzzle_input(part=2)
    print(burrow)
    scores: list[int] = []
    make_all_moves(burrow, scores)
    print(f"number of scores: {len(scores)}")
    min_score = min(scores)
    print(f"min score: {min_score}")
    print_single_answer(PI.day, 2, min_score)
    # check_answer(15472, min_score, day=PI.day, part=1)
    # 46444 too high

    return None


if __name__ == "__main__":
    main()
