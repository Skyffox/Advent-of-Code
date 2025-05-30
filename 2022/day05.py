# pylint: disable=line-too-long
"""
Day 5: Supply Stacks

Part 1: After the rearrangement procedure completes, what crate ends up on top of each stack?
Answer: DHBJQJCCW

Part 2: After the rearrangement procedure completes, what crate ends up on top of each stack?
Answer: WJVRLSJJT
"""

from copy import deepcopy
from typing import List, Tuple
from utils import profiler


def get_and_parse_instructions(file_path: str) -> List[Tuple[int, int, int]]:
    """
    Reads move instructions from file and parses them.

    Args:
        file_path (str): Path to input file.

    Returns:
        List[Tuple[int, int, int]]: List of parsed instructions as
            (count, from_stack_zero_based, to_stack_zero_based).
    """
    instructions = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("move"):
                parts = [int(x) for x in line.strip().split() if x.isdigit()]
                # Convert to zero-based stack indices
                instructions.append((parts[0], parts[1] - 1, parts[2] - 1))
    return instructions


@profiler
def part_1(instructions: List[Tuple[int, int, int]], stacks: List[List[str]]) -> str:
    """
    Simulate crate moves one-by-one (reversing order when moving multiple crates).

    Args:
        instructions (List[Tuple[int, int, int]]): Move instructions.
        stacks (List[List[str]]): Initial crate stacks.

    Returns:
        str: Top crate of each stack after rearrangement.
    """
    for count, from_idx, to_idx in instructions:
        for _ in range(count):
            crate = stacks[from_idx].pop()
            stacks[to_idx].append(crate)

    return "".join(stack[-1] for stack in stacks if stack)


@profiler
def part_2(instructions: List[Tuple[int, int, int]], stacks: List[List[str]]) -> str:
    """
    Simulate crate moves in bulk, preserving their original order.

    Moves crates all at once from source to destination stack,
    keeping the order of the crates intact (no reversing).

    Args:
        instructions (List[Tuple[int, int, int]]): Move instructions.
        stacks (List[List[str]]): Initial crate stacks.

    Returns:
        str: Top crate of each stack after rearrangement.
    """
    for count, from_idx, to_idx in instructions:
        # Slice the last 'count' crates from the source stack
        crates_to_move = stacks[from_idx][-count:]
        # Append them all at once to the destination stack
        stacks[to_idx].extend(crates_to_move)
        # Remove the moved crates from the source stack
        stacks[from_idx] = stacks[from_idx][:-count]

    return "".join(stack[-1] for stack in stacks if stack)


if __name__ == "__main__":
    input_data = get_and_parse_instructions("inputs/5_input.txt")

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
