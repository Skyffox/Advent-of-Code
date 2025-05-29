# pylint: disable=line-too-long
"""
Day 11: Corporate Policy

Part 1: Given Santa's current password (your puzzle input), what should his next password be?
Answer: vzbxxyzz

Part 2: Santa's password expired again. What's the next one?
Answer: vzcaabcc
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


def increment_password(pw: str) -> str:
    """
    Increments the password string like a base-26 number.

    Args:
        pw (str): Current password.

    Returns:
        str: The next password.
    """
    pw = list(pw)
    i = len(pw) - 1

    while i >= 0:
        if pw[i] == 'z':
            pw[i] = 'a'
            i -= 1
        else:
            pw[i] = chr(ord(pw[i]) + 1)
            break

    return ''.join(pw)


def is_valid(pw: str) -> bool:
    """
    Validates the password according to the corporate policy rules.

    Args:
        pw (str): Password string.

    Returns:
        bool: True if password is valid, else False.
    """
    # Rule 1: must include one increasing straight of three letters
    has_straight = any(
        ord(pw[i]) + 1 == ord(pw[i + 1]) and ord(pw[i + 1]) + 1 == ord(pw[i + 2])
        for i in range(len(pw) - 2)
    )

    # Rule 2: must not contain 'i', 'o', or 'l'
    if any(c in pw for c in 'iol'):
        return False

    # Rule 3: must contain at least two different, non-overlapping pairs of letters
    pairs = set()
    i = 0
    while i < len(pw) - 1:
        if pw[i] == pw[i + 1]:
            pairs.add(pw[i])
            i += 2  # skip next to avoid overlapping
        else:
            i += 1

    return has_straight and len(pairs) >= 2


def next_valid_password(current: str) -> str:
    """
    Finds the next password that is valid.

    Args:
        current (str): Starting password.

    Returns:
        str: The next valid password.
    """
    while True:
        current = increment_password(current)
        if is_valid(current):
            return current


@profiler
def part_one(data_input: List[str]) -> str:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        str: The next valid password.
    """
    return next_valid_password(data_input[0])


@profiler
def part_two(data_input: List[str]) -> str:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        str: The valid password after the next one.
    """
    first = next_valid_password(data_input[0])
    return next_valid_password(first)


if __name__ == "__main__":
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
