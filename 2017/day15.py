# pylint: disable=line-too-long
"""
Day 15: Dueling Generators

Part 1: After 40 million pairs, what is the judge's final count?
Answer: 592

Part 2: After 5 million pairs, but using this new generator logic, what is the judge's final count?
Answer: 335
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns starting values for generators.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: Starting values [generator A, generator B].
    """
    values = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Example line: "Generator A starts with 618"
            parts = line.strip().split()
            values.append(int(parts[-1]))
    return values


def generator(start: int, factor: int, multiple: int = 1):
    """
    Generator function for values produced by a generator.

    Args:
        start (int): Starting value.
        factor (int): Multiplication factor.
        multiple (int): Value must be multiple of this (default 1).

    Yields:
        int: Next value in sequence satisfying multiple condition.
    """
    value = start
    while True:
        value = (value * factor) % 2147483647
        if value % multiple == 0:
            yield value


def judge(a: int, b: int) -> bool:
    """
    Checks if lowest 16 bits of two numbers are equal.

    Args:
        a (int): Value from generator A.
        b (int): Value from generator B.

    Returns:
        bool: True if lower 16 bits match, else False.
    """
    return (a & 0xFFFF) == (b & 0xFFFF)


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Runs 40 million pairs from generators and counts matches.

    Args:
        data_input (List[int]): Starting values for generators.

    Returns:
        int: Number of matches.
    """
    gen_a = generator(data_input[0], 16807)
    gen_b = generator(data_input[1], 48271)
    count = 0
    for _ in range(40_000_000):
        a = next(gen_a)
        b = next(gen_b)
        if judge(a, b):
            count += 1
    return count


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Runs 5 million pairs with generator criteria and counts matches.

    Args:
        data_input (List[int]): Starting values for generators.

    Returns:
        int: Number of matches.
    """
    gen_a = generator(data_input[0], 16807, 4)
    gen_b = generator(data_input[1], 48271, 8)
    count = 0
    for _ in range(5_000_000):
        a = next(gen_a)
        b = next(gen_b)
        if judge(a, b):
            count += 1
    return count


if __name__ == "__main__":
    input_data = get_input("inputs/15_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
