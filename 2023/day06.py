# pylint: disable=line-too-long
"""
Day 6: Wait For It

Part 1: Calculate in how many ways you can beat the record distance  
Answer: 1660968

Part 2: All time and distance inputs have been concatenated into one number, solve part 1 again for this new input  
Answer: 26499773
"""

from math import ceil, floor, prod
from typing import List
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Read race data from a file. The file contains two lines:
    one for times and one for distances.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[int]]: Two-element list containing times and distances as lists of integers.
    """
    lines: List[List[int]] = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(":")[1].split(" ")
            lines.append([int(x) for x in line if x != ""])

    return lines


def solve(time: int, distance: int) -> int:
    """
    Use the quadratic formula to determine how many whole-number
    durations (button-hold times) result in a distance greater than the record.

    Based on the equation:
        distance = t * (time - t)  =>  -t^2 + time*t - distance = 0

    Args:
        time (int): Total race time.
        distance (int): Record distance to beat.

    Returns:
        int: Number of integer solutions where distance > record.
    """
    delta = (time**2 - 4 * distance)**0.5
    low, high = (time - delta) / 2, (time + delta) / 2

    return ceil(high) - floor(low) - 1


@profiler
def part_1(races: List[List[int]]) -> int:
    """
    For each race, calculate the number of ways to beat the record distance
    and return the product of all such values.

    Args:
        races (List[List[int]]): List containing time and distance data.

    Returns:
        int: Product of the number of winning combinations per race.
    """
    return prod(solve(t, d) for t, d in zip(races[0], races[1]))


@profiler
def part_2(races: List[List[int]]) -> int:
    """
    Combine all times and distances into a single value each, then compute
    how many ways you can beat the combined race.

    Args:
        races (List[List[int]]): List containing time and distance digits.

    Returns:
        int: Number of ways to beat the combined race.
    """
    full_time = int("".join(map(str, races[0])))
    full_distance = int("".join(map(str, races[1])))
    return solve(full_time, full_distance)


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
