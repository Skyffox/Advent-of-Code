# pylint: disable=line-too-long
"""
Day 3: Mull It Over

Part 1: Find all correct occurrences of mul(number, number) in input
Answer: 184511516

Part 2: Do not execute mul() statements if a don't() came before it, we may execute again if we encounter a do() statement
Answer: 90044227
"""

import re
from typing import List
from utils import profiler


def get_input(file_path: str) -> str:
    """
    Read the entire input file and return it as a single string with line breaks removed.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: Concatenated string from file content with stripped lines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return "".join(line.strip() for line in file)


@profiler
def regex_numbers(inp_str: str) -> int:
    """
    Find all mul(a,b) patterns in the input string, extract the numbers,
    perform multiplication, and return the total sum.

    Args:
        inp_str (str): The input string containing function-like statements.

    Returns:
        int: The sum of all evaluated multiplications from valid mul(a,b) statements.
    """
    matches: List[str] = re.findall(r"mul\(\d+,\d+\)", inp_str)

    # Extract pairs of numbers from each match
    equations = (re.findall(r"\d+", match) for match in matches)

    # Compute and return the total sum of products
    return sum(int(a) * int(b) for a, b in equations)


if __name__ == "__main__":
    INPUT = get_input("inputs/3_input.txt")

    # Remove all the parts that are between don't() and do()
    clean_inp = re.sub(r"don't\(\).+?do\(\)", "", INPUT)

    print(f"Part 1: {regex_numbers(INPUT)}")
    print(f"Part 2: {regex_numbers(clean_inp)}")
