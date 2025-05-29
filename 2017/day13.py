# pylint: disable=line-too-long
"""
Day 13: Packet Scanners

Part 1: Given the details of the firewall you've recorded, if you leave immediately, what is the severity of your whole trip?
Answer: 1316

Part 2: What is the fewest number of picoseconds that you need to delay the packet to pass through the firewall without being caught?
Answer: 3840052
"""

from typing import List, Dict
from utils import profiler


def get_input(file_path: str) -> Dict[int, int]:
    """
    Reads the input file and parses the input into a dictionary mapping depth to range.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Dict[int, int]: Mapping of layer depth to scanner range.
    """
    firewall = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            depth, rng = line.split(": ")
            firewall[int(depth)] = int(rng)
    return firewall


def caught(firewall: Dict[int, int], delay: int) -> bool:
    """
    Checks if packet is caught given a delay.

    Args:
        firewall (Dict[int, int]): Firewall layers.
        delay (int): Delay before starting.

    Returns:
        bool: True if caught, else False.
    """
    for depth, rng in firewall.items():
        period = 2 * (rng - 1)
        if (depth + delay) % period == 0:
            return True
    return False


@profiler
def part_one(firewall: List[str]) -> int:
    """
    Calculates total severity of getting caught with no delay.

    Args:
        data_input (List[str]): Input firewall data.

    Returns:
        int: Total severity.
    """
    total = 0
    for depth, rng in firewall.items():
        period = 2 * (rng - 1)
        if depth % period == 0:
            total += depth * rng
    return total


@profiler
def part_two(firewall: List[str]) -> int:
    """
    Finds minimum delay to pass without getting caught.

    Args:
        data_input (List[str]): Input firewall data.

    Returns:
        int: Minimum delay.
    """
    delay = 0
    while caught(firewall, delay):
        delay += 1
    return delay


if __name__ == "__main__":
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
