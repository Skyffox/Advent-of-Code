# pylint: disable=line-too-long
"""
Day 9: Smoke Basin

Part 1: Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
Answer: 500

Part 2: What do you get if you multiply together the sizes of the three largest basins?
Answer: 970200
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Reads the input file and returns a 2D list representing the heightmap.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[List[int]]: 2D grid of heights.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, list(line.strip()))) for line in file.readlines()]


def neighbors(r: int, c: int, max_r: int, max_c: int) -> List[Tuple[int, int]]:
    """
    Returns the valid neighbors (up, down, left, right) of a cell.

    Args:
        r (int): Row index.
        c (int): Column index.
        max_r (int): Maximum row index.
        max_c (int): Maximum column index.

    Returns:
        List[Tuple[int, int]]: List of neighbor coordinates.
    """
    nbrs = []
    if r > 0:
        nbrs.append((r - 1, c))
    if r < max_r - 1:
        nbrs.append((r + 1, c))
    if c > 0:
        nbrs.append((r, c - 1))
    if c < max_c - 1:
        nbrs.append((r, c + 1))
    return nbrs


@profiler
def part_one(heightmap: List[List[int]]) -> int:
    """
    Finds the sum of risk levels of all low points in the heightmap.

    Args:
        heightmap (List[List[int]]): 2D grid of heights.

    Returns:
        int: Sum of risk levels (height + 1) of low points.
    """
    total_risk = 0
    rows, cols = len(heightmap), len(heightmap[0])
    for r in range(rows):
        for c in range(cols):
            current = heightmap[r][c]
            if all(current < heightmap[nr][nc] for nr, nc in neighbors(r, c, rows, cols)):
                total_risk += current + 1
    return total_risk


def basin_size(heightmap: List[List[int]], start: Tuple[int, int], visited: set) -> int:
    """
    Calculates the size of the basin using DFS starting from a low point.

    Args:
        heightmap (List[List[int]]): 2D grid of heights.
        start (Tuple[int, int]): Starting coordinates of the basin.
        visited (set): Set of visited coordinates.

    Returns:
        int: Size of the basin.
    """
    stack = [start]
    basin_points = 0
    rows, cols = len(heightmap), len(heightmap[0])

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))
        if heightmap[r][c] == 9:
            continue
        basin_points += 1
        for nr, nc in neighbors(r, c, rows, cols):
            if (nr, nc) not in visited and heightmap[nr][nc] != 9:
                stack.append((nr, nc))
    return basin_points


@profiler
def part_two(heightmap: List[List[int]]) -> int:
    """
    Finds the product of the sizes of the three largest basins.

    Args:
        heightmap (List[List[int]]): 2D grid of heights.

    Returns:
        int: Product of the three largest basin sizes.
    """
    rows, cols = len(heightmap), len(heightmap[0])
    visited = set()
    basin_sizes = []

    for r in range(rows):
        for c in range(cols):
            current = heightmap[r][c]
            if all(current < heightmap[nr][nc] for nr, nc in neighbors(r, c, rows, cols)):
                size = basin_size(heightmap, (r, c), visited)
                basin_sizes.append(size)

    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
