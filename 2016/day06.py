# pylint: disable=line-too-long
"""
Day 6: Signals and Noise

Part 1: Given the recording in your puzzle input, what is the error-corrected version of the message being sent?
Answer: wkbvmikb

Part 2: Given the recording in your puzzle input and this new decoding methodology, what is the original message that Santa is trying to send?
Answer: evakwaga

"""

from typing import List
from collections import Counter
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list of stripped lines.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[str]: List of lines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def part_one(data_input: List[str]) -> str:
    """
    Decodes the message by selecting the most common letter in each column.

    Args:
        data_input (List[str]): List of input strings.

    Returns:
        str: Decoded message using most common letters.
    """
    decoded = []
    for col_idx in range(len(data_input[0])):
        column = [line[col_idx] for line in data_input]
        most_common_char = Counter(column).most_common(1)[0][0]
        decoded.append(most_common_char)
    return "".join(decoded)


@profiler
def part_two(data_input: List[str]) -> str:
    """
    Decodes the message by selecting the least common letter in each column.

    Args:
        data_input (List[str]): List of input strings.

    Returns:
        str: Decoded message using least common letters.
    """
    decoded = []
    for col_idx in range(len(data_input[0])):
        column = [line[col_idx] for line in data_input]
        least_common_char = Counter(column).most_common()[-1][0]
        decoded.append(least_common_char)
    return "".join(decoded)


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
