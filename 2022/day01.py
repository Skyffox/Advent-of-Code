# pylint: disable=line-too-long
"""
Day 1: Calorie Counting

Part 1: Find the Elf carrying the most Calories.  
Answer: 72240

Part 2: Find the top three Elves carrying the most Calories.  
Answer: 210957
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[int]:
    """
    Parses the input file and returns a list of calorie sums carried by each Elf.
    Each Elf's inventory is separated by a blank line.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[int]: List of total calories per Elf.
    """
    elf_totals = []
    current_total = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped == "":
                elf_totals.append(current_total)
                current_total = 0
            else:
                current_total += int(stripped)

        # Add the last Elf's total if not followed by a blank line
        if current_total > 0:
            elf_totals.append(current_total)

    return elf_totals


@profiler
def part_1(calorie_totals: List[int]) -> int:
    """
    Returns the maximum calories carried by a single Elf.

    Args:
        calorie_totals (List[int]): List of total calories per Elf.

    Returns:
        int: Maximum value in the list.
    """
    return max(calorie_totals)


@profiler
def part_2(calorie_totals: List[int]) -> int:
    """
    Returns the sum of calories carried by the top three Elves.

    Args:
        calorie_totals (List[int]): List of total calories per Elf.

    Returns:
        int: Sum of the top three highest calorie totals.
    """
    return sum(sorted(calorie_totals, reverse=True)[:3])


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
