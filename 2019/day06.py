# pylint: disable=line-too-long
"""
Day 06: Universal Orbit Map

Part 1: What is the total number of direct and indirect orbits in your map data?
Answer: 270768

Part 2: What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? 
        (Between the objects they are orbiting - not between YOU and SAN.)
Answer: 451
"""

from typing import Dict, List
from utils import profiler


def load_orbit_map(file_path: str) -> Dict[str, str]:
    """
    Reads the input file, parses orbit pairs, and builds the orbit map.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[str, str]: A map from object to the object it orbits.
    """
    orbit_map = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            center, orbiter = line.split(")")
            orbit_map[orbiter] = center
    return orbit_map


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
def part_one(orbit_map: Dict[str, str]) -> int:
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


@profiler
def part_two(orbit_map: Dict[str, str]) -> int:
    """
    Calculates the minimum number of orbital transfers required to move from the object 
    YOU are orbiting to the object SAN is orbiting.

    The function finds the paths from YOU and SAN to the root object ("COM"), identifies 
    their common ancestors, and determines the shortest combined distance to a shared 
    orbiting object.

    Args:
        orbit_map (Dict[str, str]): A dictionary mapping each orbiting object to the object 
                                    it orbits.

    Returns:
        int: The minimum number of orbital transfers needed between YOU's and SAN's orbits.
    """
    path_you = get_orbit_path(orbit_map, "YOU")
    path_san = get_orbit_path(orbit_map, "SAN")

    # Find the first common ancestor
    common = set(path_you) & set(path_san)
    transfers = min(path_you.index(obj) + path_san.index(obj) for obj in common)
    return transfers


if __name__ == "__main__":
    input_data = load_orbit_map("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
