# pylint: disable=line-too-long
"""
Day 10: Pipe Maze

Part 1: How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
Answer: 6757

Part 2: How many tiles are enclosed by the loop?
Answer: 523
"""

from typing import List, Tuple, Set
from utils import profiler


def get_input(file_path: str) -> Tuple[List[List[str]], Tuple[int, int]]:
    """
    Reads the input file and extracts the grid of pipes and the starting position.

    The input file consists of a grid of characters, where each character represents a part of the loop, 
    and the starting position is marked by 'S'.

    Args:
        file_path (str): The path to the input file containing the grid.

    Returns:
        Tuple[List[List[str]], Tuple[int, int]]: 
            - A 2D list representing the grid of pipes.
            - A tuple (row, col) representing the starting position of 'S'.
    """
    grid = []
    starting_pos = (0, 0)
    with open(file_path, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            row = list(line.strip())
            grid.append(row)
            if 'S' in row:
                starting_pos = (i, row.index('S'))

    return grid, starting_pos


@profiler
def part_1(grid: List[List[str]], start_r: int, start_c: int) -> Tuple[Set[Tuple[int, int]], int]:
    """
    Traces the loop starting from 'S' and determines how many steps it takes to complete the loop.

    Args:
        grid (List[List[str]]): 2D grid representing the pipe system.
        start_r (int): Starting row index.
        start_c (int): Starting column index.

    Returns:
        Tuple[Set[Tuple[int, int]], int]: 
            - Set of coordinates visited during the loop traversal.
            - Total number of steps taken (full loop length).
    """
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    pipe_match = ('|F7', '|LJ', '-FL', '-J7')
    steps = 0

    # Find initial direction to move from 'S'
    for (delta_r, delta_c), pipes in zip(directions, pipe_match):
        next_r, next_c = start_r + delta_r, start_c + delta_c
        if grid[next_r][next_c] in pipes:
            dr, dc = delta_r, delta_c
            r, c = start_r, start_c
            break

    visited: Set[Tuple[int, int]] = {(r, c)}

    while True:
        r += dr
        c += dc
        pipe = grid[r][c]
        visited.add((r, c))
        steps += 1

        if pipe in 'L7':
            dr, dc = dc, dr
        elif pipe in 'FJ':
            dr, dc = -dc, -dr
        elif pipe == 'S':
            break

    return visited, steps


@profiler
def part_2(grid: List[List[str]], main_loop: Set[Tuple[int, int]]) -> int:
    """
    Counts the number of tiles that are enclosed by the main loop.

    It performs a scanline-like traversal of each row, toggling an "inside" flag
    when crossing vertical boundaries, based on pipe shapes.

    Args:
        grid (List[List[str]]): 2D grid of the pipe system.
        main_loop (Set[Tuple[int, int]]): Set of coordinates that form the loop path.

    Returns:
        int: Number of tiles enclosed within the loop.
    """
    area = 0

    for r, row in enumerate(grid):
        inside = False
        for c, cell in enumerate(row):
            if (r, c) not in main_loop:
                area += inside
            else:
                if cell in '|F7':
                    inside ^= True  # Toggle inside state

    return area


if __name__ == "__main__":
    grid_data, start_pos = get_input("inputs/10_input.txt")

    loop_tiles, loop_length = part_1(grid_data, *start_pos)

    print(f"Part 1: {loop_length // 2}")
    print(f"Part 2: {part_2(grid_data, loop_tiles)}")
