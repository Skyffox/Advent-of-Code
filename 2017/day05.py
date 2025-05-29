# pylint: disable=line-too-long
"""
Day 5: A Maze of Twisty Trampolines, All Alike

Part 1: How many steps does it take to reach the exit?
Answer: 373543

Part 2: How many steps does it now take to reach the exit?
Answer: 27502966
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Jumps are relative: -1 moves to the previous instruction, and 2 skips the next one. 
    Start at the first instruction in the list. The goal is to follow the jumps until one leads outside the list.

    In addition, these instructions are a little strange; after each jump, the offset of that instruction increases by 1. 
    So, if you come across an offset of 3, you would move three instructions forward, but change it to a 4 for the next time it is encountered.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: List of jump offsets.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Counts steps to exit the list following the jumping rules for part one.
    Now, the jumps are even stranger: after each jump, if the offset was three or more, 
    instead decrease it by 1. Otherwise, increase it by 1 as before.

    Args:
        data_input (List[int]): List of jump offsets.

    Returns:
        int: Number of steps to exit the list.
    """
    jumps = data_input.copy()
    steps = 0
    index = 0

    while 0 <= index < len(jumps):
        jump = jumps[index]
        jumps[index] += 1
        index += jump
        steps += 1

    return steps


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Counts steps to exit the list with modified jumping rules for part two.

    Args:
        data_input (List[int]): List of jump offsets.

    Returns:
        int: Number of steps to exit the list.
    """
    jumps = data_input.copy()
    steps = 0
    index = 0

    while 0 <= index < len(jumps):
        jump = jumps[index]
        if jump >= 3:
            jumps[index] -= 1
        else:
            jumps[index] += 1
        index += jump
        steps += 1

    return steps


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
