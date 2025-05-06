# pylint: disable=line-too-long
"""
Day 2: Corruption Checksum

Part 1: Find the difference between the largest and smallest number in each row, and sum those differences.  
Answer: 47136

Part 2: In each row, find the only two numbers where one evenly divides the other, and sum the division results.  
Answer: 250
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Parses the tab-separated input file into a list of rows, each containing integers.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[int]]: A list of lists with integers from the input.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(map(int, line.strip().split("\t"))) for line in file]


@profiler
def part_1(rows: List[List[int]]) -> int:
    """
    Calculates the checksum by summing the difference between the max and min of each row.

    Args:
        rows (List[List[int]]): The spreadsheet as a list of rows.

    Returns:
        int: The resulting checksum.
    """
    return sum(max(row) - min(row) for row in rows)


@profiler
def part_2(rows: List[List[int]]) -> int:
    """
    Finds the only pair of numbers in each row where one evenly divides the other,
    and sums the division results.

    Args:
        rows (List[List[int]]): The spreadsheet as a list of rows.

    Returns:
        int: The sum of all the division results.
    """
    total = 0
    for row in rows:
        sorted_row = sorted(row, reverse=True)
        for i, numerator in enumerate(sorted_row):
            for denominator in sorted_row[i+1:]:
                if numerator % denominator == 0:
                    total += numerator // denominator
                    break # Only one such pair per row
    return total


if __name__ == "__main__":
    input_data = get_input("inputs/2_input.txt")

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data)}")
