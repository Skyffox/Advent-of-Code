# pylint: disable=line-too-long
"""
Day 5: Alchemical Reduction

Part 1: How many units remain after fully reacting the polymer you scanned?
Answer: 11668

Part 2: What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?
Answer: 4652
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> str:
    """
    Reads the polymer data from a text file.

    Opens the specified file, reads its entire content, strips any trailing 
    whitespace including newlines, and returns the polymer as a single string.

    Args:
        file_path (str): Path to the input text file containing the polymer data.

    Returns:
        str: The raw polymer string extracted from the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def react_polymer(polymer: str) -> str:
    """
    Processes the polymer by iteratively reacting adjacent units that are 
    the same type but opposite polarity, removing them until no more reactions occur.

    A reaction occurs when two adjacent characters differ only by case 
    (e.g., 'a' and 'A'). These units annihilate each other and are removed.

    Args:
        polymer (str): The input polymer string to be reacted.

    Returns:
        str: The fully reacted polymer string with no further reactions possible.
    """
    stack = []
    for unit in polymer:
        if stack and unit.swapcase() == stack[-1]:
            stack.pop()
        else:
            stack.append(unit)
    return ''.join(stack)


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Calculates the length of the fully reacted polymer for Part 1.

    Extracts the polymer string from input, reacts it fully using `react_polymer`, 
    and returns the length of the resulting polymer.

    Args:
        data_input (List[str]): List of input lines; expects the polymer string as the first item.

    Returns:
        int: Length of the polymer after fully reacting all units.
    """
    polymer = data_input[0]
    reacted_polymer = react_polymer(polymer)
    return len(reacted_polymer)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds the length of the shortest polymer obtainable by removing all units of 
    exactly one type (case-insensitive) and then fully reacting the result.

    For each letter in the alphabet, removes all occurrences (both uppercase and lowercase) 
    from the original polymer, reacts the resulting polymer, and tracks the shortest length 
    encountered.

    Args:
        data_input (List[str]): List of input lines; expects the polymer string as the first item.

    Returns:
        int: The length of the shortest polymer after removing one unit type and reacting.
    """
    polymer = data_input[0]
    min_length = len(polymer)

    for unit in "abcdefghijklmnopqrstuvwxyz":
        filtered_polymer = polymer.replace(unit, "").replace(unit.upper(), "")
        reacted_polymer = react_polymer(filtered_polymer)
        min_length = min(min_length, len(reacted_polymer))

    return min_length


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one([input_data])}")
    print(f"Part 2: {part_two([input_data])}")
