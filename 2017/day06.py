# pylint: disable=line-too-long
"""
Day 6: Memory Reallocation

Part 1: Given the initial block counts in your puzzle input, how many redistribution cycles must be completed before a configuration is produced that has been seen before?
Answer: 3156

Part 2: How many cycles are in the infinite loop that arises from the configuration in your puzzle input?
Answer: 1610
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of integers representing memory banks.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: List of memory banks.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        line = file.readline().strip()
        return [int(x) for x in line.split()]


def redistribute(banks: List[int]) -> None:
    """
    Redistributes blocks among memory banks according to the rules.

    Args:
        banks (List[int]): Current state of memory banks.
    """
    length = len(banks)
    max_blocks = max(banks)
    index = banks.index(max_blocks)
    banks[index] = 0
    while max_blocks > 0:
        index = (index + 1) % length
        banks[index] += 1
        max_blocks -= 1


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Finds the number of redistribution cycles before a configuration is repeated.

    Args:
        data_input (List[int]): List of memory banks.

    Returns:
        int: Number of redistribution cycles.
    """
    banks = data_input.copy()
    seen = set()
    steps = 0

    while tuple(banks) not in seen:
        seen.add(tuple(banks))
        redistribute(banks)
        steps += 1

    return steps


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Finds the size of the loop between repeated configurations.

    Args:
        data_input (List[int]): List of memory banks.

    Returns:
        int: Size of the loop.
    """
    banks = data_input.copy()
    seen = {}
    steps = 0

    while tuple(banks) not in seen:
        seen[tuple(banks)] = steps
        redistribute(banks)
        steps += 1

    return steps - seen[tuple(banks)]


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
