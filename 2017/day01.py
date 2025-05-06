# pylint: disable=line-too-long
"""
Day 1: Inverse Captcha

Part 1: Calculate the sum of digits in a list that match the next digit, with the list being circular.
Answer: 1253

Part 2: Similar to Part 1, but compare each digit with the digit halfway around the list.
Answer: 1278
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and converts each digit into an integer, returning them as a list.

    Args:
        file_path (str): The path to the input file.

    Returns:
        List[int]: List of digits from the input.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip()))


@profiler
def part_1(lst: List[int]) -> int:
    """
    Sums the digits in the list that match the next digit in a circular manner.

    Args:
        lst (List[int]): A list of digits.

    Returns:
        int: The sum of digits that match the next digit (with circular behavior).
    """
    # Compare each digit with the next, wrapping around the list for circular behavior
    return sum([i for i, j in zip(lst, lst[1:] + [lst[0]]) if i == j])


@profiler
def part_2(lst: List[int]) -> int:
    """
    Sums the digits in the list that match the digit halfway further in the list.

    Args:
        lst (List[int]): A list of digits.

    Returns:
        int: The sum of digits that match the digit halfway around the list.
    """
    # Compare each digit with the one halfway around the list
    return sum([i for i, j in zip(lst, lst[len(lst)//2:] + lst[:len(lst)//2]) if i == j])


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
