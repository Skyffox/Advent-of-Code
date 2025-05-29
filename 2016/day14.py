# pylint: disable=line-too-long
"""
Day 14: One-Time Pad

Part 1: Given the actual salt in your puzzle input, what index produces your 64th one-time pad key?
Answer: 23769

Part 2: Given the actual salt in your puzzle input and using 2016 extra MD5 calls of key stretching, what index now produces your 64th one-time pad key?
Answer: 20606
"""

import hashlib
import re
from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list containing the salt string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List containing the salt string.
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
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def stretched_hash(s: str) -> str:
    """
    Returns a stretched MD5 hash of the input string by applying MD5 hashing 2017 times.

    The first hash is computed from the original string, and then the result is re-hashed
    2016 additional times.

    Args:
        s (str): The input string to hash.

    Returns:
        str: The final MD5 hash after 2017 iterations.
    """
    h = md5_hash(s)
    for _ in range(2016):
        h = md5_hash(h)
    return h


def find_triplet(s: str) -> str:
    """
    Find the first character that appears three times in a row in the string.

    Args:
        s (str): Input string.

    Returns:
        str: The character found or '' if none.
    """
    match = re.search(r'(.)\1\1', s)
    return match.group(1) if match else ''


@profiler
def compute(data_input: List[str], is_part2: bool) -> int:
    """
    Finds the index of the 64th key using stretched MD5 hashes.

    Args:
        data_input (List[str]): List containing the salt string.

    Returns:
        int: Index of the 64th key.
    """
    salt = data_input[0]
    keys_found = 0
    index = 0
    hash_cache = {}

    while True:
        if index not in hash_cache:
            hash_cache[index] = stretched_hash(f"{salt}{index}") if is_part2 else md5_hash(f"{salt}{index}")
        h = hash_cache[index]
        c = find_triplet(h)
        if c:
            for i in range(index + 1, index + 1001):
                if i not in hash_cache:
                    hash_cache[i] = stretched_hash(f"{salt}{i}") if is_part2 else md5_hash(f"{salt}{i}")
                # Checks if the string contains five consecutive characters c
                if c * 5 in hash_cache[i]:
                    keys_found += 1
                    if keys_found == 64:
                        return index
                    break
        index += 1


if __name__ == "__main__":
    input_data = get_input("inputs/14_input.txt")

    print(f"Part 1: {compute(input_data, False)}")
    print(f"Part 2: {compute(input_data, True)}")
