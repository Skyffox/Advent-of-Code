# pylint: disable=line-too-long
"""
Day 6: Guard Gallivant

Part 1: Find out how many distinct tiles the guard visits
Answer: 5030

Part 2: If we could place an obstacle in any position in the grid how many times would we cause an infinite loop
Answer: 1928 (takes ~16 seconds)
"""

from typing import List, Tuple, Optional, Dict
from utils import profiler


def within_grid(x: int, y: int, x_limit: int, y_limit: int) -> bool:
    """
    Check whether a coordinate is within the grid boundaries.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.
        x_limit (int): Maximum X boundary.
        y_limit (int): Maximum Y boundary.

    Returns:
        bool: True if (x, y) is within grid, False otherwise.
    """
    return 0 <= x < x_limit and 0 <= y < y_limit


def patrol(grid: List[List[str]], pos: Tuple[int, int]) -> Tuple[bool, Optional[List[Tuple[int, int]]]]:
    """
    Simulate guard movement on the grid. Move forward until hitting an obstacle,
    at which point the guard turns right. Track visited positions and detect loops.

    Args:
        grid (List[List[str]]): The grid map.
        pos (Tuple[int, int]): Starting position of the guard.

    Returns:
        Tuple[bool, Optional[List[Tuple[int, int]]]]:
            - True and visited tiles list if the guard exits the grid.
            - False and None if the guard enters an infinite loop.
    """
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0))  # N, E, S, W
    direction_idx = 0
    x_limit = len(grid[0])
    y_limit = len(grid)

    visited: Dict[Tuple[int, int], List[int]] = {pos: [direction_idx]}

    while True:
        next_x = pos[0] + directions[direction_idx][0]
        next_y = pos[1] + directions[direction_idx][1]
        next_pos = (next_x, next_y)

        if not within_grid(next_x, next_y, x_limit, y_limit):
            return True, list(visited.keys())

        if grid[next_y][next_x] == "#":
            direction_idx = (direction_idx + 1) % 4
        else:
            if next_pos in visited:
                if direction_idx in visited[next_pos]:
                    return False, None
                visited[next_pos].append(direction_idx)
            else:
                visited[next_pos] = [direction_idx]
            pos = next_pos


def get_input(file_path: str) -> Tuple[List[List[str]], Tuple[int, int]]:
    """
    Read the grid and starting position from the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple[List[List[str]], Tuple[int, int]]: The grid and starting position.
    """
    grid: List[List[str]] = []
    start_pos = (0, 0)
    with open(file_path, "r", encoding="utf-8") as file:
        for row_idx, line in enumerate(file):
            stripped = line.strip()
            grid.append(list(stripped))
            if "^" in stripped:
                start_pos = (stripped.index("^"), row_idx)
    return grid, start_pos


@profiler
def part_1(grid: List[List[str]], start_pos: Tuple[int, int]) -> int:
    """
    Count how many distinct tiles the guard visits before exiting.

    Args:
        grid (List[List[str]]): The grid map.
        start_pos (Tuple[int, int]): Starting position of the guard.

    Returns:
        int: Number of unique tiles visited.
    """
    _, visited = patrol(grid, start_pos)
    return len(visited) if visited else 0


@profiler
def part_2(grid: List[List[str]], start_pos: Tuple[int, int]) -> int:
    """
    Try placing an obstacle on each tile visited in part 1 to see
    how many placements cause an infinite loop.

    Args:
        grid (List[List[str]]): The grid map.
        start_pos (Tuple[int, int]): Starting position of the guard.

    Returns:
        int: Number of obstacle placements that cause a loop.
    """
    loops_count = 0
    _, visited = patrol(grid, start_pos)

    if not visited:
        return 0

    # We don't have to test every empty space, just the visited ones
    # because the obstruction must be on the visited path
    for x, y in visited:
        if (x, y) == start_pos:
            continue

        # Temporarily place an obstacle
        original = grid[y][x]
        grid[y][x] = "#"

        has_left, _ = patrol(grid, start_pos)
        if not has_left:
            loops_count += 1

        # Restore the grid
        grid[y][x] = original

    return loops_count


if __name__ == "__main__":
    input_data, start = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_1(input_data, start)}")
    print(f"Part 2: {part_2(input_data, start)}")
