# pylint: disable=line-too-long
"""
Day 11: Hex Ed

Part 1: Determine the fewest number of steps required to reach the child.
Answer: 707

Part 2: How many steps away is the furthest he ever got from his starting position?
Answer: 1442
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of steps in the hex grid.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of directions as strings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        line = file.readline().strip()
        return line.split(',')


def hex_distance(x: int, y: int, z: int) -> int:
    """
    Computes distance from origin in cube coordinates for hex grid.

    Args:
        x (int): x coordinate.
        y (int): y coordinate.
        z (int): z coordinate.

    Returns:
        int: Distance from origin.
    """
    return max(abs(x), abs(y), abs(z))


@profiler
def compute(data_input: List[str]) -> int:
    """
    Computes shortest path distance from origin after following steps.
    Computes the furthest distance from origin during the path.

    Args:
        data_input (List[str]): List of directions.

    Returns:
        int: Distance from origin.
        int: Furthest distance reached.
    """
    x = y = z = 0
    max_dist = 0

    for step in data_input:
        if step == 'n':
            y += 1
            z -= 1
        elif step == 'ne':
            x += 1
            z -= 1
        elif step == 'se':
            x += 1
            y -= 1
        elif step == 's':
            y -= 1
            z += 1
        elif step == 'sw':
            x -= 1
            z += 1
        elif step == 'nw':
            x -= 1
            y += 1

        max_dist = max(hex_distance(x, y, z), max_dist)

    return hex_distance(x, y, z), max_dist


if __name__ == "__main__":
    input_data = get_input("inputs/11_input.txt")

    fewest_steps, max_distance = compute(input_data)

    print(f"Part 1: {fewest_steps}")
    print(f"Part 2: {max_distance}")
