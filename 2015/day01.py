# pylint: disable=line-too-long
"""
Day 1: Not Quite Lisp

Part 1: Determine the final floor that Santa ends up on.
Answer: 74

Part 2: Identify the position of the instruction that causes Santa to enter the basement for the first time.
Answer: 1795
"""

from utils import profiler


def get_input(file_path: str) -> str:
    """
    Reads and returns the full input from the specified file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: Contents of the file as a single string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


@profiler
def part_1(instructions: str) -> int:
    """
    Calculates the final floor based on the given instructions.

    Args:
        instructions (str): A string consisting of '(' and ')' characters.

    Returns:
        int: The resulting floor number after processing all instructions.
    """
    return instructions.count('(') - instructions.count(')')


@profiler
def part_2(instructions: str) -> int:
    """
    Determines the position of the instruction that causes Santa
    to first enter the basement (floor -1).

    Args:
        instructions (str): A string consisting of '(' and ')' characters.

    Returns:
        int: 1-based index of the instruction that first causes the floor to reach -1.
    """
    floor = 0
    for index, char in enumerate(instructions, start=1):
        floor += 1 if char == '(' else -1
        if floor == -1:
            return index
    return -1 # In case basement is never reached


if __name__ == "__main__":
    input_data  = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data )}")
    print(f"Part 2: {part_2(input_data )}")
