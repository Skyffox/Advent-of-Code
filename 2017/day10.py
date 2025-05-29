# pylint: disable=line-too-long
"""
Day 10: Knot Hash

Part 1: Product of the first two numbers in the resulting list.
Answer: 46600

Part 2: Treating your puzzle input as a string of ASCII characters, what is the Knot Hash of your puzzle input? Ignore any leading or trailing whitespace you might encounter.
Answer: 23234babdc6afa036749cfa9b597de1b
"""

from functools import reduce
from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of ASCII codes for the input string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: List of ASCII codes.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readline().strip()


def knot_hash_round(lengths, size=256, rounds=1):
    """
    Performs the knot hash algorithm for a given number of rounds.

    Args:
        lengths (List[int]): The list of lengths to apply.
        size (int): Size of the circular list.
        rounds (int): Number of rounds to perform.

    Returns:
        List[int]: The sparse hash after all rounds.
    """
    lst = list(range(size))
    pos = 0
    skip = 0

    for _ in range(rounds):
        for length in lengths:
            # Reverse the section
            indices = [(pos + i) % size for i in range(length)]
            values = [lst[i] for i in indices][::-1]
            for i, val in zip(indices, values):
                lst[i] = val

            pos = (pos + length + skip) % size
            skip += 1

    return lst


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Runs one round of knot hash and returns product of first two numbers.

    Args:
        data_input (List[int]): Lengths for the knot hash.

    Returns:
        int: Product of first two numbers in the list after processing.
    """
    lengths = list(map(int, data_input.strip().split(',')))
    sparse = knot_hash_round(lengths)
    return sparse[0] * sparse[1]


def dense_hash(sparse_hash: List[int]) -> List[int]:
    """
    Converts sparse hash to dense hash by XORing blocks of 16 numbers.

    Args:
        sparse_hash (List[int]): Sparse hash list of 256 numbers.

    Returns:
        List[int]: Dense hash of 16 numbers.
    """
    return [reduce(lambda x, y: x ^ y, sparse_hash[i:i + 16]) for i in range(0, 256, 16)]



@profiler
def part_two(data_input: List[int]) -> str:
    """
    Computes the full Knot Hash as a hexadecimal string.

    Args:
        data_input (List[int]): ASCII codes of input string.

    Returns:
        str: Knot hash hex string.
    """
    lengths = list(map(ord, data_input)) + [17, 31, 73, 47, 23]
    sparse = knot_hash_round(lengths, rounds=64)
    dense = dense_hash(sparse)
    return ''.join(f'{x:02x}' for x in dense)


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
