# pylint: disable=line-too-long
"""
Day 4: Secure Container

Part 1: How many different passwords within the range given in your puzzle input meet the criteria?
Answer: 594

Part 2: How many different passwords within the range given in your puzzle input meet the additional criteria?
Answer: 364
"""

from collections import Counter
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
        return [line.strip() for line in file]


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Checks whether a password meets the criteria:

    - The number must be exactly six digits long.
    - The number must fall within a given inclusive range.
    - At least one pair of adjacent digits must be identical.
    - From left to right, the digits must not decrease; they can only stay the same or increase.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    range_start, range_end = map(int, data_input[0].split("-"))

    return sum(
        1
        for password in range(range_start, range_end + 1)
        if any(str(password)[i] == str(password)[i + 1] for i in range(5)) and
           all(str(password)[i] <= str(password)[i + 1] for i in range(5))
    )


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Checks whether a password meets the criteria of part 1 
    and an additional rule is introduced:

    - The two adjacent matching digits must not be part of a larger group of matching digits.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two.
    """
    range_start, range_end = map(int, data_input[0].split("-"))

    return sum(
        1
        for password in range(range_start, range_end + 1)
        if all(str(password)[i] <= str(password)[i + 1] for i in range(5)) and
           2 in Counter(str(password)).values()
    )


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
