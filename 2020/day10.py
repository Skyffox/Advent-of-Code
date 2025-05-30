# pylint: disable=line-too-long
"""
Day 10: Adapter Array

Part 1: What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
Answer: 2400

Part 2: What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?
Answer: 133496
"""

from typing import List
from collections import defaultdict
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of integers representing adapter joltages.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[int]: A list of adapter joltages.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file.readlines()]


@profiler
def part_one(adapters: List[int]) -> int:
    """
    Calculates the product of the number of 1-jolt differences and 3-jolt differences between
    consecutive adapters when the adapters are sorted.

    This solves part one of the adapter joltage problem, where the goal is to find
    these differences to determine a specific metric about the adapter chain.

    Args:
        data_input (List[int]): A list of adapter joltages.

    Returns:
        int: The product of the count of 1-jolt and 3-jolt differences.
    """
    adapters = [0] + sorted(adapters) + [max(adapters) + 3]
    diffs = {1: 0, 3: 0}
    for i in range(1, len(adapters)):
        diff = adapters[i] - adapters[i - 1]
        diffs[diff] += 1
    return diffs[1] * diffs[3]


@profiler
def part_two(adapters: List[int]) -> int:
    """
    Determines the total number of distinct ways to arrange the adapters to connect
    the charging outlet to the device.

    This solves part two by calculating the total valid adapter arrangements.

    Args:
        data_input (List[int]): A list of adapter joltages.

    Returns:
        int: The total number of valid adapter arrangements.
    """
    adapters = [0] + sorted(adapters) + [max(adapters) + 3]
    paths = defaultdict(int)
    paths[0] = 1
    for adapter in adapters[1:]:
        paths[adapter] = paths[adapter - 1] + paths[adapter - 2] + paths[adapter - 3]
    return paths[adapters[-1]]


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
