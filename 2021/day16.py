# pylint: disable=line-too-long
"""
Day 16: Packet Decoder

Part 1: Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version numbers in all packets?
Answer: 875

Part 2: What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?
Answer: 1264857437203
"""

from typing import Tuple
from utils import profiler


def hex_to_bin(hex_string: str) -> str:
    """
    Converts hexadecimal string to binary string.

    Args:
        hex_string (str): Hex input.

    Returns:
        str: Binary string.
    """
    scale = 16  # hex base
    bits = len(hex_string) * 4
    return bin(int(hex_string, scale))[2:].zfill(bits)


def parse_literal(bits: str, index: int) -> Tuple[int, int]:
    """
    Parses a literal value packet starting at index.

    Args:
        bits (str): Binary string.
        index (int): Current index in bits.

    Returns:
        Tuple[int, int]: (literal value, new index after parsing)
    """
    literal_bits = ""
    while True:
        group = bits[index:index + 5]
        literal_bits += group[1:]
        index += 5
        if group[0] == '0':
            break
    return int(literal_bits, 2), index


def parse_packet(bits: str, index: int) -> Tuple[int, int, int]:
    """
    Parses a packet and its sub-packets recursively.

    Args:
        bits (str): Binary string.
        index (int): Current index.

    Returns:
        Tuple[int, int, int]: (version_sum, value, new index)
    """
    version = int(bits[index:index + 3], 2)
    type_id = int(bits[index + 3:index + 6], 2)
    index += 6

    if type_id == 4:
        # Literal value
        value, index = parse_literal(bits, index)
        return version, value, index

    values = []
    length_type_id = bits[index]
    index += 1

    if length_type_id == '0':
        total_length = int(bits[index:index + 15], 2)
        index += 15
        subpacket_end = index + total_length
        while index < subpacket_end:
            v_sum, val, index = parse_packet(bits, index)
            version += v_sum
            values.append(val)
    else:
        num_subpackets = int(bits[index:index + 11], 2)
        index += 11
        for _ in range(num_subpackets):
            v_sum, val, index = parse_packet(bits, index)
            version += v_sum
            values.append(val)

    # Compute value based on type_id
    if type_id == 0:
        value = sum(values)
    elif type_id == 1:
        value = 1
        for v in values:
            value *= v
    elif type_id == 2:
        value = min(values)
    elif type_id == 3:
        value = max(values)
    elif type_id == 5:
        value = 1 if values[0] > values[1] else 0
    elif type_id == 6:
        value = 1 if values[0] < values[1] else 0
    elif type_id == 7:
        value = 1 if values[0] == values[1] else 0
    else:
        value = 0

    return version, value, index


@profiler
def part_one(data_input: str) -> int:
    """
    Returns the sum of all version numbers in the packet.

    Args:
        data_input (str): Hexadecimal input string.

    Returns:
        int: Sum of versions.
    """
    bits = hex_to_bin(data_input)
    version_sum, _, _ = parse_packet(bits, 0)
    return version_sum


@profiler
def part_two(data_input: str) -> int:
    """
    Evaluates the expression represented by the packets.

    Args:
        data_input (str): Hexadecimal input string.

    Returns:
        int: Evaluated value.
    """
    bits = hex_to_bin(data_input)
    _, value, _ = parse_packet(bits, 0)
    return value


if __name__ == "__main__":
    with open("inputs/16_input.txt", "r", encoding="utf-8") as f:
        input_data = f.read().strip()

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
