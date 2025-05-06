# pylint: disable=line-too-long
"""
Day 1: The Tyranny of the Rocket Equation

Part 1: Calculate the total fuel required for each module based on its mass.  
Answer: 3296269

Part 2: Include the additional fuel required for the fuel itself.  
Answer: 4941547
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Read module masses from the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[int]: A list of module masses.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]


def fuel_calc(mass: int) -> int:
    """
    Calculate the fuel required for a given mass.

    Args:
        mass (int): The mass of a module.

    Returns:
        int: The required fuel.
    """
    return mass // 3 - 2


@profiler
def part_1(masses: List[int]) -> int:
    """
    Compute total fuel required for all modules (no fuel for fuel).

    Args:
        masses (list[int]): List of module masses.

    Returns:
        int: Total fuel required.
    """
    return sum(fuel_calc(m) for m in masses)


@profiler
def part_2(masses: list[int]) -> int:
    """
    Compute total fuel including fuel for the fuel itself.

    Args:
        masses (list[int]): List of module masses.

    Returns:
        int: Total fuel including extra fuel required recursively.
    """
    total = 0
    for mass in masses:
        while (fuel := fuel_calc(mass)) > 0:
            total += fuel
            mass = fuel
    return total


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
