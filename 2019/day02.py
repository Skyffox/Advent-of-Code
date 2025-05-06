# pylint: disable=line-too-long
"""
Day 2: 1202 Program Alarm

Part 1: What value is left at position 0 after the program halts?  
Answer: 3790645

Part 2: Find noun and verb that result in output 19690720.  
Answer: 6577
"""

from typing import List
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


def run_program(instructions: List[int], noun: int = None, verb: int = None) -> int:
    """
    Simulate the intcode program.

    Args:
        instructions (List[int]): Program memory.
        noun (int, optional): Override value at position 1.
        verb (int, optional): Override value at position 2.

    Returns:
        int: Value at position 0 after program halts.
    """
    memory = instructions.copy()
    if noun is not None:
        memory[1] = noun
    if verb is not None:
        memory[2] = verb

    ip = 0 # Instruction pointer
    while True:
        opcode = memory[ip]
        if opcode == 99:
            break
        a, b, c = memory[ip + 1], memory[ip + 2], memory[ip + 3]

        if opcode == 1:
            memory[c] = memory[a] + memory[b]
        elif opcode == 2:
            memory[c] = memory[a] * memory[b]
        else:
            raise ValueError(f"Unknown opcode {opcode} at position {ip}")
        ip += 4

    return memory[0]


@profiler
def part_1(instructions: List[int]) -> int:
    """
    Run the Intcode program with fixed noun and verb.

    Args:
        instructions (List[int]): The Intcode program.

    Returns:
        int: Output at position 0 after execution.
    """
    return run_program(instructions, noun=12, verb=2)


@profiler
def part_2(instructions: List[int]) -> int:
    """
    Brute-force search for noun and verb that cause the program to produce the target output.

    Args:
        instructions (List[int]): The Intcode program.

    Returns:
        int: 100 * noun + verb that produces the target output.
    """
    target = 19690720
    for noun in range(100):
        for verb in range(100):
            if run_program(instructions, noun, verb) == target:
                return 100 * noun + verb


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
