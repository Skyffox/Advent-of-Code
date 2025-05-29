# pylint: disable=line-too-long
"""
Day 11: Seating System

Part 1: Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
Answer: 2194

Part 2: Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?
Answer: 1998
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
        return [line.strip() for line in file.readlines()]


def count_occupied_seats(seating: List[str]) -> int:
    """
    Counts the number of occupied seats in the seating arrangement.

    Args:
        seating (list[str]): A list of strings representing the seating arrangement.

    Returns:
        int: The number of occupied seats.
    """
    return sum(row.count("#") for row in seating)


def apply_rules(seating: List[str], part: int) -> List[str]:
    """
    Applies the seating rules to the current seating arrangement.

    Args:
        seating (list[str]): A list of strings representing the current seating arrangement.
        part (int): The part of the puzzle (1 or 2) to determine the rule set.

    Returns:
        list[str]: A new list of strings representing the updated seating arrangement.
    """
    new_seating = []

    for y, row in enumerate(seating):
        new_row = []
        for x, seat in enumerate(row):
            occupied_neighbors = count_occupied_neighbors(seating, x, y, part)
            if seat == "L" and occupied_neighbors == 0:
                new_row.append("#")
            elif seat == "#" and occupied_neighbors >= (4 if part == 1 else 5):
                new_row.append("L")
            else:
                new_row.append(seat)
        new_seating.append("".join(new_row))

    return new_seating


def count_occupied_neighbors(seating: List[str], x: int, y: int, part: int) -> int:
    """
    Counts the number of occupied neighbors for a given seat.

    Args:
        seating (list[str]): A list of strings representing the seating arrangement.
        x (int): The x-coordinate of the seat.
        y (int): The y-coordinate of the seat.
        part (int): The part of the puzzle (1 or 2) to determine the rule set.

    Returns:
        int: The number of occupied neighbors.
    """
    directions = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ]
    occupied_count = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < len(seating[0]) and 0 <= ny < len(seating):
            if seating[ny][nx] == "#":
                occupied_count += 1
                break
            elif seating[ny][nx] == "L":
                break
            if part == 1:
                break
            nx += dx
            ny += dy

    return occupied_count


@profiler
def compute(data_input: List[str], part: int) -> int:
    """
    Simulates seat occupation until stabilization then returns the count of occupied seats.

    The seating layout evolves in steps:
    - In each iteration, seat states update according to the rules specific for each part.
    - The process repeats until no seats change state between iterations.

    Args:
        data_input (List[str]): A list of strings representing the initial seating layout.

    Returns:
        int: The number of occupied seats after the seating stabilizes.
    """
    seating = data_input
    while True:
        new_seating = apply_rules(seating, part=part)
        if new_seating == seating:
            return count_occupied_seats(seating)
        seating = new_seating


if __name__ == "__main__":
    input_data = get_input("inputs/11_input.txt")

    print(f"Part 1: {compute(input_data, 1)}")
    print(f"Part 2: {compute(input_data, 2)}")
