# pylint: disable=line-too-long
"""
Day 15: Chiton

Part 1: What is the lowest total risk of any path from the top left to the bottom right?
Answer: 824

Part 2: Using the full map, what is the lowest total risk of any path from the top left to the bottom right?
Answer: 3063
"""

from typing import Generator, List, Tuple
from heapq import heappush, heappop
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Reads the input file and returns the risk level grid.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[List[int]]: 2D grid of risk levels.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, line.strip())) for line in file.readlines()]


def neighbors(r: int, c: int, max_r: int, max_c: int) -> Generator[Tuple[int, int], None, None]:
    """
    Returns neighbors up, down, left, right inside grid.

    Args:
        r (int): row index.
        c (int): column index.
        max_r (int): max rows.
        max_c (int): max cols.

    Returns:
        List[Tuple[int, int]]: neighboring coordinates.
    """
    for nr, nc in ((r-1, c), (r+1, c), (r, c-1), (r, c+1)):
        if 0 <= nr < max_r and 0 <= nc < max_c:
            yield nr, nc


@profiler
def dijkstra(grid: List[List[int]]) -> int:
    """
    Finds lowest total risk path from top-left to bottom-right using Dijkstra's algorithm.

    Args:
        grid (List[List[int]]): Risk grid.

    Returns:
        int: Lowest total risk (excluding starting point).
    """
    max_r, max_c = len(grid), len(grid[0])
    dist = [[float('inf')] * max_c for _ in range(max_r)]
    dist[0][0] = 0
    heap = [(0, 0, 0)] # (risk, row, col)

    while heap:
        risk, r, c = heappop(heap)
        if (r, c) == (max_r - 1, max_c - 1):
            return risk
        if risk > dist[r][c]:
            continue
        for nr, nc in neighbors(r, c, max_r, max_c):
            new_risk = risk + grid[nr][nc]
            if new_risk < dist[nr][nc]:
                dist[nr][nc] = new_risk
                heappush(heap, (new_risk, nr, nc))
    return -1


def expand_grid(grid: List[List[int]]) -> List[List[int]]:
    """
    Expands the grid 5 times in both directions with increased risk levels.

    Args:
        grid (List[List[int]]): Original risk grid.

    Returns:
        List[List[int]]: Expanded risk grid.
    """
    orig_r, orig_c = len(grid), len(grid[0])
    new_r, new_c = orig_r * 5, orig_c * 5
    expanded = [[0] * new_c for _ in range(new_r)]

    for i in range(new_r):
        for j in range(new_c):
            inc = (i // orig_r) + (j // orig_c)
            val = grid[i % orig_r][j % orig_c] + inc
            if val > 9:
                val = val % 9
            expanded[i][j] = val
    return expanded


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    expanded_grid = expand_grid(input_data)

    print(f"Part 1: {dijkstra(input_data)}")
    print(f"Part 2: {dijkstra(expanded_grid)}")
