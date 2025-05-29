# pylint: disable=line-too-long
"""
Day 17: Two Steps Forward

Part 1: Given your vault's passcode, what is the shortest path (the actual path, not just the length) to reach the vault?
Answer: RDRLDRDURD

Part 2: What is the length of the longest path that reaches the vault?
Answer: 596
"""

from typing import List
from collections import deque
import hashlib
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns a list containing the passcode string.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[str]: List containing the passcode string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


def get_doors(passcode: str, path: str) -> List[bool]:
    """
    Determines which doors are open based on MD5 hash.

    Args:
        passcode (str): The puzzle input passcode.
        path (str): The path taken so far.

    Returns:
        List[bool]: List of booleans indicating if doors [up, down, left, right] are open.
    """
    hash_str = hashlib.md5((passcode + path).encode()).hexdigest()
    return [c in 'bcdef' for c in hash_str[:4]]


@profiler
def part_one(data_input: List[str]) -> str:
    """
    Finds shortest path to vault.

    Args:
        data_input (List[str]): List containing passcode string.

    Returns:
        str: The shortest path as a string of moves (U,D,L,R).
    """
    passcode = data_input[0]
    queue = deque()
    queue.append((0, 0, "")) # x, y, path

    while queue:
        x, y, path = queue.popleft()
        if (x, y) == (3, 3):
            return path

        doors = get_doors(passcode, path)
        directions = ['U', 'D', 'L', 'R']
        moves = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

        for door_open, (nx, ny), move in zip(doors, moves, directions):
            if door_open and 0 <= nx <= 3 and 0 <= ny <= 3:
                queue.append((nx, ny, path + move))

    return ""


@profiler
def part_two(data_input: List[str]) -> int:
    """
    Finds length of the longest path to vault.

    Args:
        data_input (List[str]): List containing passcode string.

    Returns:
        int: Length of longest path.
    """
    passcode = data_input[0]
    queue = deque()
    queue.append((0, 0, "")) # x, y, path
    max_length = 0

    while queue:
        x, y, path = queue.popleft()
        if (x, y) == (3, 3):
            max_length = max(max_length, len(path))
            continue

        doors = get_doors(passcode, path)
        directions = ['U', 'D', 'L', 'R']
        moves = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]

        for door_open, (nx, ny), move in zip(doors, moves, directions):
            if door_open and 0 <= nx <= 3 and 0 <= ny <= 3:
                queue.append((nx, ny, path + move))

    return max_length


if __name__ == "__main__":
    input_data = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
