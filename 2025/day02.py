# pylint: disable=line-too-long
"""
Day 2 Challenge: Gift Shop

Part 1: Find all Invalid IDs that appear in a given range.
The invalid IDs are any ID made only of some sequence of digits repeated twice.
Answer: 24747430309

Part 2: The invalid IDs can now have a sequence that can be repeated any number of times within the ID.
Answer: 30962646823
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[int, int]]:
    """
    Reads the input file and returns a list of (lower, upper) ranges.

    Expected format:
        "100-200,500-600"
    """
    with open(file_path, "r", encoding="utf-8") as file:
        parts = file.readline().strip().split(",")
        return [tuple(map(int, p.split("-"))) for p in parts]


@profiler
def part_one(data_input: List[Tuple[int, int]]) -> int:
    """
    Solves part one, invalid IDs are those where the number is formed by
    repeating some sequence exactly twice.
    """
    invalid_sum = 0
    for lower_range, upper_range in data_input:
        for num in range(lower_range, upper_range + 1):
            s = str(num)
            n = len(s)

            # Must be even length to be repeated twice
            if n % 2 != 0:
                continue

            half = n // 2
            if s[:half] == s[half:]:
                invalid_sum += num

    return invalid_sum


@profiler
def part_two(data_input: List[Tuple[int, int]]) -> int:
    """
    Solves part two, invalid IDs are those where the number is composed of
    repeating a smaller sequence ANY number of times.

    Examples:
        1212   -> 12 repeated 2 times
        123123 -> 123 repeated 2 times
        777777 -> 7 repeated 6 times
    """
    invalid_sum = 0
    for lower_range, upper_range in data_input:
        for num in range(lower_range, upper_range + 1):
            s = str(num)
            n = len(s)

            # Create sequences up to half the original ID length, we try all possible patterns this way
            for l in range(1, n // 2 + 1):
                # The first part makes sure the sequence is repeatable
                # In the second part, we create a new sequence with the repeatable part until the lengths match each other.
                if n % l == 0 and s[:l] * (n // l) == s:
                    invalid_sum += num
                    break

    return invalid_sum


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
