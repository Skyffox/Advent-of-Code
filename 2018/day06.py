# pylint: disable=line-too-long
"""
Day 6: Chronal Coordinates

Part 1: What is the size of the largest area that isn't infinite?
Answer: 4398

Part 2: What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
Answer: 39560
"""

from typing import List, Tuple
from collections import defaultdict
from utils import profiler


def get_input(file_path: str) -> List[Tuple[int, int]]:
    """
    Reads the input file and returns a list of coordinates as tuples.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[tuple[int, int]]: A list of coordinates.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [tuple(map(int, line.strip().split(", "))) for line in file]


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """
    Calculates the Manhattan distance between two points.

    Args:
        p1 (tuple[int, int]): The first point.
        p2 (tuple[int, int]): The second point.

    Returns:
        int: The Manhattan distance between p1 and p2.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@profiler
def part_one(data_input: List[Tuple[int, int]]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[tuple[int, int]]): A list of coordinates.

    Returns:
        int: The size of the largest finite area.
    """
    # Determine the bounding box of the coordinates
    min_x = min(x for x, _ in data_input)
    max_x = max(x for x, _ in data_input)
    min_y = min(y for _, y in data_input)
    max_y = max(y for _, y in data_input)

    # Initialize dictionaries to track areas and infinite areas
    areas = defaultdict(int)
    infinite_areas = set()

    # Iterate over each point in the bounding box
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # Calculate the distances to all input coordinates
            distances = [manhattan_distance((x, y), coord) for coord in data_input]
            min_distance = min(distances)
            # Check if the point is closest to exactly one coordinate
            if distances.count(min_distance) == 1:
                closest_index = distances.index(min_distance)
                areas[closest_index] += 1
                # Check if the point is on the boundary (infinite area)
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    infinite_areas.add(closest_index)

    # Exclude areas that are infinite
    finite_areas = {index: area for index, area in areas.items() if index not in infinite_areas}
    # Return the size of the largest finite area
    return max(finite_areas.values(), default=0)


@profiler
def part_two(data_input: List[Tuple[int, int]], max_distance: int = 10000) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[tuple[int, int]]): A list of coordinates.
        max_distance (int): The maximum total distance to consider.

    Returns:
        int: The size of the region containing all locations which have a total distance
             to all given coordinates of less than max_distance.
    """
    # Determine the bounding box of the coordinates
    min_x = min(x for x, _ in data_input)
    max_x = max(x for x, _ in data_input)
    min_y = min(y for _, y in data_input)
    max_y = max(y for _, y in data_input)

    # Initialize a counter for the region size
    region_size = 0

    # Iterate over each point in the bounding box
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # Calculate the total distance to all input coordinates
            total_distance = sum(manhattan_distance((x, y), coord) for coord in data_input)
            # Check if the total distance is less than the maximum allowed
            if total_distance < max_distance:
                region_size += 1

    return region_size


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
