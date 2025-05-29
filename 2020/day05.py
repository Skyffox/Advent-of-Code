# pylint: disable=line-too-long
"""
Day 5: Binary Boarding

Part 1: As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
Answer: 892

Part 2: What is the ID of your seat?
Answer: 625
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]


def seat_id(seat: str) -> int:
    """
    Converts a boarding pass string to a seat ID.
    maketrans() creates a translation table that maps characters from one set to another.
    translate() applies the translation table to a string, replacing each character found in the table.
    Then the entire boarding pass is translated from binary to decimals.

    Args:
        seat (str): A 10-character boarding pass string.

    Returns:
        int: The seat ID.
    """
    return int(seat.translate(str.maketrans("FBLR", "0101")), 2)


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Translate all seat numbers to their corresponding seat ID.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The highest found seat ID.
    """
    return max(seat_id(seat) for seat in data_input)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Find the missing seat ID which corresponds to our seat number.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The seat ID for our seat.
    """
    seat_ids = sorted(seat_id(seat) for seat in data_input)
    for i in range(1, len(seat_ids)):
        if seat_ids[i] != seat_ids[i - 1] + 1:
            return seat_ids[i] - 1
    return -1


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
