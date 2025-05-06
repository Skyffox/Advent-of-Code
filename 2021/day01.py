# pylint: disable=line-too-long
"""
Day 1: Sonar Sweep

Part 1: See how many times there is an increase or decrease in the data.
Answer: 1624

Part 2: Instead, compare it over a window of 3 items. In this case, we only compare the first and the last of that window.
Answer: 1653
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input data from the specified file and returns a list of integers.

    Args:
        file_path (str): Path to the input file containing the list of numbers.

    Returns:
        List[int]: A list of integers representing the sonar readings.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


@profiler
def part_1(lst: List[int]) -> int:
    """
    Count the number of times a number increases from the previous number in the list.

    Args:
        lst (List[int]): A list of integers representing sonar readings.

    Returns:
        int: The number of times an increase occurs between subsequent numbers.
    """
    return sum(1 for i in range(len(lst) - 1) if lst[i + 1] > lst[i])


@profiler
def part_2(lst: List[int]) -> int:
    """
    Count the number of times a sum of a window of 3 numbers increases from the previous sum.

    Args:
        lst (List[int]): A list of integers representing sonar readings.

    Returns:
        int: The number of times a 3-number sliding window sum increases.
    """
    return sum(1 for i in range(len(lst) - 3) if lst[i + 3] > lst[i])


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
