# pylint: disable=line-too-long
"""
Day 1: Historian Hysteria

Part 1: Two lists contain location IDs. What is the total distance between your lists?
Answer: 2031679

Part 2: What is the similarity score between the two lists?
Answer: 19678534
"""

from typing import Tuple, List
from utils import profiler


def get_input(file_path: str) -> Tuple[List[int], List[int]]:
    """
    Read two lists of integers from a file.

    Each line in the input file is expected to contain two space-separated integers.
    The first integer goes into the left list, and the second into the right list.

    Args:
        file_path (str): The path to the input file.

    Returns:
        Tuple[List[int], List[int]]: A tuple containing two lists of integers.
    """
    left_lst: List[int] = []
    right_lst: List[int] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(" ")
            left_lst.append(int(line[0]))
            right_lst.append(int(line[-1]))

    return left_lst, right_lst


@profiler
def part_1(left_lst: List[int], right_lst: List[int]) -> int:
    """
    Calculate the pairwise difference between the two lists.
    Sorts both lists and computes the sum of absolute differences
    between corresponding elements.

    Args:
        left_lst (List[int]): The first list of integers.
        right_lst (List[int]): The second list of integers.

    Returns:
        int: The total sum of absolute differences.
    """
    return sum([abs(l - r) for l, r in zip(sorted(left_lst), sorted(right_lst))])


@profiler
def part_2(left_lst: List[int], right_lst: List[int]) -> int:
    """
    Calculate the similarity score.

    For each element in the left list, multiplies it by the number of times
    it appears in the right list and returns the total sum.

    Args:
        left_lst (List[int]): The first list of integers.
        right_lst (List[int]): The second list of integers.

    Returns:
        int: The similarity score.
    """
    return sum([i * right_lst.count(i) for i in left_lst])


if __name__ == "__main__":
    left_input, right_input = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(left_input, right_input)}")
    print(f"Part 2: {part_2(left_input, right_input)}")
