# pylint: disable=line-too-long
"""
Day 5: Doesn't He Have Intern-Elves For This?

Part 1: How many strings are nice?
Answer: 236

Part 2: How many strings are nice under these new rules?
Answer: 51
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
        return [line.strip() for line in file]


def is_nice_part1(s: str) -> bool:
    """
    Determines if a string is 'nice' based on part 1 rules.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is nice, False otherwise.
    """
    vowels = "aeiou"
    if sum(s.count(v) for v in vowels) < 3:
        return False

    if not any(s[i] == s[i + 1] for i in range(len(s) - 1)):
        return False

    if any(bad in s for bad in ["ab", "cd", "pq", "xy"]):
        return False

    return True


def is_nice_part2(s: str) -> bool:
    """
    Determines if a string is 'nice' based on part 2 rules.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is nice, False otherwise.
    """
    # Check for a pair that appears at least twice without overlapping
    pairs = {}
    has_pair = False
    for i in range(len(s) - 1):
        pair = s[i:i + 2]
        if pair in pairs and i - pairs[pair] > 1:
            has_pair = True
            break
        if pair not in pairs:
            pairs[pair] = i

    # Check for a letter that repeats with exactly one letter between
    has_repeat = any(s[i] == s[i + 2] for i in range(len(s) - 2))

    return has_pair and has_repeat


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    return sum(1 for line in data_input if is_nice_part1(line))


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two.
    """
    return sum(1 for line in data_input if is_nice_part2(line))


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
