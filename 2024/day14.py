# pylint: disable=line-too-long
"""
Day 14: Restroom Redoubt

Part 1: What will the safety factor be after exactly 100 seconds have elapsed?
Answer: 216027840

Part 2: What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
Answer: 6876
"""

import re
from typing import List, Tuple
from copy import deepcopy
from utils import profiler


def get_input(file_path: str) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Parse the input file into initial positions and velocities for the robots.

    Each line contains a position and velocity, e.g., "10,30 1,-1".

    Args:
        file_path (str): Path to the input file.

    Returns:
        Tuple[List[List[int]], List[List[int]]]: A tuple of position and velocity lists.
    """
    positions: List[List[int]] = []
    velocities: List[List[int]] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            curr_line = re.findall(r'-?\d+,-?\d+', line)
            positions.append(list(map(int, curr_line[0].split(","))))
            velocities.append(list(map(int, curr_line[1].split(","))))

    return positions, velocities


def print_grid(positions: List[List[int]], max_width: int, max_length: int) -> None:
    """
    Print the current positions of robots on the grid.

    Args:
        positions (List[List[int]]): List of [x, y] coordinates of robots.
        max_width (int): Width of the grid.
        max_length (int): Height of the grid.
    """
    for l in range(max_length):
        for w in range(max_width):
            if [w, l] in positions:
                print(positions.count([w, l]), end="")
            else:
                print(".", end="")
        print()
    print()


@profiler
def part_one(positions: List[List[int]], velocities: List[List[int]]) -> int:
    """
    Simulate 100 seconds of movement, and compute the safety factor.

    Args:
        positions (List[List[int]]): Initial positions of robots.
        velocities (List[List[int]]): Velocities for each robot.

    Returns:
        int: The calculated safety factor.
    """
    max_width = 101
    max_length = 103
    seconds = 100

    for _ in range(seconds):
        for idx, (p, v) in enumerate(zip(positions, velocities)):
            x, y = p[0] + v[0], p[1] + v[1]
            if x < 0:
                x += max_width
            if y < 0:
                y += max_length
            if x >= max_width:
                x %= max_width
            if y >= max_length:
                y %= max_length

            positions[idx] = [x, y]

    # Calculate the amount of guards in each quadrant
    first = second = third = fourth = 0

    for x, y in positions:
        # Upper quadrant
        if y < (max_length - 1) // 2:
            # Topleft
            if x < (max_width - 1) // 2:
                first += 1
            # Topright
            elif x > (max_width - 1) // 2:
                second += 1

        # Lower quadrant
        elif y > (max_length - 1) // 2:
            # Bottomleft
            if x < (max_width - 1) // 2:
                third += 1
            # Bottomright
            elif x > (max_width - 1) // 2:
                fourth += 1

    return first * second * third * fourth


@profiler
def part_two(positions: List[List[int]], velocities: List[List[int]]) -> int:
    """
    Simulate the robot movements until the visual "Easter egg" appears.

    Args:
        positions (List[List[int]]): Initial positions of robots.
        velocities (List[List[int]]): Velocities for each robot.

    Returns:
        int: The number of seconds elapsed when the Easter egg appears.
    """
    max_width = 101
    max_length = 103
    seconds = 6876

    for _ in range(seconds):
        for idx, (p, v) in enumerate(zip(positions, velocities)):
            # Calculate the new position based on the velocity, if we are outside the grid then we wrap around
            x, y = p[0] + v[0], p[1] + v[1]
            if x < 0:
                x += max_width
            if y < 0:
                y += max_length
            if x >= max_width:
                x %= max_width
            if y >= max_length:
                y %= max_length

            positions[idx] = [x, y]

        # Debug purposes, also the print is zero-indexed
        # if s == seconds - 1:
        #     print_grid(positions, max_width, max_length)

    return seconds


if __name__ == "__main__":
    input_positions, input_velocities = get_input("inputs/14_input.txt")

    input_positions_cpy = deepcopy(input_positions)

    print(f"Part 1: {part_one(input_positions, input_velocities)}")
    print(f"Part 2: {part_two(input_positions_cpy, input_velocities)}")
