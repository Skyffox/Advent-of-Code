# pylint: disable=line-too-long
"""
Part 1: Find all correct occurences of mul(number, number) in input
Answer: 184511516

Part 2: Do not execute mul() statements if a don't() came before it, we may execute again if we encounter a do() statement
Answer: 121869966
"""

import re
from utils import profiler


def get_input(file_path: str) -> str:
    """Get the input data"""
    with open(file_path, "r", encoding="utf-8") as file:
        return "".join(file.readlines())


@profiler
def regex_numbers(inp_str: str) -> int:
    """Search for all mul() statements and multiply the two numbers for all instances"""
    x = re.findall(r"mul\(\d+,\d+\)", inp_str)

    # Get the two numbers from the multiplication
    equations = [re.findall(r"\d+", nums) for nums in x]

    # Get the sum of all valid instructions
    return sum([int(eq[0]) * int(eq[1]) for eq in equations])


if __name__ == "__main__":
    # Get input data
    INPUT = get_input("inputs/3_input.txt")

    # Remove all the parts that are between don't() and do()
    clean_inp = re.sub(r"don't\(\).+?do\(\)", "", INPUT)

    print(f"Part 1: {regex_numbers(INPUT)}")
    print(f"Part 2: {regex_numbers(clean_inp)}")
