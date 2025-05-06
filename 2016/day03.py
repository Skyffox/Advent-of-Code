# pylint: disable=line-too-long
"""
Day 3: Squares With Three Sides

Part 1: Count how many valid triangles exist where the two smallest sides are greater than the largest side.  
Answer: 917

Part 2: Consider vertical groups of three triangles (based on columns), then determine how many valid triangles there are.  
Answer: 1649
"""

from typing import List
from copy import deepcopy
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Parses the input file and returns a list of lists, where each inner list represents the sides of a triangle.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[int]]: List of triangle sides.
    """
    triangles = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Split the line into integers representing the triangle sides
            triangles.append(list(map(int, line.split())))

    return triangles


@profiler
def part_1(triangles: List[List[int]]) -> int:
    """
    Validates triangles by checking if the sum of the two smallest sides is greater than the largest side.

    Args:
        triangles (List[List[int]]): List of triangle side lengths.

    Returns:
        int: The number of valid triangles.
    """
    valid_count = 0
    for triangle in triangles:
        triangle.sort()
        # Check if the sum of the two smallest sides is greater than the largest side
        if triangle[0] + triangle[1] > triangle[2]:
            valid_count += 1

    return valid_count


@profiler
def part_2(triangles: List[List[int]]) -> int:
    """
    Validates triangles by examining vertical groups of three numbers (columns) and checking validity.

    Args:
        triangles (List[List[int]]): List of triangle side lengths.

    Returns:
        int: The number of valid triangles when considering columns.
    """
    valid_count = 0
    # Process triangles in vertical groups of three
    for i in range(len(triangles) // 3):
        for j in range(3):
            # Extract the three values in the current column
            column = [triangles[i * 3][j], triangles[i * 3 + 1][j], triangles[i * 3 + 2][j]]
            column.sort()
            # Check if the sum of the two smallest sides is greater than the largest side
            if column[0] + column[1] > column[2]:
                valid_count += 1

    return valid_count


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")
    input_data_cpy = deepcopy(input_data)

    print(f"Part 1: {part_1(input_data)}")
    print(f"Part 2: {part_2(input_data_cpy)}")
