# pylint: disable=line-too-long
"""
Day 9: Encoding Error

Part 1: What is the first number that does not have this property?
Answer: 127

Part 2: What is the encryption weakness in your XMAS-encrypted list of numbers?
Answer: 62
"""

from typing import List
from itertools import combinations
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of integers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        list[int]: A list of integers from the input file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file.readlines()]


def find_invalid_number(numbers: List[int], preamble_length: int) -> int:
    """
    Finds the first number in the list that is not the sum of two of the 25 numbers before it.

    Args:
        numbers (list[int]): A list of numbers.
        preamble_length (int): The number of previous numbers to consider.

    Returns:
        int: The first invalid number.
    """
    for i in range(preamble_length, len(numbers)):
        if not any(sum(pair) == numbers[i] for pair in combinations(numbers[i - preamble_length:i], 2)):
            return numbers[i]
    return -1


def find_encryption_weakness(numbers: List[int], target: int) -> int:
    """
    Finds a contiguous set of at least two numbers in the list which sum to the target number,
    and returns the sum of the smallest and largest number in the set.

    Args:
        numbers (list[int]): A list of numbers.
        target (int): The target sum.

    Returns:
        int: The sum of the smallest and largest number in the contiguous set.
    """
    for i in range(len(numbers)):
        for j in range(i + 2, len(numbers) + 1):
            contiguous_set = numbers[i:j]
            total = sum(contiguous_set)
            if total == target:
                return min(contiguous_set) + max(contiguous_set)
            elif total > target:
                break
    return -1


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Identifies the first number in the input list which is not the sum of two of the 25 immediately preceding numbers.

    This is typically used in problems where the list represents a sequence of numbers following specific rules,
    such as the XMAS encryption protocol. The '25' represents the size of the preamble.

    Args:
        data_input (List[int]): A list of integers representing the encrypted data sequence.

    Returns:
        int: The first invalid number that does not follow the summing rule.
    """
    return find_invalid_number(data_input, 25)


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Finds the encryption weakness in the data by locating a contiguous range of numbers that sum to the invalid number found in part one.

    The encryption weakness is defined as the sum of the smallest and largest numbers in this contiguous range.

    Args:
        data_input (List[int]): A list of integers representing the encrypted data sequence.

    Returns:
        int: The encryption weakness, i.e., the sum of the smallest and largest numbers in the contiguous range.
    """
    invalid_number = find_invalid_number(data_input, 25)
    return find_encryption_weakness(data_input, invalid_number)


if __name__ == "__main__":
    input_data = get_input("inputs/9_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
