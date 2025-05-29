# pylint: disable=line-too-long
"""
Day 7: The Treachery of Whales

Part 1: Determine the horizontal position that the crabs can align to using the least fuel possible. 
        How much fuel must they spend to align to that position?
Answer: 344297

Part 2: Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! 
        How much fuel must they spend to align to that position?
Answer: 97164301
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of crab positions.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: List of crab horizontal positions.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip().split(",")))


def fuel_cost_part2(distance: int) -> int:
    """
    Calculates the fuel cost for moving a given distance with increasing rate.

    Args:
        distance (int): Distance to move.

    Returns:
        int: Fuel cost for that distance.
    """
    return distance * (distance + 1) // 2


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Calculates the minimum fuel needed to align all crabs at the same position (linear cost).

    Args:
        data_input (List[int]): List of crab positions.

    Returns:
        int: Minimum total fuel cost.
    """
    median = sorted(data_input)[len(data_input) // 2]
    return sum(abs(pos - median) for pos in data_input)


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Calculates the minimum fuel needed to align all crabs at the same position (increasing cost).

    Args:
        data_input (List[int]): List of crab positions.

    Returns:
        int: Minimum total fuel cost.
    """
    min_pos = min(data_input)
    max_pos = max(data_input)
    min_fuel = float("inf")

    for target in range(min_pos, max_pos + 1):
        fuel = sum(fuel_cost_part2(abs(pos - target)) for pos in data_input)
        min_fuel = min(fuel, min_fuel)

    return min_fuel


if __name__ == "__main__":
    input_data = get_input("inputs/7_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
