# pylint: disable=line-too-long
"""
Day 4: The Ideal Stocking Stuffer

Part 1: Santa needs help mining some AdventCoins. To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes.
Answer: 117946

Part 2: Now find one that starts with six zeroes.
Answer: 3938038
"""

from typing import List
import hashlib
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


@profiler
def find_lowest_number(secret_key: str, leading_zeros: int) -> int:
    """
    Finds the lowest positive integer such that the MD5 hash of the secret key
    and the integer starts with the specified number of leading zeroes.

    Args:
        secret_key (str): The secret key to hash.
        leading_zeros (int): Number of leading zeroes required in the hash.

    Returns:
        int: The lowest positive integer that meets the criteria.
    """
    prefix = "0" * leading_zeros
    number = 0
    while True:
        hash_result = hashlib.md5(f"{secret_key}{number}".encode()).hexdigest()
        if hash_result.startswith(prefix):
            return number
        number += 1


if __name__ == "__main__":
    input_data = get_input("inputs/4_input.txt")

    print(f"Part 1: {find_lowest_number(input_data[0], 5)}")
    print(f"Part 2: {find_lowest_number(input_data[0], 6)}")
