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
    Reads the input file and returns the polymer string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        str: The polymer string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def react_polymer(polymer: str) -> str:
    """
    Reacts the polymer by removing adjacent units of opposite polarity.

    Args:
        polymer (str): The polymer string.

    Returns:
        str: The reacted polymer string.
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
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    polymer = data_input[0]
    reacted_polymer = react_polymer(polymer)
    return len(reacted_polymer)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two.
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
