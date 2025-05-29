# pylint: disable=line-too-long
"""
Day 16: Dragon Checksum

Part 1: The first disk you have to fill has length 272. Using the initial state in your puzzle input, what is the correct checksum?
Answer: 10111110010110110

Part 2: The second disk you have to fill has length 35651584. Again using the initial state in your puzzle input, what is the correct checksum for this disk?
Answer: 01101100001100100
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns the initial state string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List containing the initial state string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def dragon_curve(data: str, length: int) -> str:
    """
    Expands data using the dragon curve until reaching given length.

    Args:
        data (str): Initial data string.
        length (int): Desired length of output.

    Returns:
        str: Expanded data string of at least 'length'.
    """
    while len(data) < length:
        b = ''.join('0' if c == '1' else '1' for c in reversed(data))
        data = data + '0' + b
    return data[:length]


def checksum(data: str) -> str:
    """
    Computes checksum for data string.

    Args:
        data (str): Data string.

    Returns:
        str: Checksum string.
    """
    while len(data) % 2 == 0:
        data = ''.join('1' if data[i] == data[i+1] else '0' for i in range(0, len(data), 2))
    return data


@profiler
def part_one(data_input: List[str]) -> str:
    """
    Generates data and computes checksum for length 272.

    Args:
        data_input (List[str]): List containing initial data string.

    Returns:
        str: Checksum string.
    """
    initial = data_input[0]
    length = 272
    expanded = dragon_curve(initial, length)
    return checksum(expanded)


@profiler
def part_two(data_input: List[str]) -> str:
    """
    Generates data and computes checksum for length 35651584.

    Args:
        data_input (List[str]): List containing initial data string.

    Returns:
        str: Checksum string.
    """
    initial = data_input[0]
    length = 35651584
    expanded = dragon_curve(initial, length)
    return checksum(expanded)


if __name__ == "__main__":
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
