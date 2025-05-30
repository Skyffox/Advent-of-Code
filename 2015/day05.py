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


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Solves part one of the problem using the provided input data.

    A string is considered 'nice' if:
    - It contains at least three vowels (aeiou),
    - It contains at least one letter that appears twice in a row,
    - It does NOT contain the substrings: 'ab', 'cd', 'pq', or 'xy'.

    This function counts how many input strings meet these criteria.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The number of nice strings.
    """
    vowels = "aeiou"
    forbidden = ["ab", "cd", "pq", "xy"]

    def is_nice(s: str) -> bool:
        if sum(s.count(v) for v in vowels) < 3:
            return False
        if not any(s[i] == s[i + 1] for i in range(len(s) - 1)):
            return False
        if any(bad in s for bad in forbidden):
            return False
        return True

    return sum(1 for line in data_input if is_nice(line))


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two of the problem using the provided input data.

    A string is considered 'nice' if:
    - It contains a pair of any two letters that appears at least twice in the string without overlapping,
    - It contains at least one letter which repeats with exactly one letter between them (e.g., 'xyx').

    This function counts how many input strings meet these criteria.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The number of nice strings.
    """

    def is_nice(s: str) -> bool:
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

    return sum(1 for line in data_input if is_nice(line))


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
