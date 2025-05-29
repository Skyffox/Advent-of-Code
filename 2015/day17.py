# pylint: disable=line-too-long
"""
Day 17: No Such Thing as Too Much

Part 1: Filling all containers entirely, how many different combinations of containers can exactly fit all 150 liters of eggnog?
Answer: 4372

Part 2: Find the minimum number of containers that can exactly fit all 150 liters of eggnog. How many different ways can you fill 
        that number of containers and still hold exactly 150 litres?
Answer: 4
"""

from typing import List
import itertools
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of integers (container sizes).

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[int]: List of container sizes.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@profiler
def part_one(containers: List[int]) -> int:
    """
    Counts the number of combinations of containers that sum to 150 liters.

    Args:
        containers (List[int]): List of container sizes.

    Returns:
        int: Number of valid combinations.
    """
    target = 150
    count = 0
    n = len(containers)
    for r in range(1, n + 1):
        for combo in itertools.combinations(containers, r):
            if sum(combo) == target:
                count += 1
    return count


@profiler
def part_two(containers: List[int]) -> int:
    """
    Counts how many combinations use the minimum number of containers to sum to 150.

    Args:
        containers (List[int]): List of container sizes.

    Returns:
        int: Number of combinations using minimal containers.
    """
    target = 150
    n = len(containers)
    valid_combos = []
    for r in range(1, n + 1):
        combos = [combo for combo in itertools.combinations(containers, r) if sum(combo) == target]
        if combos:
            valid_combos = combos
            break
    return len(valid_combos)


if __name__ == "__main__":
    input_data = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
