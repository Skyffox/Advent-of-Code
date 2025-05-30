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
    Reads a list of integer jump offsets from a file.

    Each integer represents a relative jump offset in a list of instructions.
    Starting at the first instruction (index 0), these offsets determine
    how to move through the list by adding the offset to the current index.

    Args:
        file_path (str): Path to the input file containing one integer offset per line.

    Returns:
        List[int]: List of integer offsets representing jump instructions.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Simulates following jump offsets through the list until moving outside it,
    counting the number of steps taken.

    Rules:
    - Begin at index 0.
    - At each step, read the current jump offset.
    - Move forward or backward by the offset value.
    - After the jump, increment the offset at the previous position by 1.
    - Repeat until the current position moves outside the list bounds.

    Args:
        data_input (List[int]): Initial list of jump offsets.

    Returns:
        int: The total number of steps taken to exit the list.
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
    Simulates following jump offsets through the list with modified update rules,
    counting steps until exiting the list.

    Modified rules differ from part one:
    - Begin at index 0.
    - At each step, read the current jump offset.
    - Move forward or backward by the offset value.
    - After the jump:
        - If the original offset was 3 or more, decrease it by 1.
        - Otherwise, increase it by 1.
    - Repeat until the current position moves outside the list bounds.

    Args:
        data_input (List[int]): Initial list of jump offsets.

    Returns:
        int: The total number of steps taken to exit the list.
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
