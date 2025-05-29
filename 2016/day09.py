# pylint: disable=line-too-long
"""
Day 9: Explosives in Cyberspace

Part 1: What is the decompressed length of the file (your puzzle input)? Don't count whitespace.
Answer: 97714

Part 2: What is the decompressed length of the file using this improved format?
Answer: 10762972461
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list containing the single compressed string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List with one element, the compressed string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def decompress_v1(s: str) -> str:
    """
    Decompress the input string (version 1, non-recursive).

    Args:
        s (str): Compressed string.

    Returns:
        str: Decompressed string.
    """
    i = 0
    result = []
    while i < len(s):
        if s[i] == '(':
            end_marker = s.find(')', i)
            marker = s[i + 1:end_marker]
            length, times = map(int, marker.split('x'))
            i = end_marker + 1
            segment = s[i:i+length]
            result.append(segment * times)
            i += length
        else:
            result.append(s[i])
            i += 1
    return "".join(result)


def decompressed_length_v2(s: str, start=0, end=None) -> int:
    """
    Calculates decompressed length of string using version 2 (recursive) without fully decompressing.

    Args:
        s (str): Compressed string.
        start (int): Start index for decompression.
        end (int): End index for decompression.

    Returns:
        int: Decompressed length.
    """
    if end is None:
        end = len(s)
    length = 0
    i = start
    while i < end:
        if s[i] == '(':
            end_marker = s.find(')', i)
            marker = s[i + 1:end_marker]
            l, times = map(int, marker.split('x'))
            i = end_marker + 1
            length += times * decompressed_length_v2(s, i, i + l)
            i += l
        else:
            length += 1
            i += 1
    return length


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Fully decompresses using version 1 rules and returns length.

    Args:
        data_input (List[str]): List with one compressed string.

    Returns:
        int: Length of decompressed string (v1).
    """
    return len(decompress_v1(data_input[0]))


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Calculates decompressed length using version 2 rules (recursive).

    Args:
        data_input (List[str]): List with one compressed string.

    Returns:
        int: Length of decompressed string (v2).
    """
    return decompressed_length_v2(data_input[0])


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
