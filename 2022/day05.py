# pylint: disable=line-too-long
"""
Day 5: Supply Stacks

Part 1: After the rearrangement procedure completes, what crate ends up on top of each stack?
Answer: DHBJQJCCW

Part 2: After the rearrangement procedure completes, what crate ends up on top of each stack?
Answer: WJVRLSJJT
"""

from copy import deepcopy
from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Read input lines from file.

    Args:
        file_path (str): Path to input file.

    Returns:
        List[str]: Lines from the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


def parse_move_instruction(line: str) -> tuple[int, int, int]:
    """
    Extract number of crates to move, source stack index, and destination stack index.

    Args:
        line (str): Instruction line.

    Returns:
        tuple[int, int, int]: (count, from_stack, to_stack)
    """
    parts = [int(x) for x in line.strip().split() if x.isdigit()]
    return parts[0], parts[1] - 1, parts[2] - 1  # adjust to 0-based index


@profiler
def part_1(instructions: List[str], stacks: List[List[str]]) -> str:
    """
    Simulate crate moves one-by-one (reversing order when moving multiple crates).

    Args:
        instructions (List[str]): Move instructions.
        stacks (List[List[str]]): Initial crate stacks.

    Returns:
        str: Top crate of each stack after rearrangement.
    """
    for line in instructions:
        if line.startswith("move"):
            count, from_idx, to_idx = parse_move_instruction(line)
            for _ in range(count):
                crate = stacks[from_idx].pop()
                stacks[to_idx].append(crate)

    return "".join(stack[-1] for stack in stacks)


@profiler
def part_2(instructions: List[str], stacks: List[List[str]]) -> str:
    """
    Simulate crate moves in bulk, preserving their original order.

    Args:
        instructions (List[str]): Move instructions.
        stacks (List[List[str]]): Initial crate stacks.

    Returns:
        str: Top crate of each stack after rearrangement.
    """
    for line in instructions:
        if line.startswith("move"):
            count, from_idx, to_idx = parse_move_instruction(line)
            crates_to_move = stacks[from_idx][-count:]
            stacks[to_idx].extend(crates_to_move)
            stacks[from_idx] = stacks[from_idx][:-count]

    return "".join(stack[-1] for stack in stacks)


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    initial_stacks = [
        ["F", "C", "P", "G", "Q", "R"],
        ["W", "T", "C", "P"],
        ["B", "H", "P", "M", "C"],
        ["L", "T", "Q", "S", "M", "P", "R"],
        ["P", "H", "J", "Z", "V", "G", "N"],
        ["D", "P", "J"],
        ["L", "G", "P", "Z", "F", "J", "T", "R"],
        ["N", "L", "H", "C", "F", "P", "T", "J"],
        ["G", "V", "Z", "Q", "H", "T", "C", "W"]
    ]

    print(f"Part 1: {part_1(input_data, deepcopy(initial_stacks))}")
    print(f"Part 2: {part_2(input_data, deepcopy(initial_stacks))}")
