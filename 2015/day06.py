# pylint: disable=line-too-long
"""
Day 6: Probably a Fire Hazard

Part 1: After following the instructions, how many lights are lit?
Answer: 543903

Part 2: What is the total brightness of all lights combined after following Santa's instructions?
Answer: 14687245
"""

from typing import List, Tuple
import re
from utils import profiler


def get_input(file_path: str) -> List[Tuple[str, int, int, int, int]]:
    """
    Reads the input file and parses each line into a tuple of action and coordinates.

    Each instruction line is parsed into:
        - action (str): One of 'on', 'off', or 'toggle'
        - x1, y1, x2, y2 (int): Coordinates of the rectangular region

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Tuple[str, int, int, int, int]]: A list of parsed instructions.
    """
    pattern = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
    instructions = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            match = re.match(pattern, line)
            if not match:
                raise ValueError(f"Invalid instruction line: {line}")
            action = match.group(1).replace("turn ", "")
            x1, y1, x2, y2 = map(int, match.groups()[1:])
            instructions.append((action, x1, y1, x2, y2))

    return instructions


@profiler
def part_one(data_input: List[str]) -> int:
    """
    The grid is a 1000x1000 array of boolean values, where each light is either ON (True) or OFF (False).
    Instructions modify the grid as follows:
        - "turn on" sets lights in the region to ON,
        - "turn off" sets lights in the region to OFF,
        - "toggle" inverts the state of each light in the region.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The total number of lights that are ON after executing all instructions.
    """
    grid = [[False] * 1000 for _ in range(1000)]

    for action, x1, y1, x2, y2 in data_input:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if action == "on":
                    grid[x][y] = True
                elif action == "off":
                    grid[x][y] = False
                elif action == "toggle":
                    grid[x][y] = not grid[x][y]

    return sum(sum(row) for row in grid)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    The grid is a 1000x1000 array of integers representing brightness levels of lights.
    Instructions modify the brightness as follows:
        - "turn on" increases brightness by 1,
        - "turn off" decreases brightness by 1, to a minimum of 0,
        - "toggle" increases brightness by 2.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The total brightness of all lights after executing all instructions.
    """
    grid = [[0] * 1000 for _ in range(1000)]

    for action, x1, y1, x2, y2 in data_input:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if action == "on":
                    grid[x][y] += 1
                elif action == "off":
                    grid[x][y] = max(0, grid[x][y] - 1)
                elif action == "toggle":
                    grid[x][y] += 2

    return sum(sum(row) for row in grid)


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
