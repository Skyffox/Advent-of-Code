# pylint: disable=line-too-long
"""
Day 17: Trick Shot

Part 1: What is the highest y position it reaches on this trajectory?
Answer: 13203

Part 2: How many distinct initial velocity values cause the probe to be within the target area after any step?
Answer: 5644
"""

from typing import Tuple
from utils import profiler


def get_input(file_path: str) -> Tuple[int, int, int, int]:
    """
    Reads the input file and returns the target area as (x_min, x_max, y_min, y_max).

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Tuple[int, int, int, int]: target area boundaries.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        line = file.read().strip()
        # Format: target area: x=20..30, y=-10..-5
        parts = line.split(": ")[1].split(", ")
        x_part = parts[0][2:]
        y_part = parts[1][2:]
        x_min, x_max = map(int, x_part.split(".."))
        y_min, y_max = map(int, y_part.split(".."))
        return x_min, x_max, y_min, y_max


def simulate_probe(vx: int, vy: int, target: Tuple[int, int, int, int]) -> Tuple[bool, int]:
    """
    Simulates the probe trajectory for given initial velocity.

    Args:
        vx (int): Initial velocity x.
        vy (int): Initial velocity y.
        target (Tuple[int, int, int, int]): (x_min, x_max, y_min, y_max)

    Returns:
        Tuple[bool, int]: (hits target, max y reached)
    """
    x_min, x_max, y_min, y_max = target
    x, y = 0, 0
    max_y = y
    while x <= x_max and y >= y_min:
        x += vx
        y += vy
        max_y = max(max_y, y)
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True, max_y
        # Account for drag
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    return False, max_y


@profiler
def part_one(target: Tuple[int, int, int, int]) -> int:
    """
    Finds the highest y position reached for any velocity hitting the target.

    Args:
        target (Tuple[int, int, int, int]): target area.

    Returns:
        int: Highest y reached.
    """
    _, x_max, y_min, _ = target
    max_height = 0
    # Reasonable velocity bounds:
    for vx in range(1, x_max + 1):
        for vy in range(y_min, 1000):  # Upper bound for vy heuristic
            hit, height = simulate_probe(vx, vy, target)
            if hit and height > max_height:
                max_height = height
    return max_height


@profiler
def part_two(target: Tuple[int, int, int, int]) -> int:
    """
    Counts how many initial velocities hit the target area.

    Args:
        target (Tuple[int, int, int, int]): target area.

    Returns:
        int: Count of valid velocities.
    """
    _, x_max, y_min, _ = target
    count = 0
    for vx in range(1, x_max + 1):
        for vy in range(y_min, 1000):  # Upper bound for vy heuristic
            hit, _ = simulate_probe(vx, vy, target)
            if hit:
                count += 1
    return count


if __name__ == "__main__":
    target_area = get_input("inputs/17_input.txt")

    print(f"Part 1: {part_one(target_area)}")
    print(f"Part 2: {part_two(target_area)}")
