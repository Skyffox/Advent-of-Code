# pylint: disable=line-too-long
"""
Day 2: 1202 Program Alarm

Part 1: What value is left at position 0 after the program halts?  
Answer: 3790645

Part 2: Find noun and verb that result in output 19690720.  
Answer: 6577
"""

from typing import List
from utils import IntcodeComputer
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Parse comma-separated integers from file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[int]: List of integers representing the program.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.readline().strip().split(",")))


def run_program_with_inputs(program: List[int], noun: int, verb: int) -> int:
    """
    Runs an Intcode program with the provided noun and verb values,
    returning the value at position 0 after execution.

    Args:
        program (List[int]): The initial state of the Intcode program (memory).
        noun (int): The value to insert at position 1 in the program.
        verb (int): The value to insert at position 2 in the program.

    Returns:
        int: The value at position 0 of the program after it halts.
    """
    memory = program.copy()
    memory[1] = noun
    memory[2] = verb
    computer = IntcodeComputer(memory)

    while not computer.halted:
        computer.run()

    return computer.memory[0]


@profiler
def part_1(program: List[int]) -> int:
    """
    Run the Intcode program with fixed noun and verb.

    Args:
        program (List[int]): The Intcode program.

    Returns:
        int: Output at position 0 after execution.
    """
    return run_program_with_inputs(program, 12, 2)


@profiler
def part_2(program: List[int], target: int = 19690720) -> int:
    """
    Brute-force search for noun and verb that cause the program to produce the target output.

    Args:
        program (List[int]): The Intcode program.

    Returns:
        int: 100 * noun + verb that produces the target output.
    """
    for noun in range(100):
        for verb in range(100):
            output = run_program_with_inputs(program, noun, verb)
            if output == target:
                return 100 * noun + verb
    return None  # Not found


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
