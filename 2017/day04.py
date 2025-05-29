# pylint: disable=line-too-long
"""
Day 4: High-Entropy Passphrase

Part 1: The system's full passphrase list is available as your puzzle input. How many passphrases are valid?
Answer: 451

Part 2: Under this new system policy, how many passphrases are valid?
Answer: 223
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of passphrases (lines).

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of passphrase strings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Counts valid passphrases with no duplicate words.

    Args:
        data_input (List[str]): List of passphrases.

    Returns:
        int: Number of valid passphrases.
    """
    valid_count = 0
    for line in data_input:
        words = line.split()
        if len(words) == len(set(words)):
            valid_count += 1
    return valid_count


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Counts valid passphrases with no two words being anagrams.

    Args:
        data_input (List[str]): List of passphrases.

    Returns:
        int: Number of valid passphrases.
    """
    valid_count = 0
    for line in data_input:
        words = line.split()
        normalized = [''.join(sorted(word)) for word in words]
        if len(normalized) == len(set(normalized)):
            valid_count += 1
    return valid_count


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
