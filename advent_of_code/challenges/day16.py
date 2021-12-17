"""Day 16: Packet Decoder."""
from __future__ import annotations

from typing import Final, Literal, Optional, Union

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=16, title="Packet Decoder")

HEX_TO_BIN: Final[dict[str, str]] = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

_ex_literal_value = "D2FE28"
_ex_operator_mode0 = "38006F45291200"
_ex_operator_mode1 = "EE00D40C823060"


def _parse_hex_to_bin(hex_str: str) -> str:
    return "".join(HEX_TO_BIN[h] for h in hex_str)


def _hex_to_bits(hex_code: str) -> list[str]:
    return list(_parse_hex_to_bin(hex_code))


def _get_puzzle_data() -> str:
    return read_data(day=PI.day).strip()


class LiteralPacket:
    """Literal packet."""

    version: int
    type_id: int
    value: int

    def __init__(self, version: int, type_id: int, value: int) -> None:
        """Create a literal packet.

        Args:
            version (int): Version number.
            type_id (int): Type ID (should always be 4).
            value (int): Value of the packet.
        """
        self.version = version
        assert type_id == 4
        self.type_id = type_id
        self.value = value
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        msg = f"Literal Packet(v{self.version}): type: {self.type_id}"
        msg += " → value: {self.value}"
        return msg

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)


class OperatorPacket:
    """Operator packet."""

    version: int
    type_id: int
    length_type_id: Literal[0, 1]
    subpackets: list[Union[LiteralPacket, OperatorPacket]]

    def __init__(
        self,
        version: int,
        type_id: int,
        length_type_id: int,
        subpackets: list[Union[LiteralPacket, OperatorPacket]],
    ) -> None:
        """Create an operator packet.

        Args:
            version (int): Version number.
            type_id (int): Type ID (should not be 4).
            length_type_id (int): Length type ID (should be either 0 or 1).
            subpackets (list[Union[LiteralPacket, OperatorPacket]]): Operator
            subpackets.
        """
        self.version = version
        assert type_id != 4
        self.type_id = type_id
        assert length_type_id in {0, 1}
        self.length_type_id = length_type_id  # type: ignore
        self.subpackets = subpackets.copy()
        return None

    def __str__(self) -> str:
        """Human-readable representation."""
        msg = f"Operator packet (v{self.version}): type: {self.type_id}, subpackets:\n"
        for p in self.subpackets:
            msg += " - " + str(p) + "\n"
        return msg

    def __repr__(self) -> str:
        """Human-readable representation."""
        return str(self)

    @property
    def value(self) -> int:
        """Get the value of the operator."""
        subpkt_values = [p.value for p in self.subpackets]
        if self.type_id == 0:
            return sum(subpkt_values)
        elif self.type_id == 1:
            val = 1
            for x in subpkt_values:
                val *= x
            return val
        elif self.type_id == 2:
            return min(subpkt_values)
        elif self.type_id == 3:
            return max(subpkt_values)
        elif self.type_id == 5:
            assert len(subpkt_values) == 2
            return int(subpkt_values[0] > subpkt_values[1])
        elif self.type_id == 6:
            assert len(subpkt_values) == 2
            return int(subpkt_values[0] < subpkt_values[1])
        elif self.type_id == 7:
            assert len(subpkt_values) == 2
            return int(subpkt_values[0] == subpkt_values[1])
        else:
            raise BaseException(f"Unexpected operator type ID: {self.type_id}")


def parse_literal_packet_type(
    bin_code: list[str], pkt_version: int, pkt_type_id: int
) -> LiteralPacket:
    """Parse a literal packet type.

    Args:
        bin_code (list[str]): Current bin code object (mutated in place).
        pkt_version (int): Packet version.
        pkt_type_id (int): Packet type ID (should be 4).

    Returns:
        LiteralPacket: Literal packet object.
    """
    groups: list[str] = []
    while True:
        group = "".join([bin_code.pop(0) for i in range(5)])
        groups.append(group)
        if group[0] == "0":
            break
    literal_value = int("".join(([g[1:] for g in groups])), base=2)
    return LiteralPacket(version=pkt_version, type_id=pkt_type_id, value=literal_value)


def _parse_operator_packet_type_mode0(
    bin_code: list[str],
) -> list[Union[LiteralPacket, OperatorPacket]]:
    num_bits = int("".join(bin_code.pop(0) for _ in range(15)), base=2)
    sub_bin_code = [bin_code.pop(0) for _ in range(num_bits)]
    subpackets = parse_bits(sub_bin_code)
    return subpackets


def _parse_operator_packet_type_mode1(
    bin_code: list[str],
) -> list[Union[LiteralPacket, OperatorPacket]]:
    num_subpackets = int("".join(bin_code.pop(0) for _ in range(11)), base=2)
    packets = parse_bits(bin_code, early_stop_at_n=num_subpackets)
    assert len(packets) == num_subpackets
    return packets


def parse_operator_packet_type(
    bin_code: list[str], pkt_version: int, pkt_type_id: int
) -> OperatorPacket:
    """Parse an operator packet type.

    Args:
        bin_code (list[str]): Current bin code object (mutated in place).
        pkt_version (int): Packet version.
        pkt_type_id (int): Packet type ID (should be 4).

    Returns:
        LiteralPacket: Operator packet object.
    """
    length_type_id = int(bin_code.pop(0))
    if length_type_id == 0:
        subpackets = _parse_operator_packet_type_mode0(bin_code)
    else:
        subpackets = _parse_operator_packet_type_mode1(bin_code)
    return OperatorPacket(
        version=pkt_version,
        type_id=pkt_type_id,
        length_type_id=length_type_id,
        subpackets=subpackets,
    )


def parse_bits(
    bin_code: list[str], early_stop_at_n: Optional[int] = None
) -> list[Union[LiteralPacket, OperatorPacket]]:
    """Parse BITS code into Literal and Operator packets.

    Args:
        bin_code (list[str]): Binary code.
        early_stop_at_n (Optional[int], optional): Stop parsing after a certain number
        of packets have been found. This is used for parsing subpackets of one of the
        Operator types. Defaults to None.

    Returns:
        list[Union[LiteralPacket, OperatorPacket]]: Packets
    """
    packets: list[Union[LiteralPacket, OperatorPacket]] = []

    while len(bin_code) > 0 and set(bin_code.copy()) != {"0"}:
        if early_stop_at_n is not None and len(packets) == early_stop_at_n:
            break

        packet_version = int("".join([bin_code.pop(0) for _ in range(3)]), base=2)
        packet_type_id = int("".join([bin_code.pop(0) for _ in range(3)]), base=2)

        if packet_type_id == 4:
            literal_packet = parse_literal_packet_type(
                bin_code, pkt_version=packet_version, pkt_type_id=packet_type_id
            )
            packets.append(literal_packet)
        else:
            op_packet = parse_operator_packet_type(
                bin_code, pkt_version=packet_version, pkt_type_id=packet_type_id
            )
            packets.append(op_packet)

    return packets


def sum_all_version_numbers(packets: list[Union[LiteralPacket, OperatorPacket]]) -> int:
    """Sum of the version numbers of packets.

    Answer for part 1 of the puzzle.
    """
    total = 0
    for packet in packets:
        if isinstance(packet, LiteralPacket):
            total += packet.version
        else:
            total += packet.version
            total += sum_all_version_numbers(packet.subpackets)
    return total


def main() -> None:
    """Run code for 'Day 16: Packet Decoder'."""
    # Part 1.
    # Examples.
    ex_literal = parse_bits(_hex_to_bits(_ex_literal_value))
    check_example(1, len(ex_literal))
    ex_packet = ex_literal[0]
    assert isinstance(ex_packet, LiteralPacket)
    check_example(6, ex_packet.version)
    check_example(4, ex_packet.type_id)
    check_example(2021, ex_packet.value)

    ex_op_m0 = parse_bits(_hex_to_bits(_ex_operator_mode0))
    check_example(1, len(ex_op_m0))
    ex_op_m0_packet = ex_op_m0[0]
    assert isinstance(ex_op_m0_packet, OperatorPacket)
    check_example(0, ex_op_m0_packet.length_type_id)
    check_example(1, ex_op_m0_packet.version)
    check_example(6, ex_op_m0_packet.type_id)
    check_example(2, len(ex_op_m0_packet.subpackets))

    ex_op_m1 = parse_bits(_hex_to_bits(_ex_operator_mode1))
    check_example(1, len(ex_op_m1))
    ex_op_m1_packet = ex_op_m1[0]
    assert isinstance(ex_op_m1_packet, OperatorPacket)
    check_example(1, ex_op_m1_packet.length_type_id)
    check_example(7, ex_op_m1_packet.version)
    check_example(3, ex_op_m1_packet.type_id)
    check_example(3, len(ex_op_m1_packet.subpackets))

    # Real
    packets = parse_bits(_hex_to_bits(_get_puzzle_data()))
    total_version = sum_all_version_numbers(packets)
    print_single_answer(day=PI.day, part=1, value=total_version)
    check_answer(953, total_version, day=PI.day, part=1)

    # Part 2.
    # Examples
    ex_val = parse_bits(list(_parse_hex_to_bin("C200B40A82")))[0].value
    check_example(3, ex_val)
    ex_val = parse_bits(list(_parse_hex_to_bin("04005AC33890")))[0].value
    check_example(54, ex_val)
    ex_val = parse_bits(list(_parse_hex_to_bin("880086C3E88112")))[0].value
    check_example(7, ex_val)
    ex_val = parse_bits(list(_parse_hex_to_bin("CE00C43D881120")))[0].value
    check_example(9, ex_val)
    ex_val = parse_bits(list(_parse_hex_to_bin("D8005AC2A8F0")))[0].value
    check_example(1, ex_val)
    ex_val = parse_bits(list(_parse_hex_to_bin("F600BC2D8F")))[0].value
    check_example(0, ex_val)
    ex_val = parse_bits(list(_parse_hex_to_bin("9C005AC2F8F0")))[0].value
    check_example(0, ex_val)
    ex_val = parse_bits(list(_parse_hex_to_bin("9C0141080250320F1802104A08")))[0].value
    check_example(1, ex_val)

    # Real
    packets = parse_bits(_hex_to_bits(_get_puzzle_data()))
    packet_value = packets[0].value
    print_single_answer(day=PI.day, part=2, value=packet_value)
    check_answer(246225449979, packet_value, day=PI.day, part=2)
    return None


if __name__ == "__main__":
    main()
