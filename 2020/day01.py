# pylint: disable=line-too-long
"""
Day 1: Report Repair

Part 1: Find the two entries in the input list that sum to 2020 and return their product.
Answer: 445536

Part 2: Find three entries in the input list that sum to 2020 and return their product.
Answer: 138688160
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Read the input file and parse it into a list of integers.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[int]: List of expense report numbers.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@profiler
def part_1(entries: List[int]) -> int:
    """
    Find two numbers in the list that add up to 2020 and return their product.

    Args:
        entries (List[int]): List of numbers from the input.

    Returns:
        int: The product of the two numbers that sum to 2020.
    """
    seen = set()
    for num in entries:
        complement = 2020 - num
        if complement in seen:
            return num * complement
        seen.add(num)
    return -1 # Should not happen if input is valid


@profiler
def part_2(entries: List[int]) -> int:
    """
    Find three numbers in the list that add up to 2020 and return their product.

    Args:
        entries (List[int]): List of numbers from the input.

    Returns:
        int: The product of the three numbers that sum to 2020.
    """
    entries_len = len(entries)
    for i in range(entries_len):
        for j in range(i + 1, entries_len):
            a, b = entries[i], entries[j]
            complement = 2020 - a - b
            if complement in entries[j + 1:]:
                return a * b * complement
    return -1 # Should not happen if input is valid


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
