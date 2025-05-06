# pylint: disable=line-too-long
"""
Day 4: Camp Cleanup

Part 1: In how many assignment pairs does one range fully contain the other?  
Answer: 644

Part 2: In how many assignment pairs do the ranges overlap?  
Answer: 926
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Parse input into pairs of integer ranges.

    Args:
        file_path (str): Path to input file.

    Returns:
        List[Tuple[Tuple[int, int], Tuple[int, int]]]: List of assignment range pairs.
    """
    assignments = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            first, second = line.strip().split(",")
            a_start, a_end = map(int, first.split("-"))
            b_start, b_end = map(int, second.split("-"))
            assignments.append(((a_start, a_end), (b_start, b_end)))
    return assignments


@profiler
def part_1(assignments: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> int:
    """
    Count how many times one range fully contains the other.

    Args:
        assignments (List[Tuple]): List of range pairs.

    Returns:
        int: Count of fully contained ranges.
    """
    count = 0
    for (a_start, a_end), (b_start, b_end) in assignments:
        if (a_start >= b_start and a_end <= b_end) or (b_start >= a_start and b_end <= a_end):
            count += 1

    return count


@profiler
def part_2(assignments: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> int:
    """
    Count how many range pairs have any overlap.

    Args:
        assignments (List[Tuple]): List of range pairs.

    Returns:
        int: Count of overlapping ranges.
    """
    count = 0
    for (a_start, a_end), (b_start, b_end) in assignments:
        if a_start <= b_end and b_start <= a_end:
            count += 1

    return count


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
