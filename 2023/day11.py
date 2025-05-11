# pylint: disable=line-too-long
"""
Day 11: Cosmic Expansion

Part 1: Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
Answer: 10154062

Part 2: Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies.
Now, instead of the expansion you did before, make each empty row or column one million times larger.
Answer: 553083047914
"""

from typing import List, Tuple, Dict
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of strings, each representing a row in the universe grid.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[str]: List of strings representing the universe map.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.rstrip() for line in file]


def manhattan_distance(coord_a: Tuple[int, int], coord_b: Tuple[int, int]) -> int:
    """
    Calculates the Manhattan distance between two points.

    Args:
        coord_a (Tuple[int, int]): First coordinate.
        coord_b (Tuple[int, int]): Second coordinate.

    Returns:
        int: Manhattan distance.
    """
    ax, ay = coord_a
    bx, by = coord_b
    return abs(ax - bx) + abs(ay - by)


def adjust_coordinates(coord: Tuple[int, int], empty_cols: List[int], empty_rows: List[int], expansion_factor: int = 1) -> Tuple[int, int]:
    """
    Adjusts a galaxy's coordinates based on how many empty rows/columns precede it, scaled by the expansion factor.

    Args:
        coord (Tuple[int, int]): Original (x, y) coordinates.
        empty_cols (List[int]): List of indices of empty columns.
        empty_rows (List[int]): List of indices of empty rows.
        expansion_factor (int): Multiplier applied to each empty row/column. Default is 1.

    Returns:
        Tuple[int, int]: Adjusted coordinates after expansion.
    """
    x, y = coord
    x_offset = sum(1 for col in empty_cols if col < x) * expansion_factor
    y_offset = sum(1 for row in empty_rows if row < y) * expansion_factor
    return x + x_offset, y + y_offset


def find_empty_axes(data: List[str]) -> Tuple[List[int], List[int]]:
    """
    Finds the indices of all empty rows and columns in the universe map.

    Args:
        data (List[str]): The universe grid as a list of strings.

    Returns:
        Tuple[List[int], List[int]]: A tuple of empty column indices and empty row indices.
    """
    num_cols = len(data[0])
    empty_rows = []
    non_empty_cols = [False] * num_cols

    for y, row in enumerate(data):
        if '#' not in row:
            empty_rows.append(y)
        for x, char in enumerate(row):
            if char == '#':
                non_empty_cols[x] = True

    empty_cols = [x for x, filled in enumerate(non_empty_cols) if not filled]
    return empty_cols, empty_rows


def compute_total_distance(data: List[str], expansion_factor: int) -> int:
    """
    Computes the sum of Manhattan distances between all pairs of galaxies after applying expansion.

    Args:
        data (List[str]): The universe grid as a list of strings.
        expansion_factor (int): Expansion factor for empty rows and columns.

    Returns:
        int: Total Manhattan distance between all galaxy pairs.
    """
    empty_cols, empty_rows = find_empty_axes(data)
    galaxies = [(x, y) for y, row in enumerate(data) for x, char in enumerate(row) if char == '#']

    adjusted_coords: Dict[Tuple[int, int], Tuple[int, int]] = {
        galaxy: adjust_coordinates(galaxy, empty_cols, empty_rows, expansion_factor)
        for galaxy in galaxies
    }

    total_distance = 0
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            total_distance += manhattan_distance(adjusted_coords[galaxies[i]], adjusted_coords[galaxies[j]])

    return total_distance


@profiler
def part_one(data: List[str]) -> int:
    """Solves Part 1 using an expansion factor of 1."""
    return compute_total_distance(data, expansion_factor=1)


@profiler
def part_two(data: List[str]) -> int:
    """Solves Part 2 using an expansion factor of 999999."""
    return compute_total_distance(data, expansion_factor=999999)


if __name__ == "__main__":
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
