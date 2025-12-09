# pylint: disable=line-too-long
"""
Day 7 Challenge: Laboratories 

Part 1: We located a diagram of the tachyon manifold. A tachyon beam enters the manifold at the location marked S; tachyon beams always move downward. 
Tachyon beams pass freely through empty space (.). However, if a tachyon beam encounters a splitter (^), the beam is stopped; instead,
a new tachyon beam continues from the immediate left and from the immediate right of the splitter. Find How many times the beam will split.
Answer: 1635

Part 2: We have noticed that it isn't a classical tachyon manifold - it's a quantum tachyon manifold. Now each time a particle reaches a splitter, 
it's actually time itself which splits. In one timeline, the particle went left, and in the other timeline, the particle went right.
To fix the manifold, what you really need to know is the number of timelines active after a single particle completes all of its possible journeys through the manifold.
Answer: 58097428661390
"""

from typing import List
from functools import lru_cache
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Reads the input file and converts each line into a list of characters.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[List[str]]: A 2D grid representation of the input.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


def within_grid(x: int, y: int, x_limit: int, y_limit: int) -> bool:
    """
    Checks if the given coordinates are within the bounds of the grid.

    Args:
        x (int): The x-coordinate to check.
        y (int): The y-coordinate to check.
        x_limit (int): The width of the grid (i.e., number of columns).
        y_limit (int): The height of the grid (i.e., number of rows).

    Returns:
        bool: True if (x, y) lies within the grid; False otherwise.
    """
    return 0 <= x < x_limit and 0 <= y < y_limit


@profiler
def part_one(grid: List[List[str]]) -> int:
    """
    Counts the total number of splits a tachyon beam encounters in the classical manifold.

    - The beam starts at 'S' and moves downward.
    - Empty cells ('.') are passed freely.
    - Splitters ('^') create new beams to the left and right; each split is counted.
    
    Args:
        grid (List[List[str]]): The input grid representing the manifold.

    Returns:
        int: Total number of splits encountered.
    """
    total_splits = 0
    rows, cols = len(grid), len(grid[0])

    for row_idx, row in enumerate(grid):
        if "S" in row:
            start_col = row.index("S")
            # Mark the cell below as a beam
            if within_grid(row_idx + 1, start_col, rows, cols):
                grid[row_idx + 1][start_col] = "|"

        for col_idx, cell in enumerate(row):
            if cell == "|":
                below_row = row_idx + 1
                below_col = col_idx

                if within_grid(below_row, below_col, rows, cols):
                    below_cell = grid[below_row][below_col]

                    if below_cell == "^":
                        total_splits += 1
                        # Spread beams to left
                        if within_grid(below_row, below_col - 1, rows, cols) and grid[below_row][below_col - 1] != "^":
                            grid[below_row][below_col - 1] = "|"
                        # Spread beams to right
                        if within_grid(below_row, below_col + 1, rows, cols) and grid[below_row][below_col + 1] != "^":
                            grid[below_row][below_col + 1] = "|"
                    else:
                        # Continue downward
                        grid[below_row][below_col] = "|"

    return total_splits


@profiler
def part_two(grid: List[str]) -> int:
    # first try was a DFS over all paths. You should use dynamic programming (DP) with memoization.
    """
    First try was using a DFS over all paths. Then realised this was a bad idea as all paths are searched 
    recursively meaning that there are a lot of recurring computations through re-exploring subtrees.

    This implementation uses a Dynamic Programming approach, this is a lot better as each cell's 
    answer is only computed once, through memoization. The complexity then becomes: O(rows x cols) 
    instead of exponential.

    Counts the total number of timelines after a tachyon beam explores all possible paths
    in the quantum manifold.

    Args:
        grid (List[List[str]]): The input grid representing the quantum manifold.

    Returns:
        int: Total number of timelines.
    """
    # The start can always be found in the first row
    start = (0, grid[0].index("S"))
    rows, cols = len(grid), len(grid[0])

    @lru_cache(None)
    def count_paths(r: int, c: int) -> int:
        """
        Recursively counts all paths from position (r, c) to the bottom of the grid.

        Args:
            r (int): Current row.
            c (int): Current column.

        Returns:
            int: Number of paths from this cell to the bottom.
        """
        next_row = r + 1
        nc = c

        # Reached the bottom: one valid path
        if next_row >= rows:
            return 1

        cell_below = grid[next_row][c]

        if cell_below  in ('.', '|'):
            # Continue straight down
            return count_paths(next_row, c)

        # Splitter: create paths to left and right
        total = 0

        # Left-down
        if c - 1 >= 0:
            total += count_paths(next_row, nc - 1)

        # Right-down
        if c + 1 < cols:
            total += count_paths(next_row, nc + 1)

        return total

    return count_paths(*start)


if __name__ == "__main__":
    # Get input data
    input_grid = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_grid)}")
    print(f"Part 2: {part_two(input_grid)}")
