# pylint: disable=line-too-long
"""
Day 5: Hydrothermal Venture

Part 1: Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
Answer: 5585

Part 2: Consider all of the lines. At how many points do at least two lines overlap?
Answer: 17193
"""

from collections import defaultdict
from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[int, int, int, int]]:
    """
    Reads the input file and returns a list of line segments as tuples (x1, y1, x2, y2).

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Tuple[int, int, int, int]]: List of line segments.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().strip().split("\n")
        segments = []
        for line in lines:
            left, right = line.split(" -> ")
            x1, y1 = map(int, left.split(","))
            x2, y2 = map(int, right.split(","))
            segments.append((x1, y1, x2, y2))
        return segments


@profiler
def mark_lines(segments: List[Tuple[int, int, int, int]], include_diagonal: bool) -> int:
    """
    Marks the points on the grid covered by the lines and counts overlaps.

    Args:
        segments (List[Tuple[int, int, int, int]]): List of line segments.
        include_diagonal (bool): Whether to include diagonal lines at 45 degrees.

    Returns:
        int: Number of points where at least two lines overlap.
    """
    grid = defaultdict(int)

    for x1, y1, x2, y2 in segments:
        if x1 == x2:
            # Vertical line
            start, end = sorted([y1, y2])
            for y in range(start, end + 1):
                grid[(x1, y)] += 1
        elif y1 == y2:
            # Horizontal line
            start, end = sorted([x1, x2])
            for x in range(start, end + 1):
                grid[(x, y1)] += 1
        elif include_diagonal and abs(x2 - x1) == abs(y2 - y1):
            # Diagonal 45 degrees
            length = abs(x2 - x1)
            dx = 1 if x2 > x1 else -1
            dy = 1 if y2 > y1 else -1
            for i in range(length + 1):
                grid[(x1 + i * dx, y1 + i * dy)] += 1

    return sum(1 for v in grid.values() if v >= 2)


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {mark_lines(input_data, include_diagonal=False)}")
    print(f"Part 2: {mark_lines(input_data, include_diagonal=True)}")
