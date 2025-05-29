# pylint: disable=line-too-long
"""
Day 9: Stream Processing

Part 1: What is the total score for all groups in your input?
Answer: 14212

Part 2: How many non-canceled characters are within the garbage in your puzzle input?
Answer: 6569
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list containing the single stream string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List with one element: the stream string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [file.readline().strip()]


@profiler
def compute(data_input: List[str]) -> int:
    """
    Computes the total score for all groups in the stream.

    Args:
        data_input (List[str]): List with the stream string.

    Returns:
        int: Total score of groups.
    """
    total_score = 0
    depth = 0
    garbage_count = 0
    in_garbage = False
    skip_next = False

    for char in data_input:
        if skip_next:
            skip_next = False
            continue
        if char == '!':
            skip_next = True
        elif in_garbage:
            if char == '>':
                in_garbage = False
            else:
                garbage_count += 1
        else:
            if char == '<':
                in_garbage = True
            elif char == '{':
                depth += 1
                total_score += depth
            elif char == '}':
                depth -= 1

    return total_score, garbage_count


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    total, garbage = compute(input_data[0])

    print(f"Part 1: {total}")
    print(f"Part 2: {garbage}")
