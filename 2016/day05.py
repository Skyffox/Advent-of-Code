# pylint: disable=line-too-long
"""
Day 5: How About a Nice Game of Chess?

Part 1: Given the actual Door ID, what is the password?
Answer: 2414bc77

Part 2: Given the actual Door ID and this new method, what is the password?
Answer: 437e60fc
"""

from typing import List
import hashlib
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list containing the single salt string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List with one element, the salt string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def md5_hash(s: str) -> str:
    """
    Returns the hexadecimal MD5 hash of a string.

    Args:
        s (str): Input string.

    Returns:
        str: MD5 hash as hex string.
    """
    return hashlib.md5(s.encode("utf-8")).hexdigest()


@profiler
def part_one(data_input: List[str]) -> str:
    """
    Finds the password by hashing the door ID + index and taking the 6th char when hash starts with five zeros.

    Args:
        data_input (List[str]): List with one salt string.

    Returns:
        str: The password for part one.
    """
    salt = data_input[0]
    password = []
    index = 0
    while len(password) < 8:
        h = md5_hash(salt + str(index))
        if h.startswith("00000"):
            password.append(h[5])
        index += 1
    return "".join(password)


@profiler
def part_two(data_input: List[str]) -> str:
    """
    Finds the password using the position indicated by the 6th char of the hash (if valid) and places the 7th char there.

    Args:
        data_input (List[str]): List with one salt string.

    Returns:
        str: The password for part two.
    """
    salt = data_input[0]
    password = [None] * 8
    index = 0
    filled_positions = 0

    while filled_positions < 8:
        h = md5_hash(salt + str(index))
        if h.startswith("00000"):
            pos_char = h[5]
            if pos_char.isdigit():
                pos = int(pos_char)
                if 0 <= pos < 8 and password[pos] is None:
                    password[pos] = h[6]
                    filled_positions += 1
        index += 1

    return "".join(password)


if __name__ == "__main__":
    input_data = get_input("inputs/5_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
