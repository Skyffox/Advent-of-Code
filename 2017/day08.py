# pylint: disable=line-too-long
"""
Day 8: I Heard You Like Registers

Part 1: What is the largest value in any register after completing the instructions?
Answer: 3745

Part 2: What is the highest value held in any register during the process?
Answer: 4644
"""

import operator
from typing import List, Tuple, Dict
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
def run_instructions(data_input: List[str]) -> Tuple[int, int]:
    """
    Executes instructions and returns:
      - The largest value in any register after completion.
      - The highest value ever held in any register during processing.

    Args:
        data_input (List[str]): List of instruction strings.

    Returns:
        Tuple[int, int]: (largest final register value, highest value during execution)
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

    max_value_ever = float('-inf')

    for line in data_input:
        reg, op, val, _, cond_reg, cond_op, cond_val = line.split()
        val = int(val)
        cond_val = int(cond_val)

        # Initialize registers if not seen
        registers.setdefault(cond_reg, 0)
        registers.setdefault(reg, 0)

        if ops[cond_op](registers[cond_reg], cond_val):
            if op == 'inc':
                registers[reg] += val
            else:
                registers[reg] -= val

            # Track highest value ever seen
            max_value_ever = max(max_value_ever, registers[reg])

    largest_final_value = max(registers.values()) if registers else 0
    return largest_final_value, max_value_ever


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    part1_result, part2_result = run_instructions(input_data)

    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")
