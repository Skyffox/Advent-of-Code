# pylint: disable=line-too-long
"""
Day 10: The Stars Align

Part 1: What message will eventually appear in the sky?
Answer: See console output (BFFZCNXE)

Part 2: Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would they have needed to wait for that message to appear?
Answer: 10392
"""

import re
from typing import List, Tuple
from utils import profiler


def get_input(file_path: str) -> List[Tuple[int, int, int, int]]:
    """
    Reads the puzzle input file and parses each line into a tuple of position and velocity.

    Each line contains a point's position and velocity in the format:
    position=< x,  y> velocity=< vx, vy>

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Tuple[int, int, int, int]]: A list of tuples representing each point as (x, y, vx, vy).
    """
    pattern = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)>\s*velocity=<\s*(-?\d+),\s*(-?\d+)>")
    points = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            x, y, vx, vy = map(int, pattern.match(line).groups())
            points.append((x, y, vx, vy))

    return points


def bounding_box(points: List[Tuple[int, int, int, int]]) -> Tuple[int, int, int, int]:
    """
    Computes the axis-aligned bounding box for a given list of points.

    Args:
        points (List[Tuple[int, int, int, int]]): List of points with positions and velocities.

    Returns:
        Tuple[int, int, int, int]: The bounding box as (min_x, max_x, min_y, max_y).
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def advance(points: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
    """
    Advances each point by one step according to its velocity.

    Args:
        points (List[Tuple[int, int, int, int]]): List of points with positions and velocities.

    Returns:
        List[Tuple[int, int, int, int]]: New list of points after moving.
    """
    return [(x + vx, y + vy, vx, vy) for (x, y, vx, vy) in points]


@profiler
def compute(points: List[Tuple[int, int, int, int]]) -> int:
    """
    Simulates the movement of points over time to find when they form a readable message.

    This function tracks the bounding box area and stops when it starts to increase,
    indicating the message has formed in the previous step. It then prints the message
    as ASCII art and returns the number of seconds elapsed.

    Args:
        points (List[Tuple[int, int, int, int]]): Initial positions and velocities of the points.

    Returns:
        int: The number of seconds that elapsed when the message appeared (Part 2 answer).
    """
    prev_area = None
    seconds = 0
    while True:
        min_x, max_x, min_y, max_y = bounding_box(points)
        area = (max_x - min_x) * (max_y - min_y)

        if prev_area is not None and area > prev_area:
            # The message has formed at the previous time step
            points = [(x - vx, y - vy, vx, vy) for (x, y, vx, vy) in points]
            seconds -= 1
            break

        prev_area = area
        points = advance(points)
        seconds += 1

    # Display the message as a grid
    min_x, max_x, min_y, max_y = bounding_box(points)
    grid = []
    points_set = set((x, y) for x, y, _, _ in points)

    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            row += "#" if (x, y) in points_set else "."
        grid.append(row)

    # Uncomment below to see the visual message (Part 1)
    # print("\n".join(grid))

    return seconds


if __name__ == "__main__":
    input_data = get_input("inputs/10_input.txt")

    # The message of Part 1 gets printed manually in this case
    print("Part 1: BFFZCNXE")
    print(f"Part 2: {compute(input_data)}")
