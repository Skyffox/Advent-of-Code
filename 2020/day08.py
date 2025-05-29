# pylint: disable=line-too-long
"""
Day 8: Handheld Halting

Part 1: Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?
Answer: 1930

Part 2: What is the value of the accumulator after the program terminates?
Answer: 1688
"""

from typing import List, Tuple
from utils import profiler


def load_instructions(file_path: str) -> List[Tuple[str, int]]:
    """
    Reads and parses the input file into a list of instructions.

    Each instruction is a tuple of the operation ("acc", "jmp", "nop") and its argument (integer).

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[tuple[str, int]]: A list of parsed instruction tuples.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [(line[:3], int(line[4:])) for line in file]


def execute_instructions(instructions: List[Tuple[str, int]]) -> Tuple[int, bool]:
    """
    Executes the instructions and returns the accumulator value and whether the program terminates.

    Args:
        instructions (list[tuple]): A list of instruction tuples.

    Returns:
        tuple: The accumulator value and a boolean indicating if the program terminates normally.
    """
    acc = 0
    pointer = 0
    visited = set()

    while pointer < len(instructions):
        if pointer in visited:
            return acc, False
        visited.add(pointer)
        op, arg = instructions[pointer]
        if op == "acc":
            acc += arg
            pointer += 1
        elif op == "jmp":
            pointer += arg
        else: # "nop"
            pointer += 1

    return acc, True


@profiler
def part_one(instructions: List[Tuple[str, int]]) -> int:
    """
    Finds the accumulator value just before any instruction is executed a second time.

    Args:
        instructions (list[tuple]): Parsed instructions from the input.

    Returns:
        int: The accumulator value when an infinite loop is detected.
    """
    acc, _ = execute_instructions(instructions)
    return acc


@profiler
def part_two(instructions: List[Tuple[str, int]]) -> int:
    """
    Attempts to fix the infinite loop by switching one 'jmp' to 'nop' or 'nop' to 'jmp',
    then executes the modified program. Returns the accumulator value if the program terminates.

    Args:
        instructions (list[tuple]): A list of instruction tuples.

    Returns:
        int: The accumulator value after the loop is fixed and the program terminates.
    """
    for i, (op, arg) in enumerate(instructions):
        if op == "acc":
            continue
        modified = instructions.copy()
        modified[i] = ("nop" if op == "jmp" else "jmp", arg)
        acc, terminated = execute_instructions(modified)
        if terminated:
            return acc
    return -1


if __name__ == "__main__":
    instructions_data = load_instructions("inputs/8_input.txt")

    print(f"Part 1: {part_one(instructions_data)}")
    print(f"Part 2: {part_two(instructions_data)}")
