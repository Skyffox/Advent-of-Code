# pylint: disable=line-too-long
"""
Day 9 Challenge: Movie Theater

Part 1: Using two red tiles (our input) create an area that consists of green tiles. What is the largest area of any rectangle you can make?
Answer: 4777409595

Part 2: The green tiles can now only be contained within a loop of red/green tiles. What is the largest area of any rectangle you can make?
Answer: 1473551379
"""

from typing import List, Tuple
from shapely.geometry import Polygon
from utils import profiler


def get_input(file_path: str) -> List[Tuple[int, int]]:
    """
    This function reads the file, parses every line into a list of coordinate tuples,

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Tuple[int, int]]: A list of (x, y) coordinate tuples.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [tuple(map(int, line.strip().split(","))) for line in file]


def calc_area(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Calculates the area of a rectangle defined by two opposite corners (inclusive).

    Args:
        x1, y1 (int): Coordinates of the first corner.
        x2, y2 (int): Coordinates of the opposite corner.

    Returns:
        int: The area of the rectangle.
    """
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


@profiler
def part_one(data_input: List[Tuple[int, int]]) -> int:
    """
    Finds the maximum rectangle area from a set of coordinates using all possible pairs.

    Args:
        data_input (List[Tuple[int, int]]): List of (x, y) coordinate tuples.

    Returns:
        int: Maximum rectangle area.
    """
    max_area = 0
    for idx, (x1, y1) in enumerate(data_input):
        for x2, y2 in data_input[idx + 1:]:
            area = calc_area(x1, y1, x2, y2)
            max_area = max(max_area, area)
    return max_area


@profiler
def part_two(data_input: List[Tuple[int, int]]) -> int:
    """
    Finds the maximum rectangle area fully contained within a polygon defined by the input coordinates.

    My first approach used too much memory. I used a list to keep track of each position of red and green tiles.
    I applied a floodfill algorithm to create the area of green tiles. Then I checked each area created by a set of
    coordinates whether it only contained red or green tiles. Because of the huge size of the grid this was way too slow.

    For the second approach I tried to remove empty rows/columns so that I could still construct the areas and continue
    from there, but this approach failed.

    Then through r/adventofcode I was made aware of the shapely library, this just solved all my problems.
    Essentially this library is able to immediately create a shape from our input points and then with the .contains()
    functions we can try to fit an area into this shape. The biggest shape that fits is the winner.

    Args:
        data_input (List[Tuple[int, int]]): List of (x, y) coordinate tuples forming a polygon.

    Returns:
        int: Maximum rectangle area contained within the polygon.
    """
    red_green_area = Polygon(data_input)
    max_area = 0

    for idx, (x1, y1) in enumerate(data_input):
        for x2, y2 in data_input[idx + 1:]:
            rect = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
            if red_green_area.contains(rect):
                area = calc_area(x1, y1, x2, y2)
                max_area = max(max_area, area)

    return max_area


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
