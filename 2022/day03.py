# pylint: disable=line-too-long
"""
Day 3: Rucksack Reorganization

Part 1: Find the item type that appears in both compartments of each rucksack.  
Answer: 7845

Part 2: Find the item type that corresponds to the badges of each three-Elf group.  
Answer: 2790
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Read and clean the input data.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[str]: List of rucksack strings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def get_priority(char: str) -> int:
    """
    Get the priority of a given character.

    Lowercase a-z = 1–26  
    Uppercase A-Z = 27–52

    Args:
        char (str): Character to convert.

    Returns:
        int: Priority value.
    """
    return ord(char) - 38 if char.isupper() else ord(char) - 96


@profiler
def part_1(rucksacks: List[str]) -> int:
    """
    For each rucksack, find the item that appears in both halves
    and sum their priorities.

    Args:
        rucksacks (List[str]): List of rucksack strings.

    Returns:
        int: Total priority sum.
    """
    total = 0
    for sack in rucksacks:
        half = len(sack) // 2
        left = set(sack[:half])
        right = set(sack[half:])
        common = left.intersection(right).pop()
        total += get_priority(common)

    return total


@profiler
def part_2(rucksacks: List[str]) -> int:
    """
    For each group of three rucksacks, find the common item (badge)
    and sum their priorities.

    Args:
        rucksacks (List[str]): List of rucksack strings.

    Returns:
        int: Total badge priority sum.
    """
    total = 0
    for i in range(0, len(rucksacks), 3):
        group = rucksacks[i:i+3]
        common = set(group[0]).intersection(group[1], group[2]).pop()
        total += get_priority(common)

    return total


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
