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


def get_input(file_path: str) -> Dict[Tuple[str, str], int]:
    """
    Parses a distance map from the input file, where each line is formatted like:
        "A to B = 42"

    Distances are bidirectional, so both (A, B) and (B, A) are added.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[Tuple[str, str], int]: Dictionary mapping location pairs to distances.
    """
    distances = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            loc1, loc2, dist = parts[0], parts[2], int(parts[4])
            distances[(loc1, loc2)] = dist
            distances[(loc2, loc1)] = dist
    return distances


def get_locations(distances: Dict[Tuple[str, str], int]) -> List[str]:
    """
    Extracts all unique locations from the distance mapping.

    Args:
        distances (Dict[Tuple[str, str], int]): Dictionary of bidirectional distances.

    Returns:
        List[str]: List of unique location names.
    """
    locations = set()
    for a, b in distances:
        locations.add(a)
        locations.add(b)
    return list(locations)


def route_distance(route: List[str], distances: Dict[Tuple[str, str], int]) -> int:
    """
    Computes the total distance for a given travel route.

    Args:
        route (List[str]): Ordered list of locations in the route.
        distances (Dict[Tuple[str, str], int]): Mapping of location pairs to distances.

    Returns:
        int: The total travel distance of the route.
    """
    return sum(distances[(route[i], route[i + 1])] for i in range(len(route) - 1))


@profiler
def part_one(distances: Dict[Tuple[str, str], int]) -> int:
    """
    Finds the shortest route that visits every location exactly once using brute-force
    permutation of all possible paths.

    Args:
        distances (Dict[Tuple[str, str], int]): Distance mapping between all location pairs.

    Returns:
        int: The shortest possible route distance.
    """
    locations = get_locations(distances)
    return min(route_distance(p, distances) for p in itertools.permutations(locations))


@profiler
def part_two(distances: Dict[Tuple[str, str], int]) -> int:
    """
    Finds the longest route that visits every location exactly once using brute-force
    permutation of all possible paths.

    Args:
        distances (Dict[Tuple[str, str], int]): Distance mapping between all location pairs.

    Returns:
        int: The longest possible route distance.
    """
    locations = get_locations(distances)
    return max(route_distance(p, distances) for p in itertools.permutations(locations))


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
