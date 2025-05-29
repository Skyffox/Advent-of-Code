# pylint: disable=line-too-long
"""
Day 8: I Heard You Like Registers

Part 1: What is the largest value in any register after completing the instructions in your puzzle input?
Answer: 3745

Part 2: To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide how much memory to allocate to these operations.
Answer: 4644
"""

import operator
from typing import List, Dict
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of instruction lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List of instructions.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Executes instructions and returns largest register value after completion.

    Args:
        data_input (List[str]): List of instruction strings.

    Returns:
        int: Largest value in any register after processing.
    """
    registers: Dict[str, int] = {}
    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
    }

    for line in data_input:
        parts = line.split()
        reg, op, val, _, cond_reg, cond_op, cond_val = parts
        val = int(val)
        cond_val = int(cond_val)

        if cond_reg not in registers:
            registers[cond_reg] = 0
        if reg not in registers:
            registers[reg] = 0

        if ops[cond_op](registers[cond_reg], cond_val):
            if op == 'inc':
                registers[reg] += val
            else:
                registers[reg] -= val

    return max(registers.values()) if registers else 0


@profiler
def compute(data_input: List[str]) -> int:
    """
    Executes instructions and returns highest value ever held in any register.

    Args:
        data_input (List[str]): List of instruction strings.

    Returns:
        int: Highest value ever held during processing.
    """
    registers: Dict[str, int] = {}
    ops = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
    }

    max_value = float('-inf')

    for line in data_input:
        parts = line.split()
        reg, op, val, _, cond_reg, cond_op, cond_val = parts
        val = int(val)
        cond_val = int(cond_val)

        if cond_reg not in registers:
            registers[cond_reg] = 0
        if reg not in registers:
            registers[reg] = 0

        if ops[cond_op](registers[cond_reg], cond_val):
            if op == 'inc':
                registers[reg] += val
            else:
                registers[reg] -= val
            max_value = max(max_value, *registers.values())

    return max(registers.values()), max_value


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    register_part1, register_part2 = compute(input_data)

    print(f"Part 1: {register_part1}")
    print(f"Part 2: {register_part2}")
