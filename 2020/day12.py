# pylint: disable=line-too-long
"""
Day 12: Rain Risk

Part 1: What is the Manhattan distance between that location and the ship's starting position?
Answer: 1457

Part 2: Almost all of the actions indicate how to move a waypoint which is relative to the ship's position.
        What is the Manhattan distance between that location and the ship's starting position?
Answer: 106860
"""

import math
from typing import List
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
        return [line.strip() for line in file.readlines()]


@profiler
def part_one(instructions: List[str]) -> int:
    """
    Navigates the ship based on the given instructions and returns the Manhattan distance.

    Args:
        instructions (list[str]): A list of navigation instructions.

    Returns:
        int: The Manhattan distance between the ship's starting position and its final position.
    """
    x, y = 0, 0     # Ship's position
    direction = 90  # Facing East

    for instruction in instructions:
        action, value = instruction[0], int(instruction[1:])
        if action == "N":
            y += value
        elif action == "S":
            y -= value
        elif action == "E":
            x += value
        elif action == "W":
            x -= value
        elif action == "L":
            direction = (direction - value) % 360
        elif action == "R":
            direction = (direction + value) % 360
        elif action == "F":
            # Move in the current direction using trigonometry
            x += round(math.cos(math.radians(direction)) * value)
            y += round(math.sin(math.radians(direction)) * value)

    return abs(x) + abs(y)


@profiler
def part_two(instructions):
    """   
    The ship starts at (0, 0), and a waypoint starts at (10, 1) relative to the ship.
    Movement instructions affect the waypoint, and 'F' moves the ship toward it.
    
    Args:
        instructions (list of str): A list of instructions like ["F10", "N3", "R90"]
    
    Returns:
        int: Manhattan distance from the starting position to the final position
    """
    sx, sy = 0, 0   # Ship's position
    wx, wy = 10, 1  # Waypoint's position

    for instruction in instructions:
        action, value = instruction[0], int(instruction[1:])
        if action == "N":
            wy += value
        elif action == "S":
            wy -= value
        elif action == "E":
            wx += value
        elif action == "W":
            wx -= value
        elif action == "L":
            # Rotate waypoint around the origin (ship's position)
            angle = math.radians(value)
            wx_new = round(math.cos(angle) * wx - math.sin(angle) * wy)
            wy = round(math.sin(angle) * wx + math.cos(angle) * wy)
            wx = wx_new
        elif action == "R":
            angle = math.radians(360 - value)
            wx_new = round(math.cos(angle) * wx - math.sin(angle) * wy)
            wy = round(math.sin(angle) * wx + math.cos(angle) * wy)
            wx = wx_new
        elif action == "F":
            # Move ship toward waypoint
            sx += wx * value
            sy += wy * value

    return abs(sx) + abs(sy)


if __name__ == "__main__":
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
