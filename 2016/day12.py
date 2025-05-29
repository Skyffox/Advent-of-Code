# pylint: disable=line-too-long
"""
Day 12: Leonardo's Monorail

Part 1: After executing the assembunny code in your puzzle input, what value is left in register a?
Answer: 317993

Part 2: If you instead initialize register c to be 1, what value is now left in register a?
Answer: 9227647
"""

from typing import List, Dict
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of instructions.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: List of instructions.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def run_program(instructions: List[str], initial_registers: Dict[str, int]) -> Dict[str, int]:
    """
    Runs the assembly-like program with the given initial registers.

    Args:
        instructions (List[str]): List of instructions.
        initial_registers (Dict[str, int]): Initial register values.

    Returns:
        Dict[str, int]: Final register values after program execution.
    """
    registers = initial_registers.copy()
    pc = 0  # program counter

    def val(x: str) -> int:
        if x.lstrip('-').isdigit():
            return int(x)
        return registers.get(x, 0)

    while 0 <= pc < len(instructions):
        parts = instructions[pc].split()
        cmd = parts[0]

        if cmd == 'cpy':
            x, y = parts[1], parts[2]
            if y in registers:
                registers[y] = val(x)
            pc += 1
        elif cmd == 'inc':
            x = parts[1]
            if x in registers:
                registers[x] += 1
            pc += 1
        elif cmd == 'dec':
            x = parts[1]
            if x in registers:
                registers[x] -= 1
            pc += 1
        elif cmd == 'jnz':
            x, y = parts[1], parts[2]
            if val(x) != 0:
                pc += val(y)
            else:
                pc += 1
        else:
            pc += 1

    return registers


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Runs the program with all registers initially zero.

    Args:
        data_input (List[str]): List of instructions.

    Returns:
        int: Value in register 'a' after execution.
    """
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    final_regs = run_program(data_input, registers)
    return final_regs['a']


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Runs the program with register 'c' initially set to 1.

    Args:
        data_input (List[str]): List of instructions.

    Returns:
        int: Value in register 'a' after execution.
    """
    registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    final_regs = run_program(data_input, registers)
    return final_regs['a']


if __name__ == "__main__":
    input_data = get_input("inputs/12_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
