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
                # extract the numbers from the string and map to integers
                curr.extend(list(map(int, re.findall(r'\d+', line))))

        equations.append(curr)

    return equations


def gcd(a, b):
    """The Greatest Common Divisor of two numbers is the largest positive integer that divides both of the numbers without leaving a remainder"""
    while b:
        a, b = b, a % b
    return a


def least_common_multiple(a, b):
    """The Least Common Multiple (LCM) of two numbers is the smallest positive integer that is divisible by both of the numbers"""
    return abs(a * b) // gcd(a, b)


def linear_equations_solver(x1, y1, x2, y2, ans_x, ans_y):
    """
    For this problem we can solve it using a system of linear equations, in this case for 2 variables

    Consider the following equations in a system of linear equations:
    x1 + x2 = ans_x
    y1 + y2 = ans_y

    you can solve a system of linear equations using the Least Common Multiple (LCM), but this method is typically applied when you are working with equations 
    that have integer coefficients and you want to eliminate fractions or simplify the process of elimination. The LCM method is often used in the elimination method, 
    where you try to eliminate one of the variables by manipulating the equations so that you can solve for the other.

    Here's how the method works:
    Write the system of equations in standard form.
    Identify the coefficients of the variable you want to eliminate from both equations.
    Find the LCM of these coefficients.
    Multiply each equation by a number that will make the coefficients of one of the variables the same (or opposites) so that you can eliminate it.
    Add or subtract the equations to eliminate one of the variables.
    Solve for the remaining variable.
    Substitute the value of that variable into one of the original equations to find the other variable.
     

    """

    # Find the Least Common Multiple between the first x and y
    lcm = least_common_multiple(x1, y1)
    
    # 
    x_factor = lcm / x1
    y_factor = lcm / y1

    # Multiply each equation by a number that will make the coefficients of one of the variables the same (or opposites) so that you can eliminate it.

    # multiply each equation with the factor and add/subtract the equations
    # we will solve for x so the eventual equation will look like this: x = answers of the two equations / the other variable
    # Now we need to add or subtrac tthe equations to elimnate the other variable, in our case since the coefficients are always positive we subtract
    b_num = y_factor * ans_y - x_factor * ans_x
    b_den = y_factor * y2 - x_factor * x2


    b = b_num / b_den

    # Solve for the remaining variable.
    a_num = ans_x - x2 * b
    a_den = x1
    # Substitute the value of x back into one of the original equations (let's use Equation 1):
    # The remaining equation becomes: ax + bx = ansx -> ax + (bx * b) = ansx -> x = (ansx - bx*b) / ax
    a = a_num / a_den

    # We can not have negative values for x and y (because they represents the amount of times we press the button for the claw machine) which is why smaller than zero is wrong
    # We also can not have non integers for the same reason
    if b_num % b_den != 0 or a_num % a_den != 0 or b < 0 or a < 0:
        return 0

    # Button A is worth 3 tokens and button B is worth 1 token
    return int(a * 3 + b)


@profiler
def part_one(equations):
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
def part_two(equations):
    """We do the same as in part 1 but the location of our prize is now very far away"""
    n = 0
    for equation in equations:
        ax, ay, bx, by, ansx, ansy = equation

        ansx += 10000000000000
        ansy += 10000000000000

        n += linear_equations_solver(ax, ay, bx, by, ansx, ansy)

    return n


if __name__ == "__main__":
    # Get input data
    input_data = get_input("inputs/13_input.txt")

    print(f"Part 1: {part_one(input_data)}")
    print(f"Part 2: {part_two(input_data)}")
