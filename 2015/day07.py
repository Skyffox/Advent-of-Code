# pylint: disable=line-too-long
"""
Day 7: Some Assembly Required

Part 1: In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire a?
Answer: 16076

Part 2: Now, take the signal you got on wire a, override wire b to that signal, and reset the other wires (including wire a). What new signal is ultimately provided to wire a?
Answer: 2797
"""

from typing import Dict
from utils import profiler


def get_input(file_path: str) -> Dict[str, str]:
    """
    Reads the input file and parses circuit instructions into a dictionary mapping wire names to expressions.

    Each line has the format: 'expression -> wire'
    For example: '123 -> x' or 'x AND y -> z'

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[str, str]: A dictionary mapping each wire to its logic expression.
    """
    instructions = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            expr, wire = line.strip().split(" -> ")
            instructions[wire] = expr
    return instructions


def get_value(wire: str, instructions: Dict[str, str], cache: Dict[str, int]) -> int:
    """
    Recursively evaluates the 16-bit signal provided to a wire, using memoization.

    Args:
        wire (str): The wire to evaluate.
        instructions (Dict[str, str]): Mapping of wires to logic expressions.
        cache (Dict[str, int]): A memoization cache to store evaluated wire values.

    Returns:
        int: The computed signal value for the given wire.
    """
    if wire.isdigit():
        return int(wire)

    if wire in cache:
        return cache[wire]

    expr = instructions[wire]
    tokens = expr.split()

    if len(tokens) == 1:
        val = get_value(tokens[0], instructions, cache)
    elif len(tokens) == 2:  # NOT x
        val = ~get_value(tokens[1], instructions, cache) & 0xFFFF
    elif len(tokens) == 3:
        a, op, b = tokens
        if op == "AND":
            val = get_value(a, instructions, cache) & get_value(b, instructions, cache)
        elif op == "OR":
            val = get_value(a, instructions, cache) | get_value(b, instructions, cache)
        elif op == "LSHIFT":
            val = get_value(a, instructions, cache) << int(b)
        elif op == "RSHIFT":
            val = get_value(a, instructions, cache) >> int(b)
        else:
            raise ValueError(f"Unknown operation: {op}")
    else:
        raise ValueError(f"Unrecognized expression: {expr}")

    cache[wire] = val & 0xFFFF
    return cache[wire]


@profiler
def part_one(instructions: Dict[str, str]) -> int:
    """
    Evaluates the final signal provided to wire 'a' by recursively computing
    the logic circuit defined by the input instructions.

    Args:
        instructions (Dict[str, str]): Mapping of wire names to logic expressions.

    Returns:
        int: The signal ultimately provided to wire 'a'.
    """
    return get_value("a", instructions, {})


@profiler
def part_two(instructions: Dict[str, str]) -> int:
    """
    First, computes the value of wire 'a' from the original instructions.
    Then, overrides the value of wire 'b' with that result, resets the cache,
    and re-evaluates wire 'a'.

    Args:
        instructions (Dict[str, str]): Mapping of wire names to logic expressions.

    Returns:
        int: The new signal provided to wire 'a' after overriding wire 'b'.
    """
    override = get_value("a", instructions, {})
    cache = {"b": override}
    return get_value("a", instructions, cache)


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
