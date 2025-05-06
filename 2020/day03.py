# pylint: disable=line-too-long
"""
Day 3: Toboggan Trajectory

Part 1: Find all the trees we encounter if we go down 1 and 3 to the right for each step.
Answer: 278

Part 2: Do the same as Part 1 but with different steps to the right and down.
Answer: 9709761600
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input data from the specified file and returns the grid of slopes.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[str]: A list of strings representing the grid of slopes, where each string represents a row.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def slope(grid: List[str], dx: int, dy: int) -> int:
    """
    Calculates the number of trees encountered when traversing the grid, given a step pattern of dx (right) and dy (down).

    Args:
        grid (List[str]): The list of strings representing the grid.
        dx (int): The number of steps to move to the right on each iteration.
        dy (int): The number of steps to move down on each iteration.

    Returns:
        int: The total number of trees encountered on the slope.
    """
    n, x, y = 0, 0, 0
    while y < len(grid) - 1:
        x += dx
        y += dy

        # If we go beyond the grid's width, wrap around to the start
        if x >= len(grid[0]):
            x %= len(grid[0])

        # Check if we encountered a tree
        if grid[y][x] == "#":
            n += 1

    return n


@profiler
def part_1(grid: List[str]) -> int:
    """
    Calculate the number of trees encountered when moving 3 steps right and 1 step down at each iteration.

    Args:
        grid (List[str]): The list of strings representing the grid.

    Returns:
        int: The number of trees encountered on the slope.
    """
    return slope(grid, 3, 1)


@profiler
def part_2(grid: List[str]) -> int:
    """
    Calculate the product of the number of trees encountered on multiple slopes with different step patterns.

    Args:
        grid (List[str]): The list of strings representing the grid.

    Returns:
        int: The product of the number of trees encountered on each slope.
    """
    result = 1
    result *= slope(grid, 1, 1) # Slope: 1 right, 1 down
    result *= slope(grid, 3, 1) # Slope: 3 right, 1 down
    result *= slope(grid, 5, 1) # Slope: 5 right, 1 down
    result *= slope(grid, 7, 1) # Slope: 7 right, 1 down
    result *= slope(grid, 1, 2) # Slope: 1 right, 2 down

    return result


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
