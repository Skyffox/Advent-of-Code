# pylint: disable=line-too-long
"""
Day 8: Resonant Collinearity

Part 1: Two of the same antennas create an antinode that is in the position that extends from the two antennas, in both directions
        Find the amount of antinodes that are still in the grid
Answer: 301

Part 2: Same as part 1, but the antinodes now propagate in both directions
Answer: 1019
"""

from typing import List, Dict
from utils import profiler


def within_grid(x: int, y: int, x_limit: int, y_limit: int) -> bool:
    """
    Check if the given coordinates (x, y) are within the bounds of the grid.

    Args:
        x (int): The x-coordinate (column index) to check.
        y (int): The y-coordinate (row index) to check.
        x_limit (int): The maximum allowable x-coordinate (width of the grid).
        y_limit (int): The maximum allowable y-coordinate (height of the grid).

    Returns:
        bool: `True` if the coordinates (x, y) are within the grid, `False` otherwise.
    """
    return 0 <= x < x_limit and 0 <= y < y_limit


def get_input(file_path: str) -> List[List[str]]:
    """
    Reads a grid from a file and returns it as a list of lists.

    Args:
        file_path (str): The path to the input file containing the grid data.

    Returns:
        List[List[str]]: A 2D list where each sublist represents a row of the grid, 
                          and each element in the sublist is a character in that row.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


def find_antennas(grid: List[List[str]]) -> Dict[str, List[List[int]]]:
    """
    This function scans through the grid to find all instances of antennas (non-empty cells).
    It creates a dictionary that groups the same types of antennas together, mapping each antenna
    type to a list of coordinates where that antenna appears.

    Args:
        grid (List[List[str]]): A 2D list representing the grid, where each element is a character.
        
    Returns:
        Dict[str, List[List[int]]]: A dictionary where keys are antenna types (characters) and values are lists of 
                                     coordinates (tuples) where the antennas are located.
    """
    antennas: Dict[str, List[List[int]]] = {}
    for y, row in enumerate(grid):
        for x, item in enumerate(row):
            if item != ".":
                if item not in antennas:
                    antennas[item] = [[y, x]]
                else:
                    antennas[item].append([y, x])
    return antennas


@profiler
def antinodes(grid: List[List[str]], antennas: Dict[str, List[List[int]]], is_part2: bool = False) -> int:
    """
    This function calculates antinodes, which are points formed by the interaction of 
    antennas. For part 1, it calculates the antinodes by finding the difference between
    antenna coordinates. For part 2, it additionally propagates antinodes in both directions
    to extend the pattern.

    Args:
        grid (List[List[str]]): A 2D list representing the grid.
        antennas (Dict[str, List[List[int]]]): A dictionary of antennas and their coordinates.
        is_part2 (bool, optional): If `True`, calculates the antinodes for part 2, where 
                                   propagation occurs in both directions. Defaults to `False`.

    Returns:
        int: The number of antinodes formed on the grid.
    """
    x_limit = len(grid[0])
    y_limit = len(grid)

    # Create an empty grid to store the antinodes.
    antinode_grid: List[List[str]] = [["."] * x_limit for _ in range(y_limit)]

    # Iterate over each antenna type
    for _, positions in antennas.items():
        # Loop twice over all locations and compare each location with the others
        for idx, loc1 in enumerate(positions):
            for loc2 in positions[idx + 1:]:
                # Calculate the difference in coordinates between two antennas
                x_diff, y_diff = loc1[0] - loc2[0], loc1[1] - loc2[1]
                # Compute the positions of the antinodes
                antinode_1x, antinode_1y = loc1[0] + x_diff, loc1[1] + y_diff
                antinode_2x, antinode_2y = loc2[0] - x_diff, loc2[1] - y_diff

                # If the antinode is within bounds, mark it on the grid
                if within_grid(antinode_1x, antinode_1y, x_limit, y_limit):
                    antinode_grid[antinode_1x][antinode_1y] = "#"
                if within_grid(antinode_2x, antinode_2y, x_limit, y_limit):
                    antinode_grid[antinode_2x][antinode_2y] = "#"

                if is_part2:
                    # In Part 2, mark the antenna locations as antinodes
                    antinode_grid[loc1[0]][loc1[1]] = "#"
                    antinode_grid[loc2[0]][loc2[1]] = "#"

                    # Propagate the antinode in both directions
                    while within_grid(antinode_1x, antinode_1y, x_limit, y_limit):
                        antinode_grid[antinode_1x][antinode_1y] = "#"
                        antinode_1x, antinode_1y = antinode_1x + x_diff, antinode_1y + y_diff
                    while within_grid(antinode_2x, antinode_2y, x_limit, y_limit):
                        antinode_grid[antinode_2x][antinode_2y] = "#"
                        antinode_2x, antinode_2y = antinode_2x - x_diff, antinode_2y - y_diff

    # Count and return the number of antinodes (represented by "#")
    return sum([row.count("#") for row in antinode_grid])


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")
    antennae = find_antennas(input_data)

    print(f"Part 1: {antinodes(input_data, antennae)}")
    print(f"Part 2: {antinodes(input_data, antennae, True)}")
