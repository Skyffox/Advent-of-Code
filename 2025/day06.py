# pylint: disable=line-too-long
"""
Day 6 Challenge: Trash Compactor

Part 1: Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation that needs to be performed. 
Problems are separated by a full column of only spaces. What is the grand total found by adding together all of the answers to the individual problems?
Answer: 5977759036837

Part 2: The way we read the problem was wrong. We instead need to read right-to-left in columns. Each number is given in its own column, with the most 
significant digit at the top and the least significant digit at the bottom, allignment of numbers is key. 
What is the grand total found by adding together all of the answers to the individual problems?
Answer: 9630000828442
"""

import math
from typing import List
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Reads a text file and converts it into a grid of characters.

    Each line in the file is split by spaces into individual string elements.
    Empty strings are preserved to maintain spacing.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: 2D list of characters representing the input grid.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.rstrip().split(" ") for line in file]


@profiler
def part_one(data_input: List[List[str]]) -> int:
    """
    Computes Part 1 total by applying column-wise operations.

    - The last row in the input represents operation signs ('+' or '*').
    - Each column of numbers is converted to integers.
    - Columns with '+' are summed, columns with '*' are multiplied.
    - The total sum of all column results is returned.

    Args:
        data_input (List[List[str]]): Input grid of strings.

    Returns:
        int: Total sum after applying operations.
    """
    # Remove empty cells
    clean_input = [[x for x in row if x != ""] for row in data_input]

    # Last row contains the operation signs
    signs = clean_input[-1]
    numbers = clean_input[:-1]

    # Transpose to get column-wise data
    transposed = [list(col) for col in zip(*numbers)]

    total = 0
    for col, sign in zip(transposed, signs):
        # Convert the entire row of strings to numbers
        nums = [int(''.join(filter(str.isdigit, x))) for x in col]

        if sign == "+":
            total += sum(nums)
        else:
            total += math.prod(nums)

    return total


@profiler
def part_two(data_input: List[List[str]]) -> int:
    """
    Computes Part 2 total by grouping numbers based on consecutive operation signs.

    Rules:
    - Numbers separated by '*' are multiplied together.
    - Numbers separated by '+' are summed immediately.
    - Operations are applied column-wise, with the last row representing signs.

    Args:
        data_input (List[List[str]]): Input grid of strings.

    Returns:
        int: Computed total after applying grouped operations.
    """
    # We need to preserve spacing in the input in order to group numbers based on vertical allignment
    equations = []
    for line in data_input:
        row_expanded: List[str] = []
        for item in line:
            if item == "":
                row_expanded.append("")
            else:
                row_expanded.extend(list(item))
        equations.append(row_expanded)

    signs = equations[-1]
    numbers = equations[:-1]

    # Transpose to get column-wise data
    transposed = [list(x) for x in zip(*numbers)]

    # Ensure signs list is as long as columns
    if len(transposed) > len(signs):
        signs.extend([""] * (len(transposed) - len(signs)))

    total = 0
    current_sign = ""
    mult_group: List[int] = []

    for col, sign in zip(transposed, signs):
        # Convert column to integer number
        number = int(''.join(x for x in col if x != ''))

        if sign:
            # Process previous multiplication group if switching signs
            if current_sign == "*":
                total += math.prod(mult_group)
                mult_group = []
            current_sign = sign

        if current_sign == "+":
            total += number
        else:
            mult_group.append(number)

    return total


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/6_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
