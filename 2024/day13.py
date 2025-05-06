# pylint: disable=line-too-long
"""
Day 13: Claw Contraption

Part 1: Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
Answer: 38714

Part 2: Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
Answer: 74015623345775
"""

import re
from typing import List
from utils import profiler


def get_input(file_path: str) -> List[List[int]]:
    """
    Parse the input file into a list of equations.

    Each equation is a list of six integers:
        x1, y1 - movement vector for button A
        x2, y2 - movement vector for button B
        ans_x, ans_y - target coordinates of the prize

    Args:
        file_path (str): Path to the input file.

    Returns:
        list[list[int]]: List of equations extracted from the input.
    """
    equations, curr = [], []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line == "\n":
                equations.append(curr)
                curr = []
            else:
                # Extract the numbers from the string and map to integers
                curr.extend(list(map(int, re.findall(r'\d+', line))))
        equations.append(curr)

    return equations


def gcd(a: int, b: int) -> int:
    """
    Compute the Greatest Common Divisor (GCD) of two integers.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: GCD of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def least_common_multiple(a: int, b: int) -> int:
    """
    Compute the Least Common Multiple (LCM) of two integers.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: LCM of a and b.
    """
    return abs(a * b) // gcd(a, b)


def linear_equations_solver(x1: int, y1: int, x2: int, y2: int, ans_x: int, ans_y: int) -> int:
    """
    Solve a system of two linear equations in two variables using elimination.

    The claw can be moved by pressing button A or button B. 
    Each button press adds a vector to the current position.
    
    We need to determine the number of times each button should be pressed 
    to reach a target coordinate, and return the minimum token cost.

    Constraints:
    - A press costs 3 tokens
    - B press costs 1 token
    - Only non-negative integer solutions are valid

    Returns:
        int: Minimum tokens required to reach the target, or 0 if no valid solution.
    """
    # First we find the LCM of our coefficients
    lcm = least_common_multiple(x1, y1)

    # Multiply each equation by a number that will make the coefficients of one of the variables the same (or opposites) so that you can eliminate it.
    x_factor = lcm / x1
    y_factor = lcm / y1

    # Subtract equations to eliminate one variable (here we eliminate x)
    b_num = y_factor * ans_y - x_factor * ans_x
    b_den = y_factor * y2 - x_factor * x2

    # Calculate for button B presses
    b = b_num / b_den

    # Substitute back to solve for button A presses
    a_num = ans_x - x2 * b
    a_den = x1
    a = a_num / a_den

    # Disallow negative or fractional solutions
    if b_num % b_den != 0 or a_num % a_den != 0 or b < 0 or a < 0:
        return 0

    # Button A is worth 3 tokens and button B is worth 1 token
    return int(a * 3 + b)


@profiler
def part_one(equations: List[List[int]]) -> int:
    """
    Part 1:
    Use the claw to reach each target position using the fewest tokens.

    Args:
        equations (list): Parsed input data.

    Returns:
        int: Total minimum token cost across all equations.
    """
    n = 0
    for equation in equations:
        # x1 and y1 represents how much button A moves our claw
        # x2 and y2 represents how much button B moves our claw
        # ans_x and ans_y represents the location of our prize
        x1, y1, x2, y2, ans_x, ans_y = equation

        n += linear_equations_solver(x1, y1, x2, y2, ans_x, ans_y)

    return n


@profiler
def part_two(equations: List[List[int]]) -> int:
    """
    Part 2:
    Solve the same as in part one, but the target coordinates are offset by 10 trillion.

    Args:
        equations (list): Parsed input data.

    Returns:
        int: Total token cost after adjusting prize coordinates.
    """
    n = 0
    for equation in equations:
        x1, y1, x2, y2, ans_x, ans_y = equation

        # Apply the offset to both coordinates
        ans_x += 10000000000000
        ans_y += 10000000000000

        n += linear_equations_solver(x1, y1, x2, y2, ans_x, ans_y)

    return n


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
