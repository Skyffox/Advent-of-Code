# pylint: disable=line-too-long
"""
Day 7: Bridge Repair

Part 1: Define all possible operations on a list of numbers and see if a combination fits an answer
Answer: 975671981569

Part 2: Do the same as part 1, but there is an additional operator || that concatenates two values
Answer: 223472064194845
"""

import time
from typing import List, Tuple


def eval_equation(nums: List[int], target: int) -> bool:
    """
    Recursively evaluates a list of integers from left to right using + and * operations to match a target.

    Args:
        nums (List[int]): List of integers.
        target (int): Target value to achieve.

    Returns:
        bool: True if a valid combination of + and * results in the target.
    """
    if nums[0] > target:
        return False
    if len(nums) == 1:
        return nums[0] == target

    n = nums[0]
    rest = nums[1:]

    add = rest.copy()
    mul = rest.copy()

    add[0] += n
    mul[0] *= n

    return eval_equation(add, target) or eval_equation(mul, target)


def eval_equation_part_2(nums: List[int], target: int) -> bool:
    """
    Recursively evaluates a list of integers using +, *, and || (concatenation) to match a target.

    Args:
        nums (List[int]): List of integers.
        target (int): Target value to achieve.

    Returns:
        bool: True if a valid combination of operations results in the target.
    """
    if nums[0] > target:
        return False
    if len(nums) == 1:
        return nums[0] == target

    n = nums[0]
    rest = nums[1:]

    add = rest.copy()
    mul = rest.copy()
    concat = rest.copy()

    add[0] += n
    mul[0] *= n
    concat[0] = int(str(n) + str(concat[0]))

    return (
        eval_equation_part_2(add, target)
        or eval_equation_part_2(mul, target)
        or eval_equation_part_2(concat, target)
    )


def get_input(file_path: str) -> Tuple[List[int], List[List[int]]]:
    """
    Parses input from a file, separating target values and lists of numbers.

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple[List[int], List[List[int]]]: A tuple of target values and corresponding number lists.
    """
    answers_list: List[int] = []
    number_lists: List[List[int]] = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            answer_str, number_str = line.strip().split(":")
            answers_list.append(int(answer_str))
            number_lists.append(list(map(int, number_str.strip().split())))

    return answers_list, number_lists


if __name__ == "__main__":
    t1 = time.time()

    # Get input data
    answers, numbers = get_input("inputs/7_input.txt")

    TOTAL_PART_1 = 0
    TOTAL_PART_2 = 0

    for answer, numbers in zip(answers, numbers):
        TOTAL_PART_1 += answer if eval_equation(numbers.copy(), answer) else 0
        TOTAL_PART_2 += answer if eval_equation_part_2(numbers.copy(), answer) else 0

    print(f"Part 1: {TOTAL_PART_1}")
    print(f"Part 2: {TOTAL_PART_2}")

    # Calc execution time, not really suited for the profiler since we use recursion
    t2 = time.time()
    print(f"Executed in {t2 - t1:0.4f} seconds")
