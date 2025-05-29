# pylint: disable=line-too-long
"""
Day 11: Dumbo Octopus

Part 1: Given the starting energy levels of the dumbo octopuses in your cavern, simulate 100 steps. How many total flashes are there after 100 steps?
Answer: 1647

Part 2: If you can calculate the exact moments when the octopuses will all flash simultaneously, you should be able to navigate through the cavern. 
        What is the first step during which all octopuses flash?
Answer: 348
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Reads the input file and returns a 2D grid of octopus energy levels.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[List[int]]: 2D grid of energy levels.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, list(line.strip()))) for line in file.readlines()]


def neighbors(r: int, c: int, max_r: int, max_c: int) -> List[Tuple[int, int]]:
    """
    Returns all neighbors (including diagonals) of a cell in the grid.

    Args:
        r (int): Row index.
        c (int): Column index.
        max_r (int): Number of rows.
        max_c (int): Number of columns.

    Returns:
        List[Tuple[int, int]]: List of neighbor coordinates.
    """
    nbrs = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nr, nc = r + dr, c + dc
            if (dr != 0 or dc != 0) and 0 <= nr < max_r and 0 <= nc < max_c:
                nbrs.append((nr, nc))
    return nbrs


def step(grid: List[List[int]]) -> int:
    """
    Executes one simulation step of octopus energy increase and flashing.

    Args:
        grid (List[List[int]]): Current energy grid.

    Returns:
        int: Number of flashes during this step.
    """
    rows, cols = len(grid), len(grid[0])
    flashed = [[False] * cols for _ in range(rows)]

    # First increase all energy by 1
    for r in range(rows):
        for c in range(cols):
            grid[r][c] += 1

    def flash(r: int, c: int):
        if flashed[r][c] or grid[r][c] <= 9:
            return
        flashed[r][c] = True
        for nr, nc in neighbors(r, c, rows, cols):
            grid[nr][nc] += 1
            flash(nr, nc)

    # Flash loop
    for r in range(rows):
        for c in range(cols):
            flash(r, c)

    # Reset energy to 0 for flashed octopuses
    flash_count = 0
    for r in range(rows):
        for c in range(cols):
            if flashed[r][c]:
                grid[r][c] = 0
                flash_count += 1

    return flash_count


@profiler
def part_one(data_input: List[List[int]]) -> int:
    """
    Simulates 100 steps and returns total flashes.

    Args:
        data_input (List[List[int]]): Initial energy grid.

    Returns:
        int: Total flashes after 100 steps.
    """
    grid = [row.copy() for row in data_input]
    total_flashes = 0
    for _ in range(100):
        total_flashes += step(grid)
    return total_flashes


@profiler
def part_two(data_input: List[List[int]]) -> int:
    """
    Finds the first step where all octopuses flash simultaneously.

    Args:
        data_input (List[List[int]]): Initial energy grid.

    Returns:
        int: Step number when all octopuses flash.
    """
    grid = [row.copy() for row in data_input]
    rows, cols = len(grid), len(grid[0])
    total_octopuses = rows * cols
    step_num = 0
    while True:
        step_num += 1
        flashes = step(grid)
        if flashes == total_octopuses:
            return step_num


if __name__ == "__main__":
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
