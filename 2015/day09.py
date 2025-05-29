# pylint: disable=line-too-long
"""
Day 9: All in a Single Night

Part 1: What is the distance of the shortest route?
Answer: 251

Part 2: What is the distance of the longest route?
Answer: 898
"""

from typing import List, Dict, Tuple
import itertools
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def parse_distances(data: List[str]) -> Dict[Tuple[str, str], int]:
    """
    Parses distance instructions into a dictionary of location pairs and distances.

    Args:
        data (List[str]): List of strings in the form "A to B = 42".

    Returns:
        Dict[Tuple[str, str], int]: Mapping of (location1, location2) to distance.
    """
    distances = {}
    for line in data:
        parts = line.split()
        loc1, loc2, dist = parts[0], parts[2], int(parts[4])
        distances[(loc1, loc2)] = dist
        distances[(loc2, loc1)] = dist # Since distances are bidirectional
    return distances


def get_locations(distances: Dict[Tuple[str, str], int]) -> List[str]:
    """
    Returns a list of all unique locations from the distance dictionary.

    Args:
        distances (Dict[Tuple[str, str], int]): Distance mapping.

    Returns:
        List[str]: List of unique city names.
    """
    locations = set()
    for a, b in distances:
        locations.add(a)
        locations.add(b)
    return list(locations)


def route_distance(route: List[str], distances: Dict[Tuple[str, str], int]) -> int:
    """
    Calculates the total distance of a given route.

    Args:
        route (List[str]): Ordered list of locations.
        distances (Dict[Tuple[str, str], int]): Distance mapping.

    Returns:
        int: Total distance of the route.
    """
    return sum(distances[(route[i], route[i + 1])] for i in range(len(route) - 1))


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Finds the shortest route that visits every location once.

    Args:
        data_input (List[str]): A list of input lines.

    Returns:
        int: The minimum total distance of any valid route.
    """
    distances = parse_distances(data_input)
    locations = get_locations(distances)

    return min(route_distance(p, distances) for p in itertools.permutations(locations))


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds the longest route that visits every location once.

    Args:
        data_input (List[str]): A list of input lines.

    Returns:
        int: The maximum total distance of any valid route.
    """
    distances = parse_distances(data_input)
    locations = get_locations(distances)

    return max(route_distance(p, distances) for p in itertools.permutations(locations))


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
