# pylint: disable=line-too-long
"""
Day 05: Sunny with a Chance of Asteroids

Part 1: After providing 1 to the only input instruction and passing all the tests, what diagnostic code does the program produce?
Answer: 4511442

Part 2: What is the diagnostic code for system ID 5?
Answer: 12648139
"""

from typing import List
from utils import IntcodeComputer
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns the Intcode program as a list of integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: The Intcode program.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip().split(",")))


@profiler
def part_one(program: List[str]) -> int:
    """
    Runs the Intcode program with input value 1 and returns the diagnostic code.

    Args:
        program (List[int]): Intcode program.

    Returns:
        int: Diagnostic code output.
    """
    computer = IntcodeComputer(program.copy())
    computer.add_input(1) # System ID for part 1
    output = None
    while not computer.halted:
        val = computer.run()
        if val is not None:
            output = val # Last output value before halt
    return output


@profiler
def part_two(program: List[int]) -> int:
    """
    Runs the Intcode program with input value 5 and returns the diagnostic code.

    Args:
        program (List[int]): Intcode program.

    Returns:
        int: Diagnostic code output.
    """
    computer = IntcodeComputer(program.copy())
    computer.add_input(5) # System ID for part 2
    output = None
    while not computer.halted:
        val = computer.run()
        if val is not None:
            output = val
    return output


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
