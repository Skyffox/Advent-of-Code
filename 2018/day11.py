# pylint: disable=line-too-long
"""
Day 11: Chronal Charge

Part 1: What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?
Answer: 21,93

Part 2: What is the X,Y,size identifier of the square with the largest total power?
Answer: 231,108,14
"""

from typing import List
from utils import profiler


def get_input(file_path: str) -> int:
    """
    Reads the input file and returns the grid serial number.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        int: The grid serial number.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return int(file.read().strip())


def power_level(x: int, y: int, serial: int) -> int:
    """
    Calculates the power level of a fuel cell.

    Args:
        x (int): X coordinate (1-based).
        y (int): Y coordinate (1-based).
        serial (int): Grid serial number.

    Returns:
        int: Power level of the cell.
    """
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    # Extract the hundreds digit
    power = (power // 100) % 10
    power -= 5
    return power


def build_grid(serial: int, size: int = 300) -> List[List[int]]:
    """
    Builds the grid of power levels.

    Args:
        serial (int): Grid serial number.
        size (int): Size of the grid (default 300).

    Returns:
        List[List[int]]: 2D grid of power levels.
    """
    return [[power_level(x + 1, y + 1, serial) for x in range(size)] for y in range(size)]


@profiler
def part_one(serial: int) -> str:
    """
    Finds the 3x3 square with the largest total power.

    Args:
        serial (int): Grid serial number.

    Returns:
        str: The top-left coordinate of the 3x3 square with the largest power, as 'x,y'.
    """
    grid = build_grid(serial)
    max_power = float('-inf')
    coord = (0, 0)

    for y in range(298):
        for x in range(298):
            total = sum(grid[y + dy][x + dx] for dy in range(3) for dx in range(3))
            if total > max_power:
                max_power = total
                coord = (x + 1, y + 1)

    return f"{coord[0]},{coord[1]}"


@profiler
def part_two(serial: int) -> str:
    """
    Finds the square of any size with the largest total power.

    Args:
        serial (int): Grid serial number.

    Returns:
        str: The top-left coordinate and size of the square with the largest power, as 'x,y,size'.
    """
    grid = build_grid(serial)
    size = 300

    # Build a Summed-Area Table (SAT) for fast subgrid power sum queries
    # sat[y][x] contains the sum of all grid values from (1,1) to (x,y)
    sat = [[0] * (size + 1) for _ in range(size + 1)]
    for y in range(1, size + 1):
        for x in range(1, size + 1):
            # Use the inclusion-exclusion principle to compute the prefix sum
            sat[y][x] = (
                grid[y - 1][x - 1]  # current cell
                + sat[y - 1][x]     # sum from above
                + sat[y][x - 1]     # sum from left
                - sat[y - 1][x - 1] # remove double-counted top-left
            )

    max_power = float('-inf')
    result = (0, 0, 0) # To store the top-left coordinate and size of the best square

    for sq_size in range(1, size + 1):
        for y in range(1, size - sq_size + 2):
            for x in range(1, size - sq_size + 2):
                # Calculate the total power in the square using the SAT
                total = (
                    sat[y + sq_size - 1][x + sq_size - 1]  # bottom-right
                    - sat[y - 1][x + sq_size - 1]          # above the square
                    - sat[y + sq_size - 1][x - 1]          # left of the square
                    + sat[y - 1][x - 1]                    # top-left overlap (added back)
                )
                if total > max_power:
                    max_power = total
                    result = (x, y, sq_size)

    return f"{result[0]},{result[1]},{result[2]}"


if __name__ == "__main__":
    serial_number = get_input("inputs/11_input.txt")

    print(f"Part 1: {part_one(serial_number)}")
    print(f"Part 2: {part_two(serial_number)}")
