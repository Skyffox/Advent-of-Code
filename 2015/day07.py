# pylint: disable=line-too-long
"""
Day 7: Some Assembly Required

Part 1: In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire a?
Answer: 16076

Part 2: Now, take the signal you got on wire a, override wire b to that signal, and reset the other wires (including wire a). What new signal is ultimately provided to wire a?
Answer: 2797
"""

from typing import List, Dict
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: A list of lines with leading/trailing whitespace removed.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def parse_instructions(lines: List[str]) -> Dict[str, str]:
    """
    Parses circuit instructions into a dictionary mapping wire names to expressions.

    Args:
        lines (List[str]): List of raw instruction strings.

    Returns:
        Dict[str, str]: Mapping from wire name to logic expression.
    """
    instructions = {}
    for line in lines:
        expr, wire = line.split(" -> ")
        instructions[wire] = expr
    return instructions


def get_value(wire: str, instructions: Dict[str, str], cache: Dict[str, int]) -> int:
    """
    Recursively evaluates the value of a wire.

    Args:
        wire (str): The wire to evaluate.
        instructions (Dict[str, str]): Dictionary of wire instructions.
        cache (Dict[str, int]): Memoization cache for wire values.

    Returns:
        int: The evaluated 16-bit signal of the wire.
    """
    if wire.isdigit():
        return int(wire)

    if wire in cache:
        return cache[wire]

    expr = instructions[wire]
    tokens = expr.split()

    if len(tokens) == 1:
        val = get_value(tokens[0], instructions, cache)

    elif len(tokens) == 2:  # NOT
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
def part_one(data_input: List[str]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    instructions = parse_instructions(data_input)
    return get_value("a", instructions, {})


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two.
    """
    instructions = parse_instructions(data_input)
    override = get_value("a", instructions, {})
    cache = {"b": override}
    return get_value("a", instructions, cache)


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
