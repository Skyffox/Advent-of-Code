# pylint: disable=line-too-long
"""
Day 10: Hoof It

Part 1: What is the sum of scores of all starting points, the score is the amount of times a starting point can reach a unique endpoint
Answer: 796

Part 2: What is the sum of the ratings of all trailheads, the rating is the amount of times a starting point can reach an endpoint
Answer: 1942
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[List[List[int]], List[Tuple[int, int]]]:
    """
    Reads the grid data and identifies all starting points.

    Args:
        file_path (str): The path to the input file containing the grid data.

    Returns:
        tuple: A tuple containing:
            - grid (list): A list of lists representing the grid.
            - starting_points (list): A list of tuples representing the coordinates of the starting points in the grid.
    """
    grid = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            grid.append(list(map(int, line.strip())))

    # Every 0 is a starting point
    starting_points = [(x, y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == 0]

    return grid, starting_points


def within_grid(x: int, y: int, x_limit: int, y_limit: int) -> bool:
    """
    Checks if the given coordinates are within the bounds of the grid.

    Args:
        x (int): The x-coordinate to check.
        y (int): The y-coordinate to check.
        x_limit (int): The width of the grid (i.e., number of columns).
        y_limit (int): The height of the grid (i.e., number of rows).

    Returns:
        bool: `True` if the coordinates are within the grid bounds, `False` otherwise.
    """
    return 0 <= x < x_limit and 0 <= y < y_limit


def follow_path(grid: List[List[int]], x: int, y: int, previous: int, path_ends: List[Tuple[int, int]]) -> None:
    """
    Recursively walks through the grid, stopping at the highest point (represented by `9`).

    Args:
        grid (list): The grid representing the terrain.
        x (int): The current x-coordinate.
        y (int): The current y-coordinate.
        previous (tuple[int, int]): The coordinates of the previous cell, used to check the difference in values.
        path_ends (list): A list that stores the coordinates of the endpoints that are reached during the traversal.
    """
    if not within_grid(x, y, len(grid[0]), len(grid)):
        return

    current = grid[y][x]
    if current - previous != 1:
        return
    if current == 9:
        path_ends.append((x, y))
        return
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        follow_path(grid, x + dx, y + dy, current, path_ends)


@profiler
def part_one(grid: List[List[int]], start_points: List[Tuple[int, int]]) -> int:
    """
    For each starting point, the function finds all the endpoints it can reach by following the path, and the score
    for each starting point is the number of unique endpoints it can reach. The function then returns the sum of all
    the scores.

    Args:
        grid (list): The grid representing the terrain.
        start_points (list): A list of tuples representing the starting points in the grid.

    Returns:
        int: The sum of the scores for all starting points, where the score is the number of unique endpoints that
            can be reached from each starting point.
    """
    score_unique = []
    for x, y in start_points:
        path_ends = []
        follow_path(grid, x, y, -1, path_ends)
        score_unique.append(len(set(path_ends)))

    return sum(score_unique)


@profiler
def part_two(grid: List[List[int]], start_points: List[Tuple[int, int]]) -> int:
    """
    For each starting point, the function finds all the endpoints it can reach, and the rating for each starting point
    is the total number of times it can reach an endpoint. The function then returns the sum of all the ratings.

    Args:
        grid (list): The grid representing the terrain.
        start_points (list): A list of tuples representing the starting points in the grid.

    Returns:
        int: The sum of the ratings for all starting points, where the rating is the number of times each starting point
            can reach an endpoint.
    """
    score_rating = []
    for x, y in start_points:
        path_ends = []
        follow_path(grid, x, y, -1, path_ends)
        score_rating.append(len(path_ends))

    return sum(score_rating)


if __name__ == "__main__":
    input_data, trailheads = get_input("inputs/10_input.txt")

    print(f"Part 1: {part_one(input_data, trailheads)}")
    print(f"Part 2: {part_two(input_data, trailheads)}")
