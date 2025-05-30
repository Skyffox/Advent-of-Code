# pylint: disable=line-too-long
"""
Day 10: Monitoring Station

Part 1: Find the best location for a new monitoring station. How many other asteroids can be detected from that location?
Answer: 292

Part 2: The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which asteroid that will be; 
        what do you get if you multiply its X coordinate by 100 and then add its Y coordinate? (For example, 8,2 becomes 802.)
Answer: 317
"""

from typing import List, Tuple
from math import atan2, pi
from collections import defaultdict
from utils import profiler


def get_and_parse_asteroids(file_path: str) -> List[Tuple[int, int]]:
    """
    Reads the input file and parses the asteroid map into a list of asteroid coordinates.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[Tuple[int, int]]: List of (x, y) asteroid coordinates.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [
            (x, y)
            for y, line in enumerate(file)
            for x, ch in enumerate(line.strip())
            if ch == '#'
        ]


def angle_between(source: Tuple[int, int], target: Tuple[int, int]) -> float:
    """
    Computes the angle from source to target, adjusted to start from up and rotate clockwise.

    Args:
        source (Tuple[int, int]): The source coordinate.
        target (Tuple[int, int]): The target coordinate.

    Returns:
        float: The angle in radians.
    """
    dx = target[0] - source[0]
    dy = source[1] - target[1] # Reverse Y for upward
    angle = atan2(dx, dy)
    return angle % (2 * pi)


@profiler
def part_one(asteroids: List[str]) -> int:
    """
    Solves part one of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part one.
    """
    max_visible = 0

    for base in asteroids:
        angles = {angle_between(base, other) for other in asteroids if other != base}
        max_visible = max(max_visible, len(angles))

    return max_visible


@profiler
def part_two(asteroids: List[str]) -> int:
    """
    Solves part two of the problem using the provided input data.

    Args:
        data_input (List[str]): A list of input lines from the puzzle input file.

    Returns:
        int: The result for part two (the ID of the 200th vaporized asteroid).
    """
    # Step 1: Find best base location
    best_base = None
    max_visible = 0
    for base in asteroids:
        angles = {angle_between(base, other) for other in asteroids if other != base}
        if len(angles) > max_visible:
            best_base = base
            max_visible = len(angles)

    # Step 2: Group asteroids by angle and sort each group by distance
    targets = defaultdict(list)
    for other in asteroids:
        if other == best_base:
            continue
        angle = angle_between(best_base, other)
        # Calculate the Manhattan distance
        dist = abs(best_base[0] - other[0]) + abs(best_base[1] - other[1])
        targets[angle].append((dist, other))

    for group in targets.values():
        group.sort() # Closest first

    # Step 3: Vaporize asteroids in clockwise order
    sorted_angles = sorted(targets.keys())
    vaporized = []

    while len(vaporized) < 200:
        for angle in sorted_angles:
            if targets[angle]:
                _, asteroid = targets[angle].pop(0)
                vaporized.append(asteroid)
                if len(vaporized) == 200:
                    x, y = asteroid
                    return x * 100 + y

    return -1


if __name__ == "__main__":
    input_data = get_and_parse_asteroids("inputs/10_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
