# pylint: disable=line-too-long
"""
Day 17: Conway Cubes

Part 1: Starting with your given initial configuration, simulate six cycles. 
        How many cubes are left in the active state after the sixth cycle?
Answer: 276

Part 2: Starting with your given initial configuration, simulate six cycles in a 4-dimensional space. 
        How many cubes are left in the active state after the sixth cycle?
Answer: 2136
"""

from typing import List, Tuple, Set, Dict
from utils import profiler


def get_input(file_path: str) -> Tuple[Set[Tuple[int, int, int]], Set[Tuple[int, int, int, int]]]:
    """
    Parses the input file and returns the initial active cubes for both 3D and 4D simulations.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple containing:
            - Set of active 3D coordinates (x, y, z=0)
            - Set of active 4D coordinates (x, y, z=0, w=0)
    """
    active_3d = set()
    active_4d = set()

    with open(file_path, "r", encoding="utf-8") as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line.strip()):
                if ch == "#":
                    active_3d.add((x, y, 0))
                    active_4d.add((x, y, 0, 0))

    return active_3d, active_4d


def neighbors_3d(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    """
    Generates all 26 neighboring coordinates for a given 3D point.

    Args:
        x, y, z (int): Coordinates.

    Returns:
        List of neighboring 3D coordinates.
    """
    return [
        (x + dx, y + dy, z + dz)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
        if not (dx == dy == dz == 0)
    ]


def neighbors_4d(x: int, y: int, z: int, w: int) -> List[Tuple[int, int, int, int]]:
    """
    Generates all 80 neighboring coordinates for a given 4D point.

    Args:
        x, y, z, w (int): Coordinates.

    Returns:
        List of neighboring 4D coordinates.
    """
    return [
        (x + dx, y + dy, z + dz, w + dw)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
        for dw in (-1, 0, 1)
        if not (dx == dy == dz == dw == 0)
    ]


def run_cycle_3d(active: Set[Tuple[int, int, int]]) -> Set[Tuple[int, int, int]]:
    """
    Runs one cycle of the 3D Conway Cubes simulation.

    Args:
        active: Set of active 3D cube coordinates.

    Returns:
        Updated set of active 3D coordinates after one cycle.
    """
    counts: Dict[Tuple[int, int, int], int] = {}

    for cube in active:
        for neighbor in neighbors_3d(*cube):
            counts[neighbor] = counts.get(neighbor, 0) + 1

    return {cube for cube, count in counts.items() if count == 3 or (count == 2 and cube in active)}


def run_cycle_4d(active: Set[Tuple[int, int, int, int]]) -> Set[Tuple[int, int, int, int]]:
    """
    Runs one cycle of the 4D Conway Cubes simulation.

    Args:
        active: Set of active 4D cube coordinates.

    Returns:
        Updated set of active 4D coordinates after one cycle.
    """
    counts: Dict[Tuple[int, int, int, int], int] = {}

    for cube in active:
        for neighbor in neighbors_4d(*cube):
            counts[neighbor] = counts.get(neighbor, 0) + 1

    return {cube for cube, count in counts.items() if count == 3 or (count == 2 and cube in active)}


@profiler
def part_one(active_3d: Set[Tuple[int, int, int]]) -> int:
    """
    Runs the 3D Conway Cubes simulation for 6 cycles and counts active cubes.

    Args:
        active_3d: Initial set of active 3D coordinates.

    Returns:
        Number of active cubes after 6 cycles.
    """
    for _ in range(6):
        active_3d = run_cycle_3d(active_3d)
    return len(active_3d)


@profiler
def part_two(active_4d: Set[Tuple[int, int, int, int]]) -> int:
    """
    Runs the 4D Conway Cubes simulation for 6 cycles and counts active cubes.

    Args:
        active_4d: Initial set of active 4D coordinates.

    Returns:
        Number of active cubes after 6 cycles.
    """
    for _ in range(6):
        active_4d = run_cycle_4d(active_4d)
    return len(active_4d)


if __name__ == "__main__":
    initial_active_3d, initial_active_4d = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_one(initial_active_3d)}")
    print(f"Part 2: {part_two(initial_active_4d)}")