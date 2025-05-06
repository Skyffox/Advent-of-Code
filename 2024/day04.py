# pylint: disable=line-too-long
"""
Day 4: Ceres Search

Part 1: Find the word XMAS in all possible directions in a grid
Answer: 2532

Part 2: Find an X of MAS in the same grid
Answer: 1941
"""

from typing import List
from utils import profiler


def search(grid: List[List[str]], word: str, row: int, col: int, step_x: int, step_y: int) -> bool:
    """
    Check if a given word exists in the grid from a starting point in a specific direction.

    Args:
        grid (List[List[str]]): 2D character grid.
        word (str): The target word to search for.
        row (int): Starting row index.
        col (int): Starting column index.
        step_x (int): Step size in x (columns).
        step_y (int): Step size in y (rows).

    Returns:
        bool: True if the word is found in the specified direction, False otherwise.
    """
    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1

    for char in word:
        # See if we go out of bounds
        if row < 0 or row > x_max or col < 0 or col > y_max:
            return False
        # Check character match
        if char != grid[row][col]:
            return False

        row += step_x
        col += step_y

    return True


def get_input(file_path: str) -> List[List[str]]:
    """
    Read the input file and return a 2D grid of characters.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: The parsed grid.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


@profiler
def part_1(grid: List[List[str]]) -> int:
    """
    Count occurrences of the word 'XMAS' in all 8 directions in the grid.

    Args:
        grid (List[List[str]]): The character grid.

    Returns:
        int: Number of times 'XMAS' appears.
    """
    occurrences = 0
    directions = [-1, 0, 1]

    for row_idx, row in enumerate(grid):
        for col_idx, _ in enumerate(row):
            # Do a search for each direction to see if we can find a word
            for step_y in directions:
                for step_x in directions:
                    if step_x == step_y == 0:
                        continue
                    if search(grid, "XMAS", row_idx, col_idx, step_x, step_y):
                        occurrences += 1

    return occurrences


@profiler
def part_2(grid: List[List[str]]) -> int:
    """
    Count 'X' shapes made of the word 'MAS' (or 'SAM') diagonally crossing.
    An 'X' is formed by one instance of 'MAS' or 'SAM' from top-left to bottom-right,
    and another from bottom-left to top-right intersecting at the center letter.

    Args:
        grid (List[List[str]]): The character grid.

    Returns:
        int: Number of 'X' shapes found.
    """
    occurrences = 0

    for col_idx, row in enumerate(grid):
        for row_idx, _ in enumerate(row):
            # Check diagonals for both 'MAS' and 'SAM'
            if (search(grid, "MAS", row_idx, col_idx, 1, 1) or search(grid, "SAM", row_idx, col_idx, 1, 1)) and \
               (search(grid, "MAS", row_idx + 2, col_idx, -1, 1) or search(grid, "SAM", row_idx + 2, col_idx, -1, 1)):
                occurrences += 1

    return occurrences


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
