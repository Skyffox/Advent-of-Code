# pylint: disable=line-too-long
"""
Day 3: Gear Ratios

Part 1: Find all numeric values that are adjacent to a symbol (not the dot)
Answer: 554003

Part 2: Find the numeric values of which there are TWO adjacent to the * symbol
Answer: 87263515
"""

from typing import List, Tuple, Union
from utils import profiler


def get_input(file_path: str) -> List[List[str]]:
    """
    Read the input file and return the grid as a list of character lists.

    Args:
        file_path (str): Path to the input file.

    Returns:
        List[List[str]]: 2D grid of characters.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [list(line.strip()) for line in file]


def check_value(y: int, x: int, grid: List[List[str]]) -> Tuple[bool, Union[Tuple[int, int], tuple]]:
    """
    Check the 3x3 area around a coordinate for any symbol other than a digit or a dot.
    If a '*' is found, its coordinates are returned separately.

    Args:
        y (int): Y-coordinate in the grid.
        x (int): X-coordinate in the grid.
        grid (List[List[str]]): The character grid.

    Returns:
        Tuple[bool, Tuple[int, int] or empty tuple]: 
            - True if a symbol is found near the coordinate.
            - Coordinate of '*' if found, else empty tuple.
    """
    asterisk_coord = ()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            new_y, new_x = y + y_offset, x + x_offset

            # Ensure coordinates are within bounds
            if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]):
                val = grid[new_y][new_x]
                if not val.isdigit() and val != '.':
                    if val == "*":
                        asterisk_coord = (new_y, new_x)
                    return True, (new_y, new_x)

    return False, asterisk_coord


@profiler
def part_1(grid: List[List[str]]) -> Tuple[int, List[Tuple[int, List[Tuple[int, int]]]]]:
    """
    Locate all numbers in the grid and sum those that are adjacent to any symbol (excluding dots).

    Args:
        grid (List[List[str]]): 2D grid of characters.

    Returns:
        Tuple[int, List[Tuple[int, List[Tuple[int, int]]]]]: 
            - Total sum of valid numbers.
            - List of all numbers with their coordinates for reuse in part 2.
    """
    number_coords = []
    total = 0

    for y, line in enumerate(grid):
        temp = []
        for x, val in enumerate(line):
            if val.isdigit():
                temp.append([val, (y, x)])
                if x == len(line) - 1 or not line[x + 1].isdigit():
                    num = int(''.join([item[0] for item in temp]))
                    coords = [item[1] for item in temp]
                    number_coords.append((num, coords))
                    temp = []

    # Check adjacency to any symbol
    for num, coords in number_coords:
        if any(check_value(y, x, grid)[0] for y, x in coords):
            total += num

    return total, number_coords


@profiler
def part_2(number_coords: List[Tuple[int, List[Tuple[int, int]]]], grid: List[List[str]]) -> int:
    """
    Compute the gear ratio by finding '*' symbols adjacent to exactly two numbers,
    then multiply those numbers together and sum the results.

    Args:
        number_coords (List[Tuple[int, List[Tuple[int, int]]]]): List of numbers and their coordinates from part 1.
        grid (List[List[str]]): The character grid.

    Returns:
        int: Total gear ratio from all valid '*' gears.
    """
    gear_ratio = 0
    asterisks = {}

    for num, coords in number_coords:
        for y, x in coords:
            _, asterisk = check_value(y, x, grid)
            if asterisk:
                asterisks.setdefault(asterisk, []).append(num)
                break # Avoid double-counting this number

    for nums in asterisks.values():
        if len(nums) == 2:
            gear_ratio += nums[0] * nums[1]

    return gear_ratio


if __name__ == "__main__":
    input_data = get_input("inputs/3_input.txt")

    total_nums, coordinate_lst = part_1(input_data)

    print(f"Part 1: {total_nums}")
    print(f"Part 2: {part_2(coordinate_lst, input_data)}")
