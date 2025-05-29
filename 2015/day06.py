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


def parse_instruction(line: str) -> Tuple[str, int, int, int, int]:
    """
    Parses a line of the input into an instruction and coordinates.

    Args:
        line (str): The input instruction line.

    Returns:
        tuple[str, int, int, int, int]: Action ('on', 'off', 'toggle') and coordinates (x1, y1, x2, y2).
    """
    pattern = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
    match = re.match(pattern, line)
    if not match:
        raise ValueError(f"Invalid instruction line: {line}")
    action = match.group(1).replace("turn ", "")
    x1, y1, x2, y2 = map(int, match.groups()[1:])
    return action, x1, y1, x2, y2


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    grid = [[False] * 1000 for _ in range(1000)]

    for line in data_input:
        action, x1, y1, x2, y2 = parse_instruction(line)
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
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two.
    """
    grid = [[0] * 1000 for _ in range(1000)]

    for line in data_input:
        action, x1, y1, x2, y2 = parse_instruction(line)
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
