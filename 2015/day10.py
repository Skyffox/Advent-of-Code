# pylint: disable=line-too-long
"""
Day 10: Elves Look, Elves Say

Part 1: Starting with the digits in your puzzle input, apply this process 40 times. What is the length of the result?
Answer: 492982

Part 2: Now, starting again with the digits in your puzzle input, apply this process 50 times. What is the length of the new result?
Answer: 6989950
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


def look_and_say(sequence: str) -> str:
    """
    Applies the look-and-say transformation to a sequence.

    Args:
        sequence (str): The input number sequence.

    Returns:
        str: The next sequence in the look-and-say series.
    """
    result = []
    i = 0
    while i < len(sequence):
        count = 1
        while i + 1 < len(sequence) and sequence[i] == sequence[i + 1]:
            count += 1
            i += 1
        result.append(f"{count}{sequence[i]}")
        i += 1
    return "".join(result)


@profiler
def part_one(data_input: List[str]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The length of the sequence after 40 iterations.
    """
    sequence = data_input[0]
    for _ in range(40):
        sequence = look_and_say(sequence)
    return len(sequence)


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The length of the sequence after 50 iterations.
    """
    sequence = data_input[0]
    for _ in range(50):
        sequence = look_and_say(sequence)
    return len(sequence)


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
