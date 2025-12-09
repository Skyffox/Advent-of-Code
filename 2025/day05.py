# pylint: disable=line-too-long
"""
Day 5 Challenge: Cafeteria 

Part 1: Count how many ingredient IDs fall within at least one freshness range.
Answer: 773

Part 2: Merges overlapping freshness ranges and computes the total covered length.
Answer: 332067203034711
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Parse the puzzle input into two structures:
    - A list of (start, end) integer ranges.
    - A list of ingredient IDs.

    Lines containing a hyphen ("-") are treated as ranges.
    Other non-empty lines are treated as ingredient IDs.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        tuple[list[tuple[int, int]], list[int]]:
            A tuple containing:
                - fresh_ranges: list of (lower, upper) integer pairs.
                - ingredient_ids: list of individual ingredient integer IDs.
    """
    fresh_range, ids = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue # Skip the blank line
            if "-" in line:
                a, b = line.split("-")
                fresh_range.append((int(a), int(b)))
            else:
                ids.append(int(line))

    return fresh_range, ids


@profiler
def part_one(fresh_ranges: List[Tuple[int, int]], ingredient_ids: List[int]) -> int:
    """
    Count how many ingredient IDs fall in at least one freshness range.

    Args:
        fresh_ranges (list[tuple[int, int]]): Freshness interval ranges.
        ingredient_ids (list[int]): Ingredient IDs to evaluate.

    Returns:
        int: Number of IDs that fall within any range.
    """
    num_of_fresh = 0
    for ingredient_id in ingredient_ids:
        for lower, upper in fresh_ranges:
            if lower <= ingredient_id <= upper:
                num_of_fresh += 1
                break

    return num_of_fresh


@profiler
def part_two(fresh_ranges: List[Tuple[int, int]]) -> int:
    """
    Merge overlapping freshness ranges and sum the total covered span.

    Args:
        fresh_ranges (list[tuple[int, int]]): List of raw freshness ranges.

    Returns:
        int: Total length covered by merged intervals.
    """
    # Sort ranges by start
    fresh_ranges = sorted(fresh_ranges)

    merged = []
    current_start, current_end = fresh_ranges[0]

    # Merge intervals
    for start, end in fresh_ranges[1:]:
        if start <= current_end + 1:
            # Overlaps or touches → merge
            current_end = max(current_end, end)
        else:
            # No overlap → push old interval
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    merged.append((current_start, current_end))

    # Sum interval lengths
    return sum(e - s + 1 for s, e in merged)


if __name__ == "__main__":
    # Get input data
    fresh, ingredient = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one(fresh, ingredient)}")
    print(f"Part 2: {part_two(fresh)}")
