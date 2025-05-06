# pylint: disable=line-too-long
"""
Day 1: Trebuchet?!

Part 1: Get the numeric calibration values from the input
Answer: 54081

Part 2: Get the calibration values like in part 1 whilst converting digits in their alphabetical form to their numeric form
Answer: 54649
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[str]:
    """
    Read input from a file and return each line stripped of whitespace.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[str]: A list of input lines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@profiler
def part_1(lines: List[str]) -> int:
    """
    Extract the first and last numeric digits from each line and form a two-digit number.
    Sum all such numbers for the input.

    Args:
        lines (List[str]): List of input strings.

    Returns:
        int: Sum of the two-digit numbers formed from each line.
    """
    total = 0
    for line in lines:
        numbers = [str(x) for x in line if x.isnumeric()]
        if numbers:
            total += int(numbers[0] + numbers[-1])
    return total


@profiler
def part_2(lines: List[str]) -> int:
    """
    Like part 1, but replaces alphabetic digit words (e.g., "one", "two") with their numeric equivalents first.

    Args:
        lines (List[str]): List of input strings.

    Returns:
        int: Sum of the two-digit numbers formed from each line after conversion.
    """
    digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    total = 0

    for line in lines:
        while True:
            # Find all indices of digit words in the line
            indices = [(line.find(word), index + 1) for index, word in enumerate(digits) if line.find(word) != -1]
            if indices:
                # Replace the first index of the number with the numeric equivalent. Cast to list and back so we can mutate.
                line = list(line)
                for idx, replacement in indices:
                    line[idx] = str(replacement)
                line = "".join(line)
            else:
                break

        # Add the first and last numeric value of the input string.
        numbers = [str(x) for x in line if x.isnumeric()]
        if numbers:
            total += int(numbers[0] + numbers[-1])

    return total


if __name__ == "__main__":
    input_data = get_input("inputs/1_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
