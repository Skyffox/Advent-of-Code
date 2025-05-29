# pylint: disable=line-too-long
"""
Day 06: Universal Orbit Map

Part 1: What is the total number of direct and indirect orbits in your map data?
Answer: 270768

Part 2: What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? 
        (Between the objects they are orbiting - not between YOU and SAN.)
Answer: 451
"""

from typing import List, Dict
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
        return [line.strip() for line in file if line.strip()]


def build_orbit_map(pairs: List[str]) -> Dict[str, str]:
    """
    Builds a dictionary representing the orbit map.

    Args:
        pairs (List[str]): A list of orbit relationships in the form "A)B".

    Returns:
        Dict[str, str]: A map from object to the object it orbits.
    """
    orbit_map = {}
    for pair in pairs:
        center, orbiter = pair.split(")")
        orbit_map[orbiter] = center
    return orbit_map


def count_orbits(orbit_map: Dict[str, str]) -> int:
    """
    Counts total direct and indirect orbits.

    Args:
        orbit_map (Dict[str, str]): The orbit relationships.

    Returns:
        int: The total number of orbits.
    """
    total = 0
    for obj in orbit_map:
        while obj in orbit_map:
            obj = orbit_map[obj]
            total += 1
    return total


def get_orbit_path(orbit_map: Dict[str, str], start: str) -> List[str]:
    """
    Returns the list of objects from the given start object to the root ("COM").

    Args:
        orbit_map (Dict[str, str]): The orbit relationships.
        start (str): The starting object.

    Returns:
        List[str]: Path from start to COM.
    """
    path = []
    while start in orbit_map:
        start = orbit_map[start]
        path.append(start)
    return path


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    orbit_map = build_orbit_map(data_input)
    return count_orbits(orbit_map)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two.
    """
    orbit_map = build_orbit_map(data_input)
    path_you = get_orbit_path(orbit_map, "YOU")
    path_san = get_orbit_path(orbit_map, "SAN")

    # Find the first common ancestor
    common = set(path_you) & set(path_san)
    transfers = min(path_you.index(obj) + path_san.index(obj) for obj in common)
    return transfers


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
