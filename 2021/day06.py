# pylint: disable=line-too-long
"""
Day 6: Lanternfish

Part 1: Find a way to simulate lanternfish. How many lanternfish would there be after 80 days?
Answer: 362666

Part 2: How many lanternfish would there be after 256 days?
Answer: 1640526601595
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Reads the input file and returns a list of lanternfish timers.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        List[int]: List of initial timers for lanternfish.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return list(map(int, file.read().strip().split(",")))


@profiler
def part_one(data_input: List[int]) -> int:
    """
    Simulates lanternfish growth for 80 days and returns the total count.

    Args:
        data_input (List[int]): Initial timers of lanternfish.

    Returns:
        int: Total number of lanternfish after 80 days.
    """
    fish = data_input.copy()
    for _ in range(80):
        new_fish = 0
        for i, timer in enumerate(fish):
            if timer == 0:
                fish[i] = 6
                new_fish += 1
            else:
                fish[i] -= 1
        fish.extend([8] * new_fish)
    return len(fish)


@profiler
def part_two(data_input: List[int]) -> int:
    """
    Simulates lanternfish growth for 256 days using an efficient counting method.

    Args:
        data_input (List[int]): Initial timers of lanternfish.

    Returns:
        int: Total number of lanternfish after 256 days.
    """
    counts = [0] * 9
    for timer in data_input:
        counts[timer] += 1

    for _ in range(256):
        new_fish = counts[0]
        counts = counts[1:] + [new_fish]
        counts[6] += new_fish

    return sum(counts)


if __name__ == "__main__":
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
