# pylint: disable=line-too-long
"""
Day 3: Perfectly Spherical Houses in a Vacuum

Part 1: Follow the instructions to see how many houses Santa can visit  
Answer: 2565

Part 2: Take turns between Santa and Robo-Santa and see how many houses they can visit  
Answer: 2639
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads the input file and returns the movement instructions.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list[str]: A list of direction characters ('<', '>', '^', 'v').
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(file.read().strip())


def move(x: int, y: int, direction: str, visited: dict[tuple[int, int], int]) -> tuple[dict, int, int]:
    """
    Updates the (x, y) position based on the direction and tracks visited houses.

    Args:
        x (int): Current x-coordinate.
        y (int): Current y-coordinate.
        direction (str): Direction to move ('<', '>', '^', 'v').
        visited (dict): Dictionary mapping (x, y) coordinates to visit counts.

    Returns:
        tuple: Updated visited dictionary, new x, new y.
    """
    if direction == '>':
        x += 1
    elif direction == '<':
        x -= 1
    elif direction == '^':
        y += 1
    elif direction == 'v':
        y -= 1

    visited[(x, y)] = visited.get((x, y), 0) + 1
    return visited, x, y


@profiler
def part_1(instructions: List[str]) -> int:
    """
    Follows instructions and counts how many unique houses Santa visits.

    Args:
        instructions (list[str]): Movement instructions.

    Returns:
        int: Number of unique houses visited.
    """
    x, y = 0, 0
    visited = {(0, 0): 1}
    for direction in instructions:
        visited, x, y = move(x, y, direction, visited)
    return len(visited)


@profiler
def part_2(instructions: list[str]) -> int:
    """
    Alternates turns between Santa and Robo-Santa, counting unique houses visited.

    Args:
        instructions (list[str]): Movement instructions.

    Returns:
        int: Number of unique houses visited.
    """
    santa_x, santa_y = 0, 0
    robo_x, robo_y = 0, 0
    visited = {(0, 0): 2}

    for turn, direction in enumerate(instructions):
        if turn % 2 == 0:
            visited, santa_x, santa_y = move(santa_x, santa_y, direction, visited)
        else:
            visited, robo_x, robo_y = move(robo_x, robo_y, direction, visited)

    return len(visited)


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
