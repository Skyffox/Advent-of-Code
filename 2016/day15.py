# pylint: disable=line-too-long
"""
Day 15: Timing is Everything

Part 1: What is the first time you can press the button to get a capsule?
Answer: 16824

Part 2: With this new disc, and counting again starting from time=0 with the configuration in your puzzle input, 
        what is the first time you can press the button to get another capsule?
Answer: 3543984
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of lines stripped.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def parse_discs(data_input: List[str]) -> List[Tuple[int, int]]:
    """
    Parses the discs from the input lines.

    Args:
        data_input (List[str]): Lines describing discs.

    Returns:
        List[tuple[int, int]]: List of tuples (positions, start_position).
    """
    discs = []
    for line in data_input:
        parts = line.split()
        positions = int(parts[3])
        start_pos = int(parts[-1].strip('.'))
        discs.append((positions, start_pos))
    return discs


def find_time(discs: List[Tuple[int, int]]) -> int:
    """
    Finds the earliest time to press the button to get the capsule through.

    Args:
        discs (List[tuple[int, int]]): List of discs (positions, start_pos).

    Returns:
        int: The earliest time to press the button.
    """
    time = 0
    while True:
        # Check if all discs align at the correct position when capsule reaches them
        if all((start_pos + time + i + 1) % positions == 0 for i, (positions, start_pos) in enumerate(discs)):
            return time
        time += 1


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Solves part one with given discs.

    Args:
        data_input (List[str]): Input lines.

    Returns:
        int: Earliest time to press button.
    """
    discs = parse_discs(data_input)
    return find_time(discs)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two by adding an extra disc.

    Args:
        data_input (List[str]): Input lines.

    Returns:
        int: Earliest time to press button with extra disc.
    """
    discs = parse_discs(data_input)
    # Add extra disc as per part two instructions
    discs.append((11, 0))
    return find_time(discs)


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
