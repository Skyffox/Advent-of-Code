# pylint: disable=line-too-long
"""
Day 2: Dive

Part 1: Find out what our position is after following the commands.
Answer: 2073315

Part 2: Now there is another factor that influences our course (the aim).
Answer: 1840311528
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[List[str], int]]:
    """
    Reads the input commands from a file and returns them as a list of movement instructions.

    Args:
        file_path (str): Path to the input file containing movement instructions.

    Returns:
        List[Tuple[List[str], int]]: A list of tuples where each tuple contains a movement direction and a unit count.
    """
    instructions = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            move = line.strip().split(" ")
            units = int(move[1])
            instructions.append([move, units])

    return instructions


@profiler
def part_1(lst: List[Tuple[List[str], int]]) -> int:
    """
    Simulate the movement of the submarine based on the instructions provided.
    In Part 1, the movement is straightforward: forward increases horizontal position, 
    down and up adjust the depth.

    Args:
        lst (List[Tuple[List[str], int]]): List of movement instructions.

    Returns:
        int: The final horizontal position multiplied by the final depth.
    """
    x, y = 0, 0
    for move, units in lst:
        if move[0] == "forward":
            x += units
        elif move[0] == "down":
            y += units
        elif move[0] == "up":
            y -= units

    return x * y


@profiler
def part_2(lst: List[Tuple[List[str], int]]) -> int:
    """
    Simulate the movement of the submarine with an additional factor, the aim.
    The aim influences the depth when moving forward.

    Args:
        lst (List[Tuple[List[str], int]]): List of movement instructions.

    Returns:
        int: The final horizontal position multiplied by the final depth, considering the aim.
    """
    position, depth, aim = 0, 0, 0
    for move, units in lst:
        if move[0] == "forward":
            position += units
            depth += aim * units
        elif move[0] == "down":
            aim += units
        elif move[0] == "up":
            aim -= units

    return position * depth


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
