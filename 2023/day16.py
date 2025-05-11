# pylint: disable=line-too-long
"""
Day 16: The Floor Will Be Lava

Part 1: Simulate a laser beam through a grid and count how many tiles become energized.
Answer: 7870

Part 2: Try all possible entry points and directions to find the maximum number of energized tiles.
Answer: 8143
"""

from typing import List, Tuple, Set
from utils import profiler


# Directions represented as (dx, dy) offsets
DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


def get_input(file_path: str) -> List[List[str]]:
    """
    Reads the input file and returns the 2D grid as a list of character lists.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: 2D grid of characters.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f]


def next_dirs(tile: str, direction: str) -> List[str]:
    """
    Determines new directions based on the current tile and beam direction.

    Args:
        tile (str): The tile character ('.', '/', '\\', '|', '-').
        direction (str): Current direction of the beam ('up', 'down', 'left', 'right').

    Returns:
        List[str]: A list of next directions the beam should take.
    """
    if tile == ".":
        return [direction]
    if tile == "/":
        return {
            "up": ["right"],
            "down": ["left"],
            "left": ["down"],
            "right": ["up"]
        }[direction]
    if tile == "\\":
        return {
            "up": ["left"],
            "down": ["right"],
            "left": ["up"],
            "right": ["down"]
        }[direction]
    if tile == "|":
        return [direction] if direction in ("up", "down") else ["up", "down"]
    if tile == "-":
        return [direction] if direction in ("left", "right") else ["left", "right"]
    return []


def simulate_beam(grid: List[List[str]], start_pos: Tuple[int, int], start_dir: str) -> Set[Tuple[int, int]]:
    """
    Simulates a beam of light moving through the grid.

    Args:
        grid (List[List[str]]): The grid of tiles.
        start_pos (Tuple[int, int]): Starting (x, y) position of the beam.
        start_dir (str): Initial direction of the beam.

    Returns:
        Set[Tuple[int, int]]: Set of all energized tile coordinates.
    """
    max_y, max_x = len(grid), len(grid[0])
    seen = set()
    energized = set()
    stack = [(start_pos[0], start_pos[1], start_dir)]

    while stack:
        x, y, d = stack.pop()
        if (x, y, d) in seen:
            continue
        seen.add((x, y, d))

        if not (0 <= x < max_x and 0 <= y < max_y):
            continue

        energized.add((x, y))
        tile = grid[y][x]

        for new_dir in next_dirs(tile, d):
            dx, dy = DIRECTIONS[new_dir]
            stack.append((x + dx, y + dy, new_dir))

    return energized


@profiler
def part_one(grid: List[List[str]]) -> int:
    """
    Computes the number of tiles energized starting from top-left, moving right.

    Args:
        grid (List[List[str]]): The input grid.

    Returns:
        int: Number of energized tiles.
    """
    return len(simulate_beam(grid, (0, 0), "right"))


@profiler
def part_two(grid: List[List[str]]) -> int:
    """
    Computes the maximum number of energized tiles starting from any grid edge.

    Args:
        grid (List[List[str]]): The input grid.

    Returns:
        int: Maximum number of energized tiles.
    """
    max_y, max_x = len(grid), len(grid[0])
    max_energized = 0

    # Top and bottom edges
    for x in range(max_x):
        max_energized = max(max_energized, len(simulate_beam(grid, (x, 0), "down")))
        max_energized = max(max_energized, len(simulate_beam(grid, (x, max_y - 1), "up")))

    # Left and right edges
    for y in range(max_y):
        max_energized = max(max_energized, len(simulate_beam(grid, (0, y), "right")))
        max_energized = max(max_energized, len(simulate_beam(grid, (max_x - 1, y), "left")))

    return max_energized


if __name__ == "__main__":
    input_data = get_input("inputs/16_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
