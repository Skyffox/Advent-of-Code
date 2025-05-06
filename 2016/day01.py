# pylint: disable=line-too-long
"""
Day 1: No Time for a Taxicab

Part 1: See how many blocks we are away from the start after following instructions  
Answer: 252

Part 2: Check for a path and see where we have been before  
Answer: 143
"""

from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Reads and parses the input instructions.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[str]: A list of instruction strings, e.g., ['R2', 'L3'].
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip().split(", ")


def move(
    orientation: str,
    direction: str,
    distance: int,
    position: Tuple[int, int],
    visited: List[Tuple[int, int]]
) -> Tuple[str, Tuple[int, int], List[Tuple[int, int]]]:
    """
    Updates orientation and position based on the instruction, tracking each step.

    Args:
        orientation (str): Current facing direction ('N', 'E', 'S', 'W').
        direction (str): Turn direction from input ('L' or 'R').
        distance (int): Number of steps to take.
        position (tuple[int, int]): Current (x, y) coordinates.
        visited (List[tuple[int, int]]): List of all visited positions.

    Returns:
        tuple: Updated orientation, position, and visited list.
    """
    # Define direction change logic
    directions = ['N', 'E', 'S', 'W']
    idx = directions.index(orientation)
    if direction == 'R':
        orientation = directions[(idx + 1) % 4]
    else:
        orientation = directions[(idx - 1) % 4]

    x, y = position

    for _ in range(distance):
        if orientation == 'N':
            y += 1
        elif orientation == 'S':
            y -= 1
        elif orientation == 'E':
            x += 1
        elif orientation == 'W':
            x -= 1
        visited.append((x, y))

    return orientation, (x, y), visited


@profiler
def part_1(instructions: List[str]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Executes instructions and computes final Manhattan distance from origin.

    Args:
        instructions (List[str]): Movement instructions.

    Returns:
        Tuple: Final Manhattan distance, and list of visited positions for Part 2.
    """
    position = (0, 0)
    visited = [position]
    orientation = 'N'

    for instr in instructions:
        turn = instr[0]
        steps = int(instr[1:])
        orientation, position, visited = move(orientation, turn, steps, position, visited)

    distance = abs(position[0]) + abs(position[1])
    return distance, visited


@profiler
def part_2(visited: List[Tuple[int, int]]) -> int:
    """
    Finds the first location visited twice.

    Args:
        visited (List[Tuple[int, int]]): List of positions visited in order.

    Returns:
        int: Manhattan distance to the first location visited twice.
    """
    seen = set()
    for pos in visited:
        if pos in seen:
            return abs(pos[0]) + abs(pos[1])
        seen.add(pos)
    return -1 # Just in case


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    answer_1, visited_positions = part_1(input_data)
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {part_2(visited_positions)}")
