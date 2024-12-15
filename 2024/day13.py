# pylint: disable=line-too-long
"""
Part 1: Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
Answer: 38714

Part 2: Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
Answer: 74015623345775
"""

import re
from utils import profiler


def get_input(file_path: str) -> list:
    """Get the input data"""
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
    """The Greatest Common Divisor of two numbers is the largest positive integer that divides both of the numbers without leaving a remainder"""
    while b:
        a, b = b, a % b
    return a


def least_common_multiple(a: int, b: int) -> int:
    """The Least Common Multiple (LCM) of two numbers is the smallest positive integer that is divisible by both of the numbers"""
    return abs(a * b) // gcd(a, b)


def linear_equations_solver(x1: int, y1: int, x2: int, y2: int, ans_x: int, ans_y: int) -> int:
    """
    For this problem we can solve it using a system of linear equations, in this case for 2 variables

    Consider the following equations in a system of linear equations:
    x1 + x2 = ans_x     Equation 1
    y1 + y2 = ans_y     Equation 2

    We are going to solve this system of linear equations using the Least Common Multiple (LCM), which is used in the elimination method, 
    where you try to eliminate one of the variables by manipulating the equations so that you can solve for the other  
    """
    # First we find the LCM of our coefficients
    lcm = least_common_multiple(x1, y1)

    # Multiply each equation by a number that will make the coefficients of one of the variables the same (or opposites) so that you can eliminate it.
    x_factor = lcm / x1
    y_factor = lcm / y1

    # Next we need to add or subtract the equations to eliminate one of the variables
    # in our case since the coefficients are always positive we subtract them from each other
    b_num = y_factor * ans_y - x_factor * ans_x
    b_den = y_factor * y2 - x_factor * x2

    # Calculate for the first variable
    b = b_num / b_den

    # Substitute the value of x back into one of the original equations (let's use Equation 1):
    # The remaining equation becomes: ax + bx = ansx -> ax + (bx * b) = ansx -> x = (ans_x - bx*b) / ax
    a_num = ans_x - x2 * b
    a_den = x1

    # Solve for the remaining variable
    a = a_num / a_den

    # We can not have negative values for x and y (because they represents the amount of times we press the button for the claw machine)
    # which is why smaller than zero is wrong. We also can not have non integers for the same reason
    if b_num % b_den != 0 or a_num % a_den != 0 or b < 0 or a < 0:
        return 0

    # Button A is worth 3 tokens and button B is worth 1 token
    return int(a * 3 + b)


@profiler
def part_one(equations: list) -> int:
    """We need to operate a claw machine to get to a specific (X, Y) location, our prize"""
    n = 0
    for equation in equations:
        # x1 and y1 represents how much button A moves our claw
        # x2 and y2 represents how much button B moves our claw
        # ans_x and ans_y represents the location of our prize
        x1, y1, x2, y2, ans_x, ans_y = equation

        n += linear_equations_solver(x1, y1, x2, y2, ans_x, ans_y)

    return n


@profiler
def part_two(equations: list) -> int:
    """We do the same as in part 1 but the location of our prize is now very far away"""
    n = 0
    for equation in equations:
        x1, y1, x2, y2, ans_x, ans_y = equation

        ans_x += 10000000000000
        ans_y += 10000000000000

        n += linear_equations_solver(x1, y1, x2, y2, ans_x, ans_y)

    return n


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
