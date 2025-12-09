# pylint: disable=line-too-long
"""
Day 1 Challenge: Secret Entrance

Part 1: Crack the password by counting the number of times the dial is left pointing at 0 after any rotation in the sequence.
Answer: 997

Part 2: Now you need to count the number of times any click causes the dial to point at 0, regardless of whether it happens during a rotation or at the end of one.
Answer: 5978
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[str, int]]:
    """
    Reads the input file and returns a list of (direction, distance) tuples.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[tuple[str, int]]: Parsed (direction, distance) pairs.
    """
    result = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # First character is direction, rest is integer
            result.append((line[0], int(line[1:])))
    return result


@profiler
def part_one(data_input: List[Tuple[str, int]]) -> int:
    """
    Solves part one, count how many the lock stands still on 0.

    Args:
        data_input (List[Tuple[str, int]]): Parsed puzzle input.

    Returns:
        int: Number of times the position lands on 0.
    """
    pos = 50
    zero_hits = 0

    for direction, distance in data_input:
        delta = -distance if direction == "L" else distance
        pos = (pos + delta) % 100

        if pos == 0:
            zero_hits += 1

    return zero_hits


@profiler
def part_two(data_input: List[Tuple[str, int]]) -> int:
    """
    Solves part two, count how many times the lock passes or stands still on 0.

    Args:
        data_input (List[Tuple[str, int]]): Parsed puzzle input.

    Returns:
        int: Number of times the position lands on 0.
    """
    pos = 50
    zero_hits = 0

    for direction, steps in data_input:
        # +1 for L (increasing), -1 for R (decreasing)
        step_dir = 1 if direction == "L" else -1

        for _ in range(steps):
            pos = (pos + step_dir) % 100

            # Count whenever we land exactly on 0
            if pos == 0:
                zero_hits += 1

    return zero_hits


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
