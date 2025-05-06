# pylint: disable=line-too-long
"""
Day 1: Chronal Calibration

Part 1: Calculate the resulting frequency after applying all frequency changes.  
Answer: 505

Part 2: Find the first frequency that is reached twice when applying changes in a loop.  
Answer: 72330
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads frequency changes from the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[int]: A list of integer frequency changes.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@profiler
def part_1(changes: List[int]) -> int:
    """
    Calculates the resulting frequency after applying all changes once.

    Args:
        changes (List[int]): The list of frequency changes.

    Returns:
        int: The final frequency.
    """
    return sum(changes)


@profiler
def part_2(changes: List[int]) -> int:
    """
    Finds the first frequency that is reached twice by repeatedly applying the changes.

    Args:
        changes (List[int]): The list of frequency changes.

    Returns:
        int: The first repeated frequency.
    """
    seen = {0}
    current = 0
    while True:
        for change in changes:
            current += change
            if current in seen:
                return current
            seen.add(current)


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
