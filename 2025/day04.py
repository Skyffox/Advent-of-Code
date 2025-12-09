# pylint: disable=line-too-long
"""
Day 4 Challenge: Printing Department

Part 1: The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions.
How many rolls of paper can be accessed by a forklift?
Answer: 1553

Part 2: Same as part 1, but we keep iterating until no more rolls of paper can be moved. Then count the total rolls of paper that
have been moved.
Answer: 8442
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Read the grid describing the printing department floor.
    Each line represents a row in the grid and consists of "." or "@".

    Args:
        file_path (str): Path to the text file containing the grid.

    Returns:
        List[List[str]]: A 2D list where each inner list contains the characters of a row.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(x.strip()) for x in file.readlines()]


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


def adjacent(grid, x: int, y: int) -> List[Tuple[int, int]]:
    """
    Collect the values of all eight adjacent cells around (x, y).

    Adjacent positions include:
        - the three cells above
        - left and right
        - the three cells below

    Cells outside the grid are treated as "." (empty space).

    Args:
        grid (List[List[str]]): The 2D floor layout.
        x (int): X-coordinate (column index).
        y (int): Y-coordinate (row index).

    Returns:
        List[str]: The cell contents of the valid adjacent positions, in a
                   consistent scanning order. Invalid positions are returned grid[x + dx][y + dy]
                   as ".".
    """
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [grid[x + dx][y + dy] if within_grid(x + dx, y + dy, len(grid[0]), len(grid)) else "." for dx, dy in offsets]


def move_rolls(data_input: List[List[str]]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Identify all rolls currently accessible to forklifts.

    A roll "@" can be moved if fewer than four of its eight adjacent
    cells also contain "@".

    This function performs a single scan of the grid.

    Args:
        data_input (List[List[str]]): The 2D grid representing the floor.

    Returns:
        Tuple[int, List[Tuple[int,int]]]:
            - The number of rolls that can be moved in this scan.
            - A list of coordinates (row, column) for rolls that should be removed.
    """
    rolls_to_be_moved = 0
    coordinates = []

    for x, row in enumerate(data_input):
        for y, cell in enumerate(row):
            if cell == "@":
                surrounding_cells = adjacent(data_input, x, y)
                if surrounding_cells.count("@") < 4:
                    rolls_to_be_moved += 1
                    coordinates.append((x, y))

    return rolls_to_be_moved, coordinates


@profiler
def part_one(data_input: List[List[str]]) -> int:
    """
    Computes how many rolls are accessible based on the rule:
        A roll is accessible if fewer than four of its eight neighbors
        are also rolls.

    This operation is performed once on the initial grid state.

    Args:
        data_input (List[List[str]]): The floor layout.

    Returns:
        int: The number of rolls accessible in the initial configuration.
    """
    rolls, _ = move_rolls(data_input)
    return rolls


@profiler
def part_two(data_input: List[List[str]]) -> int:
    """
    Repeatedly remove all currently accessible rolls until no more can be moved.

    Process:
        1. Run the Part 1 rule on the current grid to find accessible rolls.
        2. Replace each accessible roll "@" with "."
        3. Repeat until a full scan finds zero accessible rolls.

    This simulates a chain reaction where removing rolls reduces local
    congestion, potentially making additional rolls accessible later.

    Args:
        data_input (List[List[str]]): The initial grid.

    Returns:
        int: The total number of rolls moved across all iterations.
    """
    total_moved = 0
    rolls_moved = 1 # Start non-zero to enter loop

    while rolls_moved != 0:
        rolls_moved, coords = move_rolls(data_input)

        # Remove all accessible rolls for next iteration
        for x, y in coords:
            data_input[x][y] = "."

        total_moved += rolls_moved

    return total_moved


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
