# pylint: disable=line-too-long
"""
Day 8: Matchsticks

Part 1: Disregarding the whitespace in the file, what is the number of characters of code for string literals minus the number of characters in 
        memory for the values of the strings in total for the entire file?
Answer: 1333

Part 2: Find the total number of characters to represent the newly encoded strings minus the number of characters of code in each original string literal.
Answer: 2046
"""

from typing import List
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


def encoded_length(line: str) -> int:
    """
    Returns the length of the encoded version of the string.

    Args:
        line (str): The input string literal.

    Returns:
        int: The length after escaping characters.
    """
    escaped = line.replace("\\", "\\\\").replace("\"", "\\\"")
    return len(f"\"{escaped}\"")


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Calculate the sum of number of characters of code for string literals minus the number of characters in memory.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    return sum(len(line) - len(eval(line)) for line in data_input)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Calculate the sum of the total number of characters to represent the newly encoded strings minus the number of characters of code.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two.
    """
    return sum(encoded_length(line) - len(line) for line in data_input)


if __name__ == "__main__":
    input_data = get_input("inputs/8_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
