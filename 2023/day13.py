# pylint: disable=line-too-long
"""
Day 13: Point of Incidence

Part 1: Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?
Answer: 32723

Part 2: What is the new total if exactly one smudge (character flip) is allowed per pattern?
Answer: 34536
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Reads the input file and returns a list of 2D pattern blocks.
    
    Args:
        file_path (str): The path to the input file that contains the pattern data.

    Returns:
        List[List[str]]: A list of 2D blocks, where each block is a list of strings (lines of the pattern).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        blocks = []
        block = []
        for line in file:
            line = line.rstrip()
            if line:
                block.append(line)
            else:
                blocks.append(block)
                block = []
        if block:
            blocks.append(block)
    return blocks


def find_reflection(grid: List[str], tolerance: int = 0) -> int:
    """
    Finds the first row (or column if transposed) where the grid reflects with up to `tolerance` differences.

    Args:
        grid (List[str]): The grid (rows or columns).
        tolerance (int): Allowed number of mismatches (0 for exact match).

    Returns:
        int: Index of reflection line or 0 if none found.
    """
    for i in range(1, len(grid)):
        top = grid[:i][::-1]
        bottom = grid[i:]
        overlap = min(len(top), len(bottom))
        diff = sum(
            sum(a != b for a, b in zip(top[j], bottom[j]))
            for j in range(overlap)
        )
        if diff == tolerance:
            return i
    return 0


def score(grid: List[str], tolerance: int = 0) -> int:
    """
    Computes the reflection score (100 * row or column index), allowing for a given mismatch tolerance.

    Args:
        grid (List[str]): Grid of pattern rows.
        tolerance (int): Allowed character differences.

    Returns:
        int: Reflection score.
    """
    if row := find_reflection(grid, tolerance):
        return 100 * row

    # Transpose inline
    transposed = [''.join(row[i] for row in grid) for i in range(len(grid[0]))]
    if col := find_reflection(transposed, tolerance):
        return col

    return 0


@profiler
def part_one(data: List[List[str]]) -> int:
    """Solves Part 1 using exact reflection matching."""
    return sum(score(block, tolerance=0) for block in data)


@profiler
def part_two(data: List[List[str]]) -> int:
    """Solves Part 2 allowing exactly one character mismatch."""
    return sum(score(block, tolerance=1) for block in data)


if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
